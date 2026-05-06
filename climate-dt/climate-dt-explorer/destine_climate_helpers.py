"""
Helper module for DestinE Climate DT data retrieval via Polytope.

Hides most technical steps (polytope addresses, request construction, file I/O, chunking).
All science (differencing, plotting, analysis) is in the notebook.
"""

import os
import gc
import logging
import pandas as pd
import earthkit.data
import xarray as xr
import numpy as np

# Earthkit cache configuration — prevents unbounded cache growth
earthkit.data.config.set("cache-policy", "temporary")
earthkit.data.config.set("maximum-cache-size", "2G")

# Suppress verbose logging from earthkit and polytope
for _logger_name in ("earthkit.data", "polytope", "polytope.api",
                      "polytope_client", "urllib3"):
    logging.getLogger(_logger_name).setLevel(logging.WARNING)


def get_polytope_address(model):
    """Return the correct Polytope server address for a given model."""
    if model.upper() == 'IFS-NEMO':
        return "polytope.mn5.apps.dte.destination-earth.eu"
    return "polytope.lumi.apps.dte.destination-earth.eu"


def _infer_activity(experiment):
    """Infer the activity from the experiment name."""
    if experiment in ('hist', 'cont'):
        return 'baseline'
    elif experiment == 'SSP3-7.0':
        return 'projections'
    else:
        raise ValueError(
            f"Unknown experiment '{experiment}'. "
            "Expected 'hist', 'cont', or 'SSP3-7.0'."
        )


def build_clmn_request(model, experiment, years, param,
                        resolution='standard', realization='1'):
    """Build a Polytope request dict for the clmn (monthly) stream.

    years can be a single int or an iterable of ints. Multiple years
    are joined with '/' so Polytope returns them all in one request.
    """
    if isinstance(years, (int, np.integer)):
        year_str = str(years)
    else:
        year_str = '/'.join(str(y) for y in years)

    return {
        "class": "d1",
        "dataset": "climate-dt",
        "type": "fc",
        "expver": "0001",
        "generation": "2",
        "realization": realization,
        "activity": _infer_activity(experiment),
        "experiment": experiment,
        "model": model.upper(),
        "param": param,
        "levtype": "sfc",
        "resolution": resolution,
        "stream": "clmn",
        "year": year_str,
        "month": "1/2/3/4/5/6/7/8/9/10/11/12",
    }


def _fetch_chunk(model, experiment, years, param,
                 resolution='standard', realization='1'):
    """
    Download a chunk of years in a single Polytope request.

    Returns an xarray DataArray with a 'valid_time' dimension, or None on failure.
    """
    request = build_clmn_request(model, experiment, years, param,
                                  resolution, realization)
    print(request)
    address = get_polytope_address(model)

    try:
        #earthkit.data.cache.purge()
        data = earthkit.data.from_source(
            "polytope", "destination-earth", request,
            address=address, stream=False
        )
        # Convert to xarray, splitting along valid_time for proper time axis
        a, b = data.to_xarray(split_dims=['valid_time'])
        ds = xr.concat(
            a,
            xr.DataArray(
                dims=b[0].keys(),
                data=[i['valid_time'] for i in b]
            )
        )
        # ds is a Dataset; return the first (and only) data variable
        var_name = list(ds.data_vars)[0]
        da = ds[var_name]

        # Clean up earthkit metadata attribute if present (not serialisable)
        if '_earthkit' in da.attrs:
            da = da.assign_attrs({'_earthkit': str(da.attrs['_earthkit'])})

        del data, ds
        gc.collect()
        return da

    except Exception as e:
        print(f"  WARNING: failed to fetch {model} {experiment} "
              f"years={list(years)}: {e}")
        return None


def fetch_period(model, experiment, years, param,
                 resolution='standard', store_data=False,
                 data_dir='./data', realization='1',
                 chunk_size=35):
    """
    Download multiple years of monthly data, optionally caching to disk.

    Parameters
    ----------
    model : str
        Model name ('ICON', 'IFS-FESOM', 'IFS-NEMO').
    experiment : str
        Experiment name ('hist', 'cont', 'SSP3-7.0').
    years : iterable of int
        Years to download.
    param : str
        Parameter code (e.g. '228004' for avg_2t).
    resolution : str
        'standard' or 'high'.
    store_data : bool
        If True, save a single NetCDF file per chunk and skip if it exists.
    data_dir : str
        Root directory for stored data.
    realization : str
        Realization number (default '1').
    chunk_size : int
        Number of years per Polytope request.

    Returns
    -------
    xarray.DataArray
        Concatenated data with a 'valid_time' dimension covering all months
        across all years.
    """
    years_list = list(years)
    chunks = [years_list[i:i + chunk_size]
              for i in range(0, len(years_list), chunk_size)]
    chunk_arrays = []
    print("here")

    for chunk_years in chunks:
        print(f"Processing years {chunk_years[0]}-{chunk_years[-1]}...")
        y0, y1 = chunk_years[0], chunk_years[-1]

        # If storing, check if ALL individual year files exist for this chunk
        if store_data:
            outdir = os.path.join(
                data_dir, model.upper(), experiment, 'clmn', resolution
            )
            os.makedirs(outdir, exist_ok=True)

            cached = []
            missing_years = []
            for y in chunk_years:
                fp = os.path.join(outdir, f"{param}_{y}.nc")
                if os.path.isfile(fp):
                    cached.append(xr.open_dataarray(fp))
                else:
                    missing_years.append(y)

            if not missing_years:
                print(f"  {model} {experiment} {y0}-{y1}: loading from cache")
                chunk_arrays.extend(cached)
                continue
            else:
                # Close any partially loaded files
                for c in cached:
                    c.close()

        print(f"  {model} {experiment} {y0}-{y1}: downloading "
              f"({len(chunk_years)} years in one request)...")
        da = _fetch_chunk(model, experiment, chunk_years, param,
                          resolution, realization)

        if da is None and len(chunk_years) > 1:
            # Chunk request failed, e.g. ICON, then fall back to year-by-year requests
            print(f"  {model} {experiment} {y0}-{y1}: chunk failed, "
                  f"retrying year by year...")
            for y in chunk_years:
                da_y = _fetch_chunk(model, experiment, [y], param,
                                    resolution, realization)
                if da_y is not None:
                    if store_data:
                        fp = os.path.join(outdir, f"{param}_{y}.nc")
                        if not os.path.isfile(fp):
                            da_y.to_netcdf(fp)
                    chunk_arrays.append(da_y)
            continue

        if da is None:
            continue

        # Save individual year files if requested
        if store_data:
            vt = pd.to_datetime(da['valid_time'].values)
            for y in chunk_years:
                year_da = da.sel(valid_time=vt.year == y)
                fp = os.path.join(outdir, f"{param}_{y}.nc")
                if not os.path.isfile(fp):
                    year_da.to_netcdf(fp)

        chunk_arrays.append(da)

    if not chunk_arrays:
        raise RuntimeError(
            f"No data retrieved for {model} {experiment} "
            f"({years_list[0]}-{years_list[-1]})"
        )

    return xr.concat(chunk_arrays, dim='valid_time')
