<img src="./docs/images/Logo_Destination_Earth_Colours.png" width=60% >

<br /><br />

# Polytope Examples for DT Data Access

- [Polytope Examples for DT Data Access](#polytope-examples-for-dt-data-access)
  - [Access using your Destination Earth Service Platform credentials](#access-using-your-destination-earth-service-platform-credentials)
  - [Installation](#installation)
    - [Option 1: Conda Instructions](#option-1-conda-instructions)
    - [Option 2: Python Virtual Environment (venv)](#option-2-python-virtual-environment-venv)
  - [Data Locations](#data-locations)
  - [Climate-DT Examples](#climate-dt-examples)
    - [Full Field](#full-field)
    - [Full Field Post-Processing](#full-field-post-processing)
    - [Feature Extraction](#feature-extraction)
    - [Climate DT Explorer](#climate-dt-explorer)
  - [Extremes-DT Examples](#extremes-dt-examples)
  - [On-Demand Extremes-DT Examples](#on-demand-extremes-dt-examples)
  - [NextGEMS Examples](#nextgems-examples)
  - [Polytope Quota Limits for DestinE](#polytope-quota-limits-for-destine)


## Access using your Destination Earth Service Platform credentials

This repository describes the process for accessing Destination Earth DT data via the Polytope web service hosted on the LUMI Databridge.

1. Clone the repo locally or if using polytope via Insula `cd` into the polytope directory.
```
git clone git@github.com:destination-earth-digital-twins/polytope-examples.git
```

2. Install polytope-client from PyPI:
```
pip install --upgrade polytope-client
```

3. Retrieve a token from the Destination Earth Service Platform (DESP) by running the script included in this repository:
```
python desp-authentication.py -u <username> -p <password>
# see --help for more options
```
Or you can run the script without arguments
```
python desp-authentication.py 
# see --help for more options
```
You will then be prompted to enter your username and password if no credentials are found in a config or through environment variables.

You will need some dependencies to run the script, which can be installed using pip:
```
pip install --upgrade lxml conflator
```

The script automatically places your token in `~/.polytopeapirc` where the client will pick it up. The token is a long-lived ("offline_access") token.

3. Run the example scripts in this repository to download data, and customise them as you wish.

## Installation

You can run the notebooks by setting up an appropriate environment using one of the following options:

* Option 1: Use the `environment.yml` file to create a Conda environment, or

* Option 2: Use the `requirements.txt` file to set up a Python virtual environment.

After creating the environment, the provided commands will also register an IPython kernel named earthkit, which you can select when working with the notebooks.

### Option 1: Conda Instructions

```
envname=earthkit
conda create -n $envname -c conda-forge -y python=3.10
conda env update -n $envname -f environment.yml
conda activate $envname

# set earthkit environment to the default used by ipykernels
python3 -m ipykernel install --user --name=$envname
```

### Option 2: Python Virtual Environment (venv)

```
envname=earthkit

# Create a virtual environment
python3 -m venv $envname

# Activate it
source $envname/bin/activate      # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# If using Jupyter notebooks, register your environment as a kernel for ipykernel
python3 -m ipykernel install --user --name=$envname
```

## Data Locations

Data can be found on both LUMI and MN5, to access data on either change the `address` argument in `earthkit.data.from_source()` to either `polytope.mn5.apps.dte.destination-earth.eu` for MN5 or `polytope.lumi.apps.dte.destination-earth.eu` for LUMI.

## Climate-DT Examples

- [Climate DT Example Directory](climate-dt) — see also the [Climate DT README](climate-dt/README.md) for full details on available data and variables.

```
climate-dt/
├── explorer/                    # Browse the Climate DT data portfolio lazily without downloading upfront
├── feature-extraction/          # Extract specific spatial or temporal features from the datacube
├── full-field/                  # Retrieve and visualise complete global or regional fields
└── full-field-post-processing/  # Apply server-side or client-side post-processing to retrieved fields
```

### Full Field

Polytope allows users to download complete global or regional fields from the Climate DT. Full field requests return GRIB data using standard MARS keys. Server-side options such as `grid` (interpolation to a target grid) and `area` (geographic subselection) can be applied at request time to reduce data volume before download. See the [Polytope full fields documentation](https://polytope.readthedocs.io/en/latest/Service/Full_fields/) for more details.

- [Climate DT python Script](climate-dt/full-field/climate-dt.py)
- [Climate DT notebook example](climate-dt/full-field/climate-dt-earthkit-example.ipynb)
- [Climate DT notebook domain example](climate-dt/full-field/climate-dt-earthkit-example-domain.ipynb)
- [Climate DT notebook area example](climate-dt/full-field/climate-dt-earthkit-area-example.ipynb)
- [Climate DT notebook area of interest example](climate-dt/full-field/climate-dt-earthkit-aoi-example.ipynb)
- [Climate DT notebook grid example](climate-dt/full-field/climate-dt-earthkit-grid-example.ipynb)
- [Climate DT notebook healpix data](climate-dt/full-field/climate-dt-healpix-data.ipynb)
- [Climate DT notebook healpix ocean](climate-dt/full-field/climate-dt-healpix-ocean-example.ipynb)
- [Climate DT notebook HighResMIP example](climate-dt/full-field/climate-dt-highresmip-earthkit-example.ipynb)
- [Climate DT monthly means notebook example](climate-dt/full-field/climate-dt-earthkit-monthly-mean-example.ipynb)

### Full Field Post-Processing

These notebooks demonstrate server-side and client-side post-processing of retrieved fields, including grid interpolation, and format conversion.

- [Climate DT notebook healpix interpolation](climate-dt/full-field-post-processing/climate-dt-earthkit-healpix-interpolate.ipynb)
- [Climate DT notebook serverside interpolation](climate-dt/full-field-post-processing/climate-dt-earthkit-serverside-interpolation.ipynb)
- [Climate DT notebook GeoTIFF export](climate-dt/full-field-post-processing/climate-dt-earthkit-geotiff.ipynb)

### Feature Extraction

Polytope feature extraction reads only the user-requested data rather than whole fields, which significantly reduces I/O. Features are n-dimensional shapes (polytopes) cut from the datacube — such as time series at a point, vertical profiles, trajectories, bounding boxes, and polygons. See the [Polytope feature extraction documentation](https://polytope.readthedocs.io/en/latest/Service/Features/feature/) for more details.

- [Climate DT notebook feature extraction timeseries](climate-dt/feature-extraction/climate-dt-earthkit-fe-timeseries.ipynb)
- [Climate DT notebook feature extraction trajectory](climate-dt/feature-extraction/climate-dt-earthkit-fe-trajectory.ipynb)
- [Climate DT notebook feature extraction vertical profile](climate-dt/feature-extraction/climate-dt-earthkit-fe-verticalprofile.ipynb)
- [Climate DT notebook feature extraction bounding box](climate-dt/feature-extraction/climate-dt-earthkit-fe-boundingbox.ipynb)
- [Climate DT notebook feature extraction country](climate-dt/feature-extraction/climate-dt-earthkit-fe-country.ipynb)
- [Climate DT notebook feature extraction polygon](climate-dt/feature-extraction/climate-dt-earthkit-fe-polygon.ipynb)
- [Climate DT notebook feature extraction pcolormesh](climate-dt/feature-extraction/climate-dt-earthkit-fe-pcolormesh.ipynb)
- [Climate DT notebook feature extraction nudging story](climate-dt/feature-extraction/climate-dt-earthkit-fe-story-nudging.ipynb)

### Climate DT Explorer

The Climate DT Explorer notebooks allow you to lazily browse the full Climate DT data portfolio without downloading any data upfront. They expose the datacube as a virtual [zarr](https://zarr.readthedocs.io/) store backed by Polytope, so you can inspect available variables, perform climate change analysis over multi-decadal periods, and generate ready-to-use request snippets — only fetching the data chunks you actually need.

- [Climate DT lazy portfolio browser (monthly)](climate-dt/explorer/03_lazy_browse_portfolio.ipynb)
- [Climate DT lazy portfolio browser (hourly)](climate-dt/explorer/04_lazy_browse_portfolio_hourly.ipynb)
- [Climate DT climate change analysis](climate-dt/explorer/02_climate_change_destine.ipynb)
- [Climate DT variable lookup](climate-dt/explorer/05_variable_lookup.ipynb)

## Extremes-DT Examples

- [Extremes DT Example Directory](extremes-dt)
  - **Full Field**
    - [Extremes DT python Script](extremes-dt/full-field/extremes-dt.py)
    - [Extremes DT notebook example](extremes-dt/full-field/extremes-dt-earthkit-example.ipynb)
    - [Extremes DT notebook domain example](extremes-dt/full-field/extremes-dt-earthkit-example-domain.ipynb)
    - [Extremes DT notebook H3 example](extremes-dt/full-field/extremes-dt-earthkit-example-H3.ipynb)
  - **Full Field Post-Processing**
    - [Extremes DT notebook regrid example](extremes-dt/full-field-post-processing/extremes-dt-earthkit-example-regrid.ipynb)
    - [Extremes DT notebook serverside interpolation](extremes-dt/full-field-post-processing/extremes-dt-earthkit-serverside-interpolation.ipynb)
  - **Feature Extraction**
    - [Extremes DT notebook feature extraction timeseries](extremes-dt/feature-extraction/extremes-dt-earthkit-example-fe-timeseries.ipynb)
    - [Extremes DT notebook feature extraction trajectory](extremes-dt/feature-extraction/extremes-dt-earthkit-example-fe-trajectory.ipynb)
    - [Extremes DT notebook feature extraction 4D trajectory](extremes-dt/feature-extraction/extremes-dt-earthkit-example-fe-trajectory4d.ipynb)
    - [Extremes DT notebook feature extraction vertical profile](extremes-dt/feature-extraction/extremes-dt-earthkit-example-fe-verticalprofile.ipynb)
    - [Extremes DT notebook feature extraction bounding box](extremes-dt/feature-extraction/extremes-dt-earthkit-example-fe-boundingbox.ipynb)
    - [Extremes DT notebook feature extraction country](extremes-dt/feature-extraction/extremes-dt-earthkit-example-fe-country.ipynb)
    - [Extremes DT notebook feature extraction polygon](extremes-dt/feature-extraction/extremes-dt-earthkit-example-fe-polygon.ipynb)
    - [Extremes DT notebook feature extraction pcolormesh](extremes-dt/feature-extraction/extremes-dt-earthkit-example-fe-pcolormesh.ipynb)
    - [Extremes DT notebook feature extraction polygon using H3](extremes-dt/feature-extraction/extremes-dt-earthkit-example-fe-polygon-H3.ipynb)
    - [Extremes DT notebook feature extraction wave](extremes-dt/feature-extraction/extremes-dt-earthkit-example-fe-wave.ipynb)

## On-Demand Extremes-DT Examples

- [On-Demand Extremes DT Example Directory](on-demand-extremes-dt)
  - **Full Field**
    - [On-Demand Extremes DT python Script](on-demand-extremes-dt/full-field/on-demand-extremes-dt-example.py)
    - [On-Demand Extremes DT notebook example](on-demand-extremes-dt/full-field/on-demand-extremes-dt-example.ipynb)
  - **Feature Extraction**
    - [On-Demand Extremes DT feature extraction country example](on-demand-extremes-dt/feature-extraction/on-demand-country-fe-example.ipynb)
    - [On-Demand Extremes DT feature extraction trajectory example](on-demand-extremes-dt/feature-extraction/on-demand-trajectory-fe-example.ipynb)
    - [On-Demand Extremes DT feature extraction timeseries example](on-demand-extremes-dt/feature-extraction/on-demand-extremes-dt-timeseries-fe-example.ipynb)
    - [On-Demand Extremes DT feature extraction vertical profile example](on-demand-extremes-dt/feature-extraction/on-demand-extremes-dt-vertical-profile-fe-example.ipynb)

## NextGEMS Examples

- [NextGEMS Example Directory](nextgems)
  - **Full Field**
    - [NextGEMS historical 1990-2020 notebook](nextgems/full-field/nextGEMS-historical-earthkit-example.ipynb)
    - [NextGEMS scenario 2020-2050 notebook](nextgems/full-field/nextGEMS-scenario-earthkit-example.ipynb)
  - **Feature Extraction**
    - [NextGEMS historical feature extraction timeseries](nextgems/feature-extraction/nextGEMS-historical-fe-timeseries-example.ipynb)
    - [NextGEMS historical feature extraction trajectory](nextgems/feature-extraction/nextGEMS-historical-fe-trajectory-example.ipynb)
    - [NextGEMS historical feature extraction vertical profile](nextgems/feature-extraction/nextGEMS-historical-fe-verticalprofile-example.ipynb)
    - [NextGEMS historical feature extraction bounding box](nextgems/feature-extraction/nextGEMS-historical-fe-boundingbox-example.ipynb)
    - [NextGEMS historical feature extraction country](nextgems/feature-extraction/nextGEMS-historical-fe-country-example.ipynb)

## Polytope Documentation

General information about the Polytope Web service and how to use it can be found here: https://polytope.readthedocs.io/en/latest/Service/Full_fields/

## Polytope Quota Limits for DestinE

To ensure system stability and fair usage, the following operational limits are enforced:

- **API Rate Limit:** Up to 50 requests per second. This limit may be adjusted based on system usage.
- **Concurrent Operations Limit:** A maximum of 5 download requests can be active at the same time.

Please plan your usage accordingly to avoid interruptions.
