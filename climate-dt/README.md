# Climate DT Examples

Example notebooks for accessing and analysing **DestinE Climate DT** data via [Polytope](https://github.com/ecmwf/polytope-client) and [earthkit](https://github.com/ecmwf/earthkit-data).

Supports the three Climate DT models **IFS-NEMO**, **IFS-FESOM**, and **ICON**.

## Repository structure

```
climate-dt/
├── feature-extraction/          # Extract specific spatial/temporal features
├── full-field/                  # Retrieve and visualise full fields
├── full-field-post-processing/  # Post-process full fields (interpolation, GeoTIFF, AI)
├── explorer/                    # Browse the Climate DT portfolio lazily
├── data/                        # Cached sample data files
├── environment.yml              # Conda environment definition
└── requirements.txt             # pip requirements with version pins
```

## Quick start

### 1. Set up the Python environment

**Option A: conda**

```bash
conda env create -f environment.yml
conda activate destine-analysis
```

**Option B: venv**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> **Note:** `polytope_zarr.py` (used by the `climate-dt-explorer` notebooks) requires **zarr v2**
> (`zarr>=2.18,<3`) and `numcodecs<0.16`. These pins are included in `requirements.txt`.
> Installing zarr v3 will cause a `TypeError: Unsupported type for store_like` error.

If you are running on the **DESP**, the packages may already be available. Ensure your kernel has
`earthkit-data` and `healpy` installed and that `zarr<3` is pinned.

### 2. Authenticate

Before running any notebook you need a valid [DESP account](https://platform.destine.eu/) with
upgraded Climate DT access. Run **`polytope-explorer/01_key_destine_once.ipynb`** once to store
your API key in `~/.polytopeapirc` if you have not already done this using the `desp-authentication.py` script. All other notebooks will pick it up automatically.

---

## Notebooks

### `feature-extraction/`

Notebooks that extract specific spatial or temporal features from Climate DT data.

| Notebook | Description |
|----------|-------------|
| `climate-dt-earthkit-fe-timeseries.ipynb` | Extract and plot a time series at a single point |
| `climate-dt-earthkit-fe-trajectory.ipynb` | Extract data along a trajectory |
| `climate-dt-earthkit-fe-verticalprofile.ipynb` | Extract a vertical profile at a location |
| `climate-dt-earthkit-fe-boundingbox.ipynb` | Extract data within a bounding box |
| `climate-dt-earthkit-fe-polygon.ipynb` | Extract data within an arbitrary polygon |
| `climate-dt-earthkit-fe-country.ipynb` | Cut out data for a specific country |
| `climate-dt-earthkit-fe-pcolormesh.ipynb` | Plot extracted data using pcolormesh and contourf |
| `climate-dt-earthkit-fe-story-nudging.ipynb` | Time series extraction for storyline/nudging experiments |

### `full-field/`

Notebooks that retrieve and visualise complete global or regional fields.

| Notebook | Description |
|----------|-------------|
| `climate-dt-earthkit-example.ipynb` | Basic full-field retrieval and plotting with earthkit |
| `climate-dt-earthkit-example-domain.ipynb` | Full-field retrieval plotted on a regional domain |
| `climate-dt-earthkit-area-example.ipynb` | Server-side interpolation to a regular grid, then area extraction |
| `climate-dt-earthkit-aoi-example.ipynb` | Area-of-interest cut-out with earthkit-transforms |
| `climate-dt-earthkit-grid-example.ipynb` | Server-side interpolation to a supported target grid |
| `climate-dt-earthkit-MN5-example.ipynb` | Full-field retrieval from Mare Nostrum 5 |
| `climate-dt-earthkit-MN5-monthly-mean-example.ipynb` | Monthly mean (`clmn` stream) retrieval from MN5 |
| `climate-dt-healpix-data.ipynb` | Working with native HEALPix grid data |
| `climate-dt-healpix-ocean-example.ipynb` | Ocean data on the HEALPix grid |
| `climate-dt-highresmip-earthkit-example.ipynb` | HighResMIP data retrieval and plotting |
| `climate-dt.py` | Python script equivalent of the basic retrieval example |

### `full-field-post-processing/`

Notebooks that apply post-processing steps to retrieved fields.

| Notebook | Description |
|----------|-------------|
| `climate-dt-earthkit-serverside-interpolation.ipynb` | Server-side interpolation to a regular grid and area extraction |
| `climate-dt-earthkit-healpix-interpolate.ipynb` | Server-side interpolation to a HEALPix grid |
| `climate-dt-earthkit-geotiff.ipynb` | Convert full fields and bounding-box extractions to GeoTIFF |
| `climate-dt-train-ai-timeseries-polytope.ipynb` | Train an XGBoost model on a Polytope-sourced time series |

### `explorer/`

Notebooks for lazily browsing the full Climate DT data portfolio without downloading data upfront.

| Notebook | Description |
|----------|-------------|
| `01_key_destine_once.ipynb` | One-time DESP authentication — stores API key in `~/.polytopeapirc` |
| `02_climate_change_destine.ipynb` | Climate change analysis: 30-year mean differences between historical and SSP3-7.0 |
| `03_lazy_browse_portfolio.ipynb` | Lazy xarray Dataset over the full monthly (`clmn`) portfolio |
| `04_lazy_browse_portfolio_hourly.ipynb` | Lazy xarray Dataset over the hourly (`clte`) portfolio |
| `05_variable_lookup.ipynb` | Search variables by name/keyword and generate `from_climate_dt()` code snippets |
| `destine_climate_helpers.py` | Helper module for Polytope requests, caching, and chunked year iteration |
| `destine_portfolio.py` | Variable catalogue (clmn: 65 vars, clte: 64 vars) and lookup helpers |
| `polytope_zarr.py` | Virtual zarr store backed by Polytope for lazy chunk fetching |

---

## Dataset details

### `climate-dt-explorer/02_climate_change_destine.ipynb` — configuration options

All options are set in the configuration cell of the notebook:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `PARAM` | `'avg_2t'` | Variable to analyse (e.g. `'avg_2t'`, `'235043'` for precip) |
| `MODELS` | `['IFS-NEMO', 'IFS-FESOM']` | Models to include (add `'ICON'` when available) |
| `RESOLUTION` | `'standard'` | Grid resolution (`'standard'` = H128, `'high'` = H1024) |
| `HIST_YEARS` | `range(1990, 2015)` | Historical period |
| `HIST_EXPERIMENT` | `'hist'` | Historical experiment name |
| `SCEN_YEARS` | `range(2015, 2050)` | Scenario period |
| `SCEN_EXPERIMENT` | `'SSP3-7.0'` | Scenario experiment name |
| `STORE_DATA` | `True` | Cache downloaded data as per-year NetCDF files |
| `DATA_DIR` | `'./data'` | Directory for cached data |

When `STORE_DATA = True`, downloaded data are saved as individual NetCDF files per year and re-running the notebook skips years that are already cached:

```
data/
├── IFS-NEMO/
│   ├── hist/clmn/standard/
│   │   ├── avg_2t_1990.nc
│   │   ├── avg_2t_1991.nc
│   │   └── ...
│   └── SSP3-7.0/clmn/standard/
│       ├── avg_2t_2015.nc
│       └── ...
├── IFS-FESOM/
│   └── ...
└── ICON/
    └── ...
```

### CLTE (hourly) stream — variable summary

The hourly (`clte`) stream provides 64 variables across 6 levtypes.
Atmosphere fields (sfc, pl, hl, sol) are hourly; ocean/ice (o2d, o3d) are daily means.

| levtype | # vars | time res | description |
|---------|--------|----------|-------------|
| sfc (instant) | 14 | hourly | Standard shortNames (no `avg_` prefix): `tclw`, `tciw`, `sp`, `tcw`, `tcwv`, `sd`, `msl`, `tcc`, `10u`, `10v`, `2t`, `2d`, `10si`, `skt` |
| sfc (hourly mean) | 20 | hourly | Fluxes / radiation — keep `avg_` prefix: `avg_surfror` … `avg_tprate` |
| pl | 9 | hourly | 19 pressure levels (1000–1 hPa): `pv`, `z`, `t`, `u`, `v`, `q`, `w`, `r`, `clwc` |
| hl | 2 | hourly | 100 m only, IFS-only: `u`, `v` |
| sol | 2 | hourly | Snow (1–5) + soil (1–4/5): `sd`, `vsw` |
| o2d | 12 | daily | Sea ice (6) + ocean surface (6), `avg_` prefix |
| o3d | 5 | daily | 3-D ocean (up to 75 levels), `avg_` prefix |

> **Key difference from clmn:** SFC instantaneous, PL, HL, and SOL params use standard ECMWF shortNames
> (e.g. `2t` instead of `avg_2t`). Also `10si` instead of `10ws` for 10 m wind speed.
> Ocean/ice fields remain `avg_`-prefixed (daily means).

> **Note:** For multi-level levtypes (`pl`, `hl`, `sol`, `o3d`) select a specific level when plotting, e.g.
> ```python
> ds["avg_t"].sel(model="ICON", time="2014-06-01", level=850)
> ```
> Without `.sel(level=...)`, xarray will try to fetch data for **all** levels at once.

The full variable catalogue is defined in `climate-dt-explorer/destine_portfolio.py` (clmn: 65 vars, clte: 64 vars across all levtypes). Use `climate-dt-explorer/05_variable_lookup.ipynb` to search by name or keyword and generate ready-to-copy `from_climate_dt()` code snippets. You can also inspect the last Polytope request sent by the store for reuse with `earthkit.data` directly:

```python
r = store.last_request
data = earthkit.data.from_source("polytope", r["collection"], r["request"],
                                 address=r["address"], stream=False)
field = data.to_numpy()
```

---

## Requirements

- Python ≥ 3.10
- A valid [DESP account](https://platform.destine.eu/) with upgraded Climate DT access
- Python packages listed in [`requirements.txt`](requirements.txt) or [`environment.yml`](environment.yml)
