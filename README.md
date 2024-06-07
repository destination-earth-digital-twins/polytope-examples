<h3 align="center">
<img src="./docs/images/Logo_Destination_Earth_Colours.png" width=60%>
</br>

</h3>

- [Polytope Examples for DT Data Access](#polytope-examples-for-dt-data-access)
  - [Access using your Destination Earth Service Platform credentials](#access-using-your-destination-earth-service-platform-credentials)
  - [Access using your ECMWF credentials](#access-using-your-ecmwf-credentials)
  - [Installation](#installation)
  - [Climate-DT Examples](#climate-dt-examples)
  - [Extremes-DT Examples](#extremes-dt-examples)


# Polytope Examples for DT Data Access

This repository describes the process for accessing Destination Earth DT data via the Polytope web service hosted on the LUMI Databridge.

1. Install polytope-client from PyPI:
```
pip install --upgrade polytope-client
```

2. Retrieve a token from the Destination Earth Service Platform (DESP) by running the script included in this repository:
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

3. Run the example scripts in this repostory to download data, and customise them as you wish.

## Installation 

To run the notebooks you can use the `environment.yml` file provided to create a conda environment that can run the notebooks. The following commands create the environment and also create an ipykernel called `earthkit` than can be used in notebooks if selected.

```
envname=earthkit
conda create -n $envname -c conda-forge -y python=3.10
conda env update -n $envname -f environment.yml
conda activate $envname

# set earthkit environment to the default used by ipykernels
python3 -m ipykernel install --user --name=$envname
```

## Climate-DT Examples

- [Climate DT Example Directory](climate-dt)
  - [Climate DT python Script](climate-dt/climate-dt.py)
  - [Climate DT notebook example](climate-dt/climate-dt-earthkit-example.ipynb)
  - [Climate DT notebook domain example](climate-dt/climate-dt-earthkit-example-domain.ipynb)
  - [Climate DT notebook healpix regrid](climate-dt/healpix-data.ipynb)
  - [Climate DT notebook healpix ocean](climate-dt/climate-dt-healpix-ocean-example.ipynb)

## Extremes-DT Examples

- [Extremes DT Example Directory](extremes-dt)
  - [Extremes DT python Script](extremes-dt/extremes-dt.py)
  - [Extremes DT notebook example](extremes-dt/extremes-dt-earthkit-example.ipynb)
  - [Extremes DT notebook domain example](extremes-dt/extremes-dt-earthkit-example-domain.ipynb)
  - [Extremes DT notebook regrid example](extremes-dt/extremes-dt-earthkit-example-regrid.ipynb)
