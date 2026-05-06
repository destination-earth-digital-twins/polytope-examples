"""
Virtual Zarr store backed by Polytope.

Presents DestinE Climate DT data as an xarray Dataset where metadata is
available instantly and data chunks are fetched lazily on access (e.g.
when plotting or calling .values).

Usage:
    from polytope_zarr import PolytopeZarrStore
    store = PolytopeZarrStore(address=..., collection=..., base_request=...,
                              coords=..., variables=..., internal_dims=...)
    ds = store.open()
"""

import json
import logging
import numpy as np
import pandas as pd
from collections.abc import MutableMapping
from contextlib import contextmanager

# Try to import VLenUTF8 for proper string coordinates
try:
    from numcodecs import VLenUTF8
    _HAS_VLENUTF8 = True
except ImportError:
    _HAS_VLENUTF8 = False


@contextmanager
def _quiet_polytope_loggers():
    """Temporarily silence polytope/earthkit loggers during a Polytope request.

    The polytope Client creates per-instance child loggers with their own
    StreamHandlers at INFO level (bypassing parent logger settings).
    We set the *parent* logger level to WARNING so that newly-created child
    loggers (level NOTSET) inherit it and never process INFO messages, then
    also walk existing loggers to raise handler levels directly.
    """
    def _suppress():
        prefix = ("polytope", "earthkit")
        # Set parent logger level so new children inherit WARNING
        for p in prefix:
            logging.getLogger(p).setLevel(logging.WARNING)
        # Silence handlers on any existing child loggers
        for name, lg in logging.Logger.manager.loggerDict.items():
            if isinstance(lg, logging.Logger) and name.startswith(prefix):
                lg.setLevel(logging.WARNING)
                for h in lg.handlers:
                    if isinstance(h, logging.StreamHandler) and h.level < logging.WARNING:
                        h.setLevel(logging.WARNING)
    _suppress()
    try:
        yield
    finally:
        _suppress()


class PolytopeZarrStore(MutableMapping):
    """A read-only zarr v2 store that fetches data from Polytope on demand."""

    # ── Factory classmethod ──────────────────────────────────────────

    @classmethod
    def from_climate_dt(cls, models, experiment, levtype,
                        frequency="monthly",
                        years=None,
                        start_date=None, end_date=None,
                        resolution="standard",
                        realization=1,
                        activity=None,
                        address=None,
                        filter_months=None,
                        filter_hours=None):
        """Create a store for DestinE Climate DT Generation 2 data.

        Parameters
        ----------
        models : list of str
            Model names, e.g. ["ICON", "IFS-FESOM", "IFS-NEMO"].
        experiment : str or list of str
            Single experiment ("hist", "cont", "SSP3-7.0", "Tplus2.0K"),
            or a list of experiments for storyline simulations.
            When *activity* = "story-nudging", pass a list like
            ["cont", "hist", "Tplus2.0K"] — these become the "climate"
            dimension in the resulting dataset.
        levtype : str
            "sfc", "pl", "hl", "sol", "o2d", or "o3d".
        frequency : str, optional
            "monthly" (clmn stream, default) or "hourly" (clte stream).
            Ignored when *activity* = "story-nudging" (always clte/hourly).
        years : range or list, optional
            Years to include.  Required when *frequency* = "monthly".
        start_date, end_date : str, optional
            ISO date strings (e.g. "2020-01-01").  Required when
            *frequency* = "hourly" or *activity* = "story-nudging".
        filter_months : list of int, optional
            Restrict the time axis to these months (1–12).  Works with
            both ``frequency="monthly"`` and ``frequency="hourly"``.
            E.g. ``[6, 7, 8]`` for JJA.  Also constrains feature and
            area requests so only these months are fetched server-side.
        filter_hours : list of int, optional
            Restrict the time axis to these hours (0–23).  Only valid
            with *frequency* = "hourly".  E.g. ``[12, 13, 14]`` for
            12/13/14 UTC.  Also constrains feature and area requests
            so only these hours are fetched server-side.
        resolution : str, optional
            "standard" (nside 128) or "high".  Default "standard".
            High resolution is nside 1024 (4.4 km) for baseline/projections,
            nside 512 (9 km) for storylines.
        realization : int, optional
            Realization number.  Default 1.
        activity : str, optional
            "baseline", "projections", or "story-nudging".
            Default None = auto-detect ("hist"/"cont" → "baseline",
            else "projections").  Must be set explicitly for storyline
            simulations ("story-nudging"); storylines are IFS-FESOM only.
        address : str, optional
            Override the Polytope server URL.  When set, all models use
            this address (e.g. for test servers like
            ``"polytope-test.mn5.apps.dte.destination-earth.eu"``).
            Default None = auto-detect per model.

        Returns
        -------
        PolytopeZarrStore
        """
        from destine_portfolio import (PORTFOLIO_GEN2_CLMN, PORTFOLIO_GEN2_CLTE,
                                       PORTFOLIO_GEN2_STORYLINE)

        # ── Storyline path ──────────────────────────────────────────
        if activity == "story-nudging":
            if start_date is None or end_date is None:
                raise ValueError(
                    "start_date and end_date are required for storyline simulations")
            experiments = experiment if isinstance(experiment, list) else [experiment]
            stream = "clte"
            portfolio = PORTFOLIO_GEN2_STORYLINE
            _address = address or "polytope.mn5.apps.dte.destination-earth.eu"

            # Storylines ran at 9 km (nside 512), not 4.4 km (nside 1024)
            nside = 128 if resolution == "standard" else 512
            n_cells = 12 * nside ** 2
            lt = portfolio[levtype]
            freq = lt["freq"]

            if freq == "h":
                time_axis = pd.date_range(start_date, end_date, freq="h")
                time_fields = ["date", "time"]
                batch_size = 24
            elif freq == "D":
                time_axis = pd.date_range(start_date, end_date, freq="D")
                time_fields = ["date", "time"]
                batch_size = 1
            else:
                raise ValueError(f"Unknown portfolio freq {freq!r}")

            coords = {"time": time_axis, "cell": range(n_cells),
                      "climate": experiments}
            if lt["levels"] is not None:
                coords["level"] = lt["levels"]

            base_request = {
                "class": "d1",
                "dataset": "climate-dt",
                "type": "fc",
                "expver": "0001",
                "generation": "2",
                "realization": str(realization),
                "activity": "story-nudging",
                "model": "IFS-FESOM",
                "levtype": lt["levtype"],
                "resolution": resolution,
                "stream": stream,
            }

            store = cls(
                address=_address,
                collection="destination-earth",
                base_request=base_request,
                coords=coords,
                variables=lt["variables"],
                internal_dims=["cell"],
                time_fields=time_fields,
                batch_size=batch_size,
            )
            store._frequency = "hourly"
            store._freq = freq
            store._resolution = resolution
            store.nside = nside
            return store

        # ── Standard path (baseline / projections) ──────────────────
        # Validate frequency / time args
        if frequency == "monthly":
            if years is None:
                raise ValueError("years is required when frequency='monthly'")
            stream = "clmn"
            portfolio = PORTFOLIO_GEN2_CLMN
        elif frequency == "hourly":
            if start_date is None or end_date is None:
                raise ValueError(
                    "start_date and end_date are required when frequency='hourly'")
            stream = "clte"
            portfolio = PORTFOLIO_GEN2_CLTE
        else:
            raise ValueError(f"frequency must be 'monthly' or 'hourly', got {frequency!r}")

        # Derived parameters
        nside = 128 if resolution == "standard" else 1024
        n_cells = 12 * nside ** 2
        if activity is None:
            activity = "baseline" if experiment in ("hist", "cont") else "projections"
        if address is not None:
            _address = address
        else:
            _address = {m: ("polytope.mn5.apps.dte.destination-earth.eu"
                            if m == "IFS-NEMO" else
                            "polytope.lumi.apps.dte.destination-earth.eu")
                        for m in models}

        # Portfolio lookup
        lt = portfolio[levtype]

        # Time axis & request fields from portfolio freq
        freq = lt["freq"]  # "MS", "h", or "D"
        # Validate filter_hours vs frequency (filter_months works with both)
        if filter_hours is not None and frequency != "hourly":
            raise ValueError("filter_hours= is only valid with frequency='hourly'")

        if freq == "MS":
            time_axis = pd.date_range(
                f"{min(years)}-01", f"{max(years)}-12", freq="MS")
            if filter_months is not None:
                time_axis = time_axis[time_axis.month.isin(filter_months)]
            time_fields = ["year", "month"]
            batch_size = len(filter_months) if filter_months else 12
        elif freq == "h":
            time_axis = pd.date_range(start_date, end_date, freq="h")
            if filter_months is not None:
                time_axis = time_axis[time_axis.month.isin(filter_months)]
            if filter_hours is not None:
                time_axis = time_axis[time_axis.hour.isin(filter_hours)]
            time_fields = ["date", "time"]
            batch_size = len(filter_hours) if filter_hours else 24
        elif freq == "D":
            time_axis = pd.date_range(start_date, end_date, freq="D")
            time_fields = ["date", "time"]
            batch_size = 1
        else:
            raise ValueError(f"Unknown portfolio freq {freq!r}")

        # Coordinates
        coords = {"time": time_axis, "cell": range(n_cells), "model": models}
        if lt["levels"] is not None:
            coords["level"] = lt["levels"]

        base_request = {
            "class": "d1",
            "dataset": "climate-dt",
            "type": "fc",
            "expver": "0001",
            "generation": "2",
            "realization": str(realization),
            "activity": activity,
            "experiment": experiment,
            "levtype": lt["levtype"],
            "resolution": resolution,
            "stream": stream,
        }

        store = cls(
            address=_address,
            collection="destination-earth",
            base_request=base_request,
            coords=coords,
            variables=lt["variables"],
            internal_dims=["cell"],
            time_fields=time_fields,
            batch_size=batch_size,
        )
        store._frequency = frequency
        store._freq = freq  # "MS", "h", or "D" — from portfolio
        store._resolution = resolution
        store._filter_months = filter_months
        store._filter_hours = filter_hours
        store.nside = nside
        return store

    # ── Constructor ──────────────────────────────────────────────────

    def __init__(self, address, collection, base_request, coords, variables,
                 internal_dims=None, time_fields=None, batch_dim="time",
                 batch_size=12, batch_years=1, batch_days=1):
        """
        Parameters
        ----------
        address : str or dict
            Polytope server URL, or {model_name: url} for per-model routing.
        collection : str
            Polytope collection name (e.g. "destination-earth").
        base_request : dict
            Fixed request fields (class, dataset, experiment, …).
            Do NOT include year/month/day/time/param/model — those are per-chunk.
        coords : dict
            {dim_name: array-like} — e.g. {"time": pd.date_range(...),
            "cell": range(196608), "model": ["ICON", "IFS-FESOM"]}.
        variables : dict
            {var_name: {"dims": ("model", "time", "cell")}}.
        internal_dims : list, optional
            Dims that form a single chunk (e.g. ["cell"]).
        time_fields : list, optional
            Request fields extracted from timestamps. Default ["year", "month"].
        batch_dim : str, optional
            Dimension to batch over in a single Polytope request.  Default "time".
            Set to None to disable batching (one request per chunk).
        batch_size : int, optional
            Maximum number of time steps per batch unit to fetch in one request.
            Default 12 (= all months of each year for monthly stores).
        batch_years : int, optional
            For **monthly** stores: maximum number of calendar years to combine
            in a single Polytope request.  Default 1.
        batch_days : int, optional
            For **hourly** stores: maximum number of calendar days to combine
            in a single Polytope request.  Default 1.
        """
        self._address = address
        self._collection = collection
        self._base_request = dict(base_request)
        self._internal_dims = set(internal_dims or [])
        self._time_fields = time_fields or ["year", "month"]
        self._batch_dim = batch_dim
        self._batch_size = batch_size
        self._batch_years = batch_years
        self._batch_days = batch_days
        self._frequency = getattr(self, '_frequency', 'monthly')  # set by factory
        self._freq = getattr(self, '_freq', None)  # "MS", "h", "D" — set by factory
        self.last_request = None
        self._cache = {}
        self._kv = {}

        # Normalise coordinates to numpy arrays
        self._coords = {}
        self._dim_sizes = {}
        for name, vals in coords.items():
            if name == "time":
                arr = np.array(pd.DatetimeIndex(vals), dtype="datetime64[ns]")
            elif hasattr(vals, '__len__') and not isinstance(vals, str):
                arr = np.array(list(vals))
            else:
                arr = np.array(vals)
            self._coords[name] = arr
            self._dim_sizes[name] = len(arr)

        self._variables = dict(variables)
        self._build_metadata()

    # ── Metadata synthesis ──────────────────────────────────────────────

    def _build_metadata(self):
        """Populate self._kv with zarr v2 metadata and coordinate chunks."""
        self._kv[".zgroup"] = json.dumps({"zarr_format": 2}).encode()
        self._kv[".zattrs"] = json.dumps({}).encode()

        meta = {"zarr_consolidated_format": 1, "metadata": {
            ".zgroup": {"zarr_format": 2}, ".zattrs": {}
        }}

        # Coordinate arrays
        for name, arr in self._coords.items():
            self._write_coord(name, arr, meta)

        # Data variables (metadata only — chunks are lazy)
        for var_name, spec in self._variables.items():
            self._write_var_meta(var_name, spec, meta)

        self._kv[".zmetadata"] = json.dumps(meta).encode()

    def _write_coord(self, name, arr, meta):
        """Write a coordinate array's metadata + data chunk into the store."""
        if arr.dtype.kind == "M":  # datetime
            data = arr.astype("int64")
            zarray = self._zarray(shape=(len(arr),), chunks=(len(arr),),
                                  dtype="|i8", fill_value=0)
            zattrs = {"_ARRAY_DIMENSIONS": [name],
                       "units": "nanoseconds since 1970-01-01",
                       "calendar": "proleptic_gregorian"}
        elif arr.dtype.kind == "U" or arr.dtype.kind == "O":  # strings
            zarray, data = self._encode_strings(arr)
            zattrs = {"_ARRAY_DIMENSIONS": [name]}
        else:  # numeric
            data = arr.astype("int32") if arr.dtype.kind == "i" else arr
            zarray = self._zarray(shape=(len(arr),), chunks=(len(arr),),
                                  dtype=data.dtype.str, fill_value=None)
            zattrs = {"_ARRAY_DIMENSIONS": [name]}

        key_prefix = name
        self._kv[f"{key_prefix}/.zarray"] = json.dumps(zarray).encode()
        self._kv[f"{key_prefix}/.zattrs"] = json.dumps(zattrs).encode()
        self._kv[f"{key_prefix}/0"] = (
            bytes(data) if isinstance(data, (bytes, bytearray)) else data.tobytes()
        )

        meta["metadata"][f"{key_prefix}/.zarray"] = zarray
        meta["metadata"][f"{key_prefix}/.zattrs"] = zattrs

    def _write_var_meta(self, var_name, spec, meta):
        """Write a data variable's zarr metadata (no data — chunks are lazy)."""
        dims = spec["dims"]
        shape = tuple(self._dim_sizes[d] for d in dims)
        chunks = tuple(
            self._dim_sizes[d] if d in self._internal_dims else 1
            for d in dims
        )
        zarray = self._zarray(shape=shape, chunks=chunks,
                              dtype="<f4", fill_value="NaN")
        zattrs = {"_ARRAY_DIMENSIONS": list(dims)}
        # Propagate extra attributes (long_name, units, etc.) from spec
        for attr_key in ("long_name", "units"):
            if attr_key in spec:
                zattrs[attr_key] = spec[attr_key]

        self._kv[f"{var_name}/.zarray"] = json.dumps(zarray).encode()
        self._kv[f"{var_name}/.zattrs"] = json.dumps(zattrs).encode()

        meta["metadata"][f"{var_name}/.zarray"] = zarray
        meta["metadata"][f"{var_name}/.zattrs"] = zattrs

    @staticmethod
    def _zarray(shape, chunks, dtype, fill_value, compressor=None):
        return {"zarr_format": 2, "shape": list(shape),
                "chunks": list(chunks), "dtype": dtype,
                "fill_value": fill_value, "order": "C",
                "compressor": compressor, "filters": None}

    def _encode_strings(self, arr):
        """Encode a string array for zarr v2, using VLenUTF8 if available."""
        vals = [str(v) for v in arr]
        if _HAS_VLENUTF8:
            codec = VLenUTF8()
            data_bytes = codec.encode(np.array(vals, dtype=object))
            zarray = self._zarray(
                shape=(len(vals),), chunks=(len(vals),), dtype="|O",
                fill_value="", compressor=None)
            zarray["filters"] = [codec.get_config()]
            return zarray, data_bytes
        # Fallback: fixed-length bytes
        maxlen = max(len(v) for v in vals)
        data = np.array(vals, dtype=f"|S{maxlen}")
        zarray = self._zarray(shape=(len(vals),), chunks=(len(vals),),
                              dtype=data.dtype.str, fill_value="")
        return zarray, data.tobytes()

    # ── Time helpers ─────────────────────────────────────────────────────

    def _time_to_fields(self, ts):
        """Convert a pandas Timestamp to a dict of Polytope request fields."""
        freq = getattr(self, '_freq', None)
        if freq == "h":
            return {"date": ts.strftime("%Y%m%d"), "time": ts.strftime("%H%M")}
        if freq == "D":
            return {"date": ts.strftime("%Y%m%d"), "time": "0000"}
        # monthly (freq == "MS" or legacy)
        return {"year": str(ts.year), "month": str(ts.month),
                "day": str(ts.day), "time": ts.strftime("%H:%M")}

    # ── Lazy chunk fetching ─────────────────────────────────────────────

    def _chunk_key_for_indices(self, indices):
        """Build a dotted chunk key from a list of integer indices."""
        return ".".join(str(i) for i in indices)

    def _fetch_chunk(self, var_name, chunk_key):
        """Fetch one or more chunks via a batched Polytope request.

        When batch_dim is set (default: "time"), this looks for other
        uncached indices along that dimension and fetches up to batch_size
        of them in a single Polytope call (e.g. month=1/2/3/.../12).
        Results are split and cached individually.
        """
        spec = self._variables[var_name]
        dims = spec["dims"]
        indices = [int(i) for i in chunk_key.split(".")]

        # Identify the batch dimension position
        batch_pos = None
        if self._batch_dim and self._batch_dim in dims:
            batch_pos = list(dims).index(self._batch_dim)
            if self._batch_dim in self._internal_dims:
                batch_pos = None  # can't batch over an internal dim

        # Collect batch indices: uncached neighbours along batch_dim
        if batch_pos is not None:
            batch_indices = []
            dim_size = self._dim_sizes[self._batch_dim]

            # For time batching, collect uncached neighbours within a range.
            # Hourly stores use batch_days; monthly stores use batch_years.
            if self._batch_dim == "time":
                ref_ts = pd.Timestamp(self._coords["time"][indices[batch_pos]])
                if self._frequency == "hourly":
                    ref_date = ref_ts.normalize()
                    max_date = ref_date + pd.Timedelta(days=self._batch_days - 1)
                    max_total = self._batch_size * self._batch_days
                    for i in range(dim_size):
                        ts_date = pd.Timestamp(self._coords["time"][i]).normalize()
                        if ts_date < ref_date or ts_date > max_date:
                            continue
                        trial = list(indices)
                        trial[batch_pos] = i
                        trial_key = f"{var_name}/{self._chunk_key_for_indices(trial)}"
                        if trial_key not in self._cache:
                            batch_indices.append(i)
                        if len(batch_indices) >= max_total:
                            break
                else:
                    ref_year = ref_ts.year
                    max_year = ref_year + self._batch_years - 1
                    max_total = self._batch_size * self._batch_years
                    for i in range(dim_size):
                        ts_year = pd.Timestamp(self._coords["time"][i]).year
                        if ts_year < ref_year or ts_year > max_year:
                            continue
                        trial = list(indices)
                        trial[batch_pos] = i
                        trial_key = f"{var_name}/{self._chunk_key_for_indices(trial)}"
                        if trial_key not in self._cache:
                            batch_indices.append(i)
                        if len(batch_indices) >= max_total:
                            break
            else:
                for i in range(dim_size):
                    trial = list(indices)
                    trial[batch_pos] = i
                    trial_key = f"{var_name}/{self._chunk_key_for_indices(trial)}"
                    if trial_key not in self._cache:
                        batch_indices.append(i)
                    if len(batch_indices) >= self._batch_size:
                        break

            # Ensure the originally requested index is included
            if indices[batch_pos] not in batch_indices:
                batch_indices.append(indices[batch_pos])
                batch_indices.sort()
        else:
            batch_indices = None

        # Build the Polytope request
        request = dict(self._base_request)
        request["param"] = var_name
        chunk_shape = []

        for dim_i, (dim, idx) in enumerate(zip(dims, indices)):
            size = self._dim_sizes[dim]
            if dim in self._internal_dims:
                chunk_shape.append(size)
                continue
            chunk_shape.append(1)

            if dim == "time" and dim_i == batch_pos and batch_indices is not None:
                # Batched time request
                timestamps = [pd.Timestamp(self._coords["time"][bi])
                              for bi in batch_indices]
                field_map_all = {}
                for ts in timestamps:
                    fm = self._time_to_fields(ts)
                    for f in self._time_fields:
                        field_map_all.setdefault(f, []).append(fm[f])
                for f in self._time_fields:
                    request[f] = "/".join(dict.fromkeys(field_map_all[f]))
            elif dim == "time":
                ts = pd.Timestamp(self._coords["time"][idx])
                fm = self._time_to_fields(ts)
                for f in self._time_fields:
                    request[f] = fm[f]
            elif dim == "model":
                request["model"] = str(self._coords["model"][idx])
            elif dim == "climate":
                request["experiment"] = str(self._coords["climate"][idx])
            elif dim == "level":
                request["levelist"] = str(int(self._coords["level"][idx]))
            else:
                coord_val = self._coords[dim][idx]
                request[dim] = str(coord_val)

        # Resolve address
        address = self._address
        if isinstance(address, dict):
            model = request.get("model", "")
            address = address.get(model, list(address.values())[0])

        n_cells = 1
        for s in chunk_shape:
            n_cells *= s

        n_batch = len(batch_indices) if batch_indices is not None else 1
        if n_batch > 1:
            if self._batch_dim == "time" and batch_indices is not None:
                yrs = set(pd.Timestamp(self._coords["time"][bi]).year
                          for bi in batch_indices)
                yr_info = f" across {len(yrs)} years" if len(yrs) > 1 else ""
            else:
                yr_info = ""
            print(f"  ⚡ batching {n_batch} {self._batch_dim} chunks{yr_info} for {var_name}")

        try:
            import earthkit.data
            self.last_request = {"request": dict(request), "address": address, "collection": self._collection}
            with _quiet_polytope_loggers():
                data = earthkit.data.from_source(
                    "polytope", self._collection, request,
                    address=address, stream=False)

            if batch_indices is not None and n_batch > 1:
                # Split the multi-field response into individual chunks
                self._split_batch(var_name, dims, indices, batch_pos,
                                  batch_indices, chunk_shape, data)
            else:
                values = data.to_numpy().flatten().astype(np.float32)
                if values.size != n_cells:
                    raise ValueError(
                        f"Size mismatch: got {values.size}, expected {n_cells}")
                store_key = f"{var_name}/{chunk_key}"
                self._cache[store_key] = values.tobytes()

        except Exception as e:
            print(f"  ⚠ fetch {var_name} chunk {chunk_key}: {e}")
            # Fill all batch indices with NaN on failure
            if batch_indices is not None:
                for bi in batch_indices:
                    trial = list(indices)
                    trial[batch_pos] = bi
                    key = f"{var_name}/{self._chunk_key_for_indices(trial)}"
                    if key not in self._cache:
                        self._cache[key] = np.full(
                            n_cells, np.nan, dtype=np.float32).tobytes()
            else:
                self._cache[f"{var_name}/{chunk_key}"] = np.full(
                    n_cells, np.nan, dtype=np.float32).tobytes()

        return self._cache.get(f"{var_name}/{chunk_key}",
                               np.full(n_cells, np.nan, dtype=np.float32).tobytes())

    def _split_batch(self, var_name, dims, indices, batch_pos,
                     batch_indices, chunk_shape, data):
        """Split a multi-field earthkit response into per-chunk cache entries."""
        n_cells = 1
        for s in chunk_shape:
            n_cells *= s

        fields = list(data)

        # ── Time dimension: match fields by metadata ────────────────────
        if self._batch_dim == "time" and dims[batch_pos] == "time":
            # Build lookup: time-key tuple → time-axis index
            time_lookup = {}
            if self._frequency == "hourly":
                meta_keys = ("date", "time")
                for bi in batch_indices:
                    ts = pd.Timestamp(self._coords["time"][bi])
                    time_lookup[(ts.strftime("%Y%m%d"), ts.strftime("%H%M"))] = bi
            else:
                meta_keys = ("year", "month")
                for bi in batch_indices:
                    ts = pd.Timestamp(self._coords["time"][bi])
                    time_lookup[(ts.year, ts.month)] = bi

            matched = set()
            for field in fields:
                try:
                    vals = tuple(
                        int(field.metadata(k)) if k in ("year", "month")
                        else str(field.metadata(k)).zfill(4) if k == "time"
                        else str(field.metadata(k))
                        for k in meta_keys)
                except Exception:
                    continue
                key_tuple = vals
                if key_tuple in time_lookup and key_tuple not in matched:
                    bi = time_lookup[key_tuple]
                    matched.add(key_tuple)
                    trial = list(indices)
                    trial[batch_pos] = bi
                    key = f"{var_name}/{self._chunk_key_for_indices(trial)}"
                    values = field.to_numpy().flatten().astype(np.float32)
                    if values.size == n_cells:
                        self._cache[key] = values.tobytes()
                    else:
                        self._cache[key] = np.full(
                            n_cells, np.nan, dtype=np.float32).tobytes()

            # Fill any unmatched batch indices with NaN
            for bi in batch_indices:
                trial = list(indices)
                trial[batch_pos] = bi
                key = f"{var_name}/{self._chunk_key_for_indices(trial)}"
                if key not in self._cache:
                    self._cache[key] = np.full(
                        n_cells, np.nan, dtype=np.float32).tobytes()
            return

        # ── Non-time dimensions: ordered matching ───────────────────────
        if len(fields) == len(batch_indices):
            for bi, field in zip(batch_indices, fields):
                trial = list(indices)
                trial[batch_pos] = bi
                key = f"{var_name}/{self._chunk_key_for_indices(trial)}"
                values = field.to_numpy().flatten().astype(np.float32)
                if values.size == n_cells:
                    self._cache[key] = values.tobytes()
                else:
                    self._cache[key] = np.full(
                        n_cells, np.nan, dtype=np.float32).tobytes()
        else:
            # Fallback: treat entire response as a single concatenated array
            all_values = data.to_numpy().flatten().astype(np.float32)
            expected = n_cells * len(batch_indices)
            if all_values.size == expected:
                for i, bi in enumerate(batch_indices):
                    trial = list(indices)
                    trial[batch_pos] = bi
                    key = f"{var_name}/{self._chunk_key_for_indices(trial)}"
                    chunk = all_values[i * n_cells:(i + 1) * n_cells]
                    self._cache[key] = chunk.tobytes()
            else:
                print(f"  ⚠ batch split: got {all_values.size} values, "
                      f"expected {expected} ({len(batch_indices)} x {n_cells})")
                for bi in batch_indices:
                    trial = list(indices)
                    trial[batch_pos] = bi
                    key = f"{var_name}/{self._chunk_key_for_indices(trial)}"
                    self._cache[key] = np.full(
                        n_cells, np.nan, dtype=np.float32).tobytes()

    # ── MutableMapping interface ────────────────────────────────────────

    def __getitem__(self, key):
        if key in self._kv:
            return self._kv[key]
        if key in self._cache:
            return self._cache[key]
        # Try to parse as a data variable chunk: "var_name/0.1.0"
        if "/" in key:
            parts = key.split("/", 1)
            var_name, chunk_key = parts[0], parts[1]
            if var_name in self._variables and "." in chunk_key:
                return self._fetch_chunk(var_name, chunk_key)
        raise KeyError(key)

    def __setitem__(self, key, value):
        self._kv[key] = value

    def __delitem__(self, key):
        if key in self._kv:
            del self._kv[key]
        elif key in self._cache:
            del self._cache[key]
        else:
            raise KeyError(key)

    def __iter__(self):
        return iter(self._kv)

    def __len__(self):
        return len(self._kv)

    def __contains__(self, key):
        if key in self._kv:
            return True
        # Report data variable chunks as existing so zarr fetches them
        if "/" in key:
            parts = key.split("/", 1)
            if parts[0] in self._variables and "." in parts[1]:
                return True
        return False

    def listdir(self, prefix=""):
        """List entries under a prefix (used by zarr for discovery)."""
        if prefix:
            prefix = prefix.rstrip("/") + "/"
        entries = set()
        for k in self._kv:
            if k.startswith(prefix):
                rest = k[len(prefix):]
                entries.add(rest.split("/")[0])
        return sorted(entries)

    # ── Convenience ─────────────────────────────────────────────────────

    @property
    def batch_years(self):
        """Number of calendar years per batch (monthly stores)."""
        return self._batch_years

    @batch_years.setter
    def batch_years(self, value):
        self._batch_years = int(value)

    @property
    def batch_days(self):
        """Number of calendar days per batch (hourly stores)."""
        return self._batch_days

    @batch_days.setter
    def batch_days(self, value):
        self._batch_days = int(value)

    def open(self):
        """Open this store as an xarray Dataset (lazy — no data fetched).

        The returned Dataset (and its DataArrays) carry a reference to this
        store so that ``.polytope.sel()`` can auto-tune batching.
        """
        import xarray as xr
        ds = xr.open_dataset(self, engine="zarr", consolidated=True)
        ds.attrs["_polytope_store"] = self
        for name in ds.data_vars:
            ds[name].attrs["_polytope_store"] = self
        return ds

    def clear_cache(self):
        """Free cached data chunks."""
        self._cache.clear()

    def __repr__(self):
        dims = ", ".join(f"{k}={v}" for k, v in self._dim_sizes.items())
        nvars = len(self._variables)
        return f"<PolytopeZarrStore {nvars} variables ({dims})>"


# ── xarray accessor: .polytope.sel() ────────────────────────────────────

def _infer_batch_window(store, sel_kwargs):
    """Auto-tune batch_days or batch_years to span the requested time slice.

    For hourly/daily stores (freq "h" or "D"), batch_days is capped to avoid
    exceeding Polytope request-size limits (~500 MB):
      - standard resolution: max 31 days  (~245 MB hourly, ~250 MB daily)
      - high resolution:     max  1 day   (~502 MB hourly)

    For monthly stores, batch_years spans the full requested year range.
    """
    time_arg = sel_kwargs.get("time")
    if store is None or time_arg is None:
        return
    if isinstance(time_arg, slice):
        start = pd.Timestamp(time_arg.start) if time_arg.start else None
        stop = pd.Timestamp(time_arg.stop) if time_arg.stop else None
        if start is not None and stop is not None:
            freq = getattr(store, '_freq', None)
            if freq in ("h", "D"):
                span_days = (stop.normalize() - start.normalize()).days + 1
                res = getattr(store, '_resolution', 'standard')
                max_days = 31 if res == 'standard' else 1
                store.batch_days = min(span_days, max_days)
            else:
                store.batch_years = stop.year - start.year + 1


def _feature_sel(store, var_name, *, bbox=None, polygon=None, point=None,
                 **sel_kwargs):
    """Execute a server-side Polytope feature request.

    Feature requests return data on a lat/lon grid or as point timeseries.
    For **hourly** stores (``clte`` stream), data is returned as GRIB.
    For **monthly** stores (``clmn`` stream), timeseries are returned as JSON.

    Parameters
    ----------
    store : PolytopeZarrStore
    var_name : str
        Variable / param name (e.g. ``"avg_2t"``).
    bbox : (south, west, north, east)
        Bounding-box corners in degrees.  Returns a ``points`` dimension with
        ``latitude``/``longitude`` coordinates.
    polygon : list of (lat, lon)
        Polygon vertices.  Same date handling as *bbox*.
    point : (lat, lon)
        Single location for a timeseries extraction.  Supports date ranges
        via ``time=slice(...)``.
    **sel_kwargs
        ``model``, ``time``, ``level`` — forwarded into the Polytope request.
    """
    import earthkit.data

    if store is None:
        raise ValueError(
            "No PolytopeZarrStore attached — open the dataset via store.open().")

    request = dict(store._base_request)
    # Remove time-specific fields; replaced below
    for f in store._time_fields:
        request.pop(f, None)

    request["param"] = var_name

    if "model" in sel_kwargs:
        request["model"] = str(sel_kwargs["model"])
    if "climate" in sel_kwargs:
        request["experiment"] = str(sel_kwargs["climate"])
    if "level" in sel_kwargs:
        request["levelist"] = str(int(sel_kwargs["level"]))

    freq = getattr(store, "_freq", "MS")
    is_monthly = freq == "MS"

    # ── time handling ─────────────────────────────────────────────────
    time_arg = sel_kwargs.get("time")

    if is_monthly:
        # Monthly (clmn) — use year/month fields
        filter_months = getattr(store, '_filter_months', None)
        if isinstance(time_arg, slice):
            t0 = pd.Timestamp(time_arg.start or store._coords["time"][0])
            t1 = pd.Timestamp(time_arg.stop or store._coords["time"][-1])
            months = pd.date_range(t0, t1, freq="MS")
            if filter_months is not None:
                months = months[months.month.isin(filter_months)]
            years = sorted({m.year for m in months})
            mons = sorted({m.month for m in months})
            request["year"] = "/".join(str(y) for y in years)
            request["month"] = "/".join(str(m) for m in mons)
        elif time_arg is not None:
            ts = pd.Timestamp(time_arg)
            request["year"] = str(ts.year)
            request["month"] = str(ts.month)
        else:
            ts = pd.Timestamp(store._coords["time"][0])
            request["year"] = str(ts.year)
            request["month"] = str(ts.month)
    else:
        # Hourly / daily (clte) — use date/time fields
        filter_hours = getattr(store, '_filter_hours', None)
        if filter_hours is not None:
            _HOURS = "/".join(f"{h:02d}00" for h in sorted(filter_hours))
        else:
            _HOURS = "/".join(f"{h:02d}00" for h in range(24))
        if isinstance(time_arg, slice):
            t0 = pd.Timestamp(time_arg.start or store._coords["time"][0])
            t1 = pd.Timestamp(time_arg.stop or store._coords["time"][-1])
            date_str = f"{t0.strftime('%Y%m%d')}/to/{t1.strftime('%Y%m%d')}"
            time_str = _HOURS if freq == "h" else "0000"
        elif time_arg is not None:
            ts = pd.Timestamp(time_arg)
            date_str = ts.strftime("%Y%m%d")
            time_str = ts.strftime("%H%M")
        else:
            ts = pd.Timestamp(store._coords["time"][0])
            date_str = ts.strftime("%Y%m%d")
            time_str = ts.strftime("%H%M")
        request["date"] = date_str
        request["time"] = time_str

    # ── feature dict ────────────────────────────────────────────────
    if bbox is not None:
        south, west, north, east = bbox
        request["feature"] = {
            "type": "boundingbox",
            "points": [[north, west], [south, east]],
        }
    elif polygon is not None:
        request["feature"] = {
            "type": "polygon",
            "shape": [list(pt) for pt in polygon],
        }
    elif point is not None:
        lat, lon = point
        feature = {
            "type": "timeseries",
            "points": [[lat, lon]],
            "axes": ["latitude", "longitude"],
        }
        # time_axis depends on the stream
        feature["time_axis"] = "month" if is_monthly else "date"
        request["feature"] = feature

    # ── resolve address & fetch ─────────────────────────────────────
    address = store._address
    if isinstance(address, dict):
        m = request.get("model", "")
        address = address.get(m, list(address.values())[0])

    ftype = request["feature"]["type"]
    time_info = request.get("date", f"{request.get('year')}-{request.get('month')}")
    logging.getLogger(__name__).info(
        "%s request for %s (%s)", ftype, var_name, time_info)
    print(f"  🌍 {ftype} request for {var_name} ({time_info})")

    store.last_request = {"request": dict(request), "address": address, "collection": store._collection}
    with _quiet_polytope_loggers():
        data = earthkit.data.from_source(
            "polytope", store._collection, request,
            address=address, stream=False)

    # Timeseries (point) requests return JSON; bbox/polygon return GRIB.
    # Try _json() first for timeseries, fall back to to_xarray().
    if point is not None:
        try:
            return data._json()
        except Exception:
            pass

    ds = data.to_xarray()

    # Clean up GRIB artefacts: squeeze singleton dims like 'number' and
    # 'step', then drop them so users see only meaningful coordinates.
    _grib_singletons = ("number", "step", "steps")
    squeeze = [d for d in _grib_singletons if d in ds.dims and ds.sizes[d] == 1]
    if squeeze:
        ds = ds.squeeze(squeeze).drop_vars(squeeze, errors="ignore")

    # Rename time dimension to 'time' for consistency with _area_sel.
    _dim_renames = {"datetimes": "time", "forecast_reference_time": "time",
                    "valid_time": "time"}
    renames = {k: v for k, v in _dim_renames.items() if k in ds.dims}
    if renames:
        ds = ds.rename(renames)

    # Ensure the time coordinate is proper datetime64 so that partial
    # string indexing (e.g. .sel(time="1990-01")) works in xarray.
    if "time" in ds.coords and not np.issubdtype(ds["time"].dtype, np.datetime64):
        ds["time"] = pd.to_datetime(ds["time"].values, utc=True).tz_localize(None)

    return ds


def _area_sel(store, var_name, *, area, grid=None, **sel_kwargs):
    """Server-side spatial subsetting via MARS *area* + *grid* keywords.

    Unlike feature requests (bbox/polygon/point), this uses the same stream
    as the store (``clmn`` or ``clte``) and always works with Generation 2
    data on both ``lumi`` and ``mn5``.

    Parameters
    ----------
    store : PolytopeZarrStore
    var_name : str
        Variable / param name (e.g. ``"avg_2t"``).
    area : (north, west, south, east)
        Bounding box in MARS order (degrees).
    grid : str or (float, float), optional
        Output grid spacing.  Default ``"0.25/0.25"`` for standard
        resolution,  ``"0.05/0.05"`` for high resolution.
    **sel_kwargs
        ``model`` or ``climate``, ``time``, ``level`` — forwarded into
        the Polytope request.
    """
    import earthkit.data

    if store is None:
        raise ValueError(
            "No PolytopeZarrStore attached — open the dataset via store.open().")

    request = dict(store._base_request)

    # Remove time-specific fields; replaced by date below
    for f in store._time_fields:
        request.pop(f, None)

    request["param"] = var_name

    # ── model / climate ───────────────────────────────────────────────
    if "model" in sel_kwargs:
        request["model"] = str(sel_kwargs["model"])
    if "climate" in sel_kwargs:
        request["experiment"] = str(sel_kwargs["climate"])
    if "level" in sel_kwargs:
        request["levelist"] = str(int(sel_kwargs["level"]))

    # ── area + grid ───────────────────────────────────────────────────
    n, w, s, e = area
    request["area"] = f"{n}/{w}/{s}/{e}"

    if grid is None:
        res = getattr(store, "_resolution", "standard")
        grid = "0.05/0.05" if res == "high" else "0.25/0.25"
    elif isinstance(grid, (list, tuple)):
        grid = f"{grid[0]}/{grid[1]}"
    request["grid"] = str(grid)

    # ── time handling ─────────────────────────────────────────────────
    freq = getattr(store, "_freq", "MS")

    time_arg = sel_kwargs.get("time")
    if freq == "MS":
        # Monthly store: use year/month fields (clmn stream).
        filter_months = getattr(store, '_filter_months', None)
        if isinstance(time_arg, slice):
            t0 = pd.Timestamp(time_arg.start or store._coords["time"][0])
            t1 = pd.Timestamp(time_arg.stop or store._coords["time"][-1])
            months = pd.date_range(t0, t1, freq="MS")
            if filter_months is not None:
                months = months[months.month.isin(filter_months)]
            unique_years = sorted(set(m.year for m in months))
            unique_months = sorted(set(m.month for m in months))
            request["year"] = "/".join(str(y) for y in unique_years)
            request["month"] = "/".join(str(m) for m in unique_months)
        elif time_arg is not None:
            ts = pd.Timestamp(time_arg)
            request["year"] = str(ts.year)
            request["month"] = str(ts.month)
        else:
            ts = pd.Timestamp(store._coords["time"][0])
            request["year"] = str(ts.year)
            request["month"] = str(ts.month)
    else:
        # Hourly / daily store
        filter_hours = getattr(store, '_filter_hours', None)
        if filter_hours is not None:
            _HOURS = "/".join(f"{h:02d}00" for h in sorted(filter_hours))
        else:
            _HOURS = "/".join(f"{h:02d}00" for h in range(24))
        if isinstance(time_arg, slice):
            t0 = pd.Timestamp(time_arg.start or store._coords["time"][0])
            t1 = pd.Timestamp(time_arg.stop or store._coords["time"][-1])
            date_str = f"{t0.strftime('%Y%m%d')}/to/{t1.strftime('%Y%m%d')}"
            time_str = _HOURS if freq == "h" else "0000"
        elif time_arg is not None:
            ts = pd.Timestamp(time_arg)
            date_str = ts.strftime("%Y%m%d")
            time_str = ts.strftime("%H%M")
        else:
            ts = pd.Timestamp(store._coords["time"][0])
            date_str = ts.strftime("%Y%m%d")
            time_str = ts.strftime("%H%M")
        request["date"] = date_str
        request["time"] = time_str

    # ── resolve address & fetch ─────────────────────────────────────
    address = store._address
    if isinstance(address, dict):
        m = request.get("model", "")
        address = address.get(m, list(address.values())[0])

    # Rename GRIB-native dims to friendly names (idempotent if already correct)
    _dim_renames = {
        "forecast_reference_time": "time",
        "valid_time": "time",
    }

    def _rename_dims(ds):
        renames = {k: v for k, v in _dim_renames.items() if k in ds.dims}
        return ds.rename(renames) if renames else ds

    logging.getLogger(__name__).info(
        "area request for %s (grid=%s)", var_name, request["grid"])
    time_info = request.get("date", f"{request.get('year')}-{request.get('month')}")
    print(f"  🌍 area request for {var_name} "
          f"({time_info}, area={request['area']}, grid={request['grid']})")

    store.last_request = {"request": dict(request), "address": address, "collection": store._collection}
    with _quiet_polytope_loggers():
        data = earthkit.data.from_source(
            "polytope", store._collection, request,
            address=address, stream=False)

    # drop_dims="step" avoids the step_timedelta hypercube issue for monthly
    # means (each month has 28-31 day step). This keeps forecast_reference_time
    # as the time axis (the actual month start), not valid_time (which is
    # shifted forward by one month for monthly accumulations).
    return _rename_dims(data.to_xarray(drop_dims="step"))


try:
    import xarray as _xr

    @_xr.register_dataarray_accessor("polytope")
    class _PolytopeDataArray:
        def __init__(self, da):
            self._da = da
            self._store = da.attrs.get("_polytope_store")

        def sel(self, *, bbox=None, polygon=None, point=None,
                area=None, grid=None, **kwargs):
            """Select data, with optional server-side spatial subsetting.

            When *area* is given the request adds MARS ``area`` + ``grid``
            keywords for server-side regridding (works for both ``clmn``
            and ``clte`` streams).

            When *bbox*, *polygon*, or *point* is given the request is
            executed as a Polytope **feature** (``clte`` stream, lat/lon
            grid).  Otherwise delegates to the normal ``.sel()`` with
            automatic batch tuning.
            """
            if area is not None:
                return _area_sel(
                    self._store, self._da.name,
                    area=area, grid=grid, **kwargs)
            if bbox is not None or polygon is not None or point is not None:
                return _feature_sel(
                    self._store, self._da.name,
                    bbox=bbox, polygon=polygon, point=point, **kwargs)
            _infer_batch_window(self._store, kwargs)
            return self._da.sel(**kwargs)

    @_xr.register_dataset_accessor("polytope")
    class _PolytopeDataset:
        def __init__(self, ds):
            self._ds = ds
            self._store = ds.attrs.get("_polytope_store")

        def sel(self, var=None, *, bbox=None, polygon=None, point=None,
                area=None, grid=None, **kwargs):
            """Select data, with optional server-side spatial subsetting.

            *var* can be a single variable name, a ``"/"``-separated string
            (e.g. ``"skt/tcc"``), or a list of names (e.g.
            ``["skt", "tcc"]``).  Lists are joined with ``"/"`` so the
            server returns all requested parameters in one response.

            If *var* is omitted and a spatial keyword (``bbox``, ``polygon``,
            ``point``, or ``area``) is given, all data variables in the
            Dataset are requested (joined with ``"/"``).  This means
            ``ds[["skt", "tcc"]].polytope.sel(bbox=...)`` automatically
            requests both variables.

            When *bbox*, *polygon*, or *point* is given the request is
            executed as a Polytope **feature** (``clte`` stream, lat/lon
            grid).  Otherwise delegates to the normal ``.sel()`` with
            automatic batch tuning.
            """
            if isinstance(var, (list, tuple)):
                var = "/".join(str(v) for v in var)
            if var is None and (bbox is not None or polygon is not None
                                or point is not None or area is not None):
                var = "/".join(self._ds.data_vars)
            if area is not None:
                return _area_sel(
                    self._store, var,
                    area=area, grid=grid, **kwargs)
            if bbox is not None or polygon is not None or point is not None:
                return _feature_sel(
                    self._store, var,
                    bbox=bbox, polygon=polygon, point=point, **kwargs)
            _infer_batch_window(self._store, kwargs)
            result = self._ds.sel(**kwargs)
            return result[var] if var is not None else result

except ImportError:
    pass
