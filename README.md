<h3 align="center">
<img src="./docs/images/Logo_Destination_Earth_Colours.png" width=60%>
</br>

</h3>

- [Polytope Examples for DT Data Access](#polytope-examples-for-dt-data-access)
  - [Access using your Destination Earth Service Platform credentials](#access-using-your-destination-earth-service-platform-credentials)
  - [Access using your ECMWF credentials](#access-using-your-ecmwf-credentials)
  - [Climate-DT Examples](#climate-dt-examples)
  - [Extremes-DT Examples](#extremes-dt-examples)


# Polytope Examples for DT Data Access

This repository describes the process for accessing Destination Earth DT data via the Polytope web service hosted on the LUMI Databridge.


## Access using your Destination Earth Service Platform credentials

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

## Access using your ECMWF credentials

1. Install polytope-client from PyPI:
```
pip install --upgrade polytope-client
```

2. Register for an ECMWF account at ecmwf.int and retrieve your API key from https://api.ecmwf.int/v1/key/

3. Modify the example scripts in this repository to include your email address and API key. Or alternatively see the documentation at https://github.com/ecmwf/polytope-client to see how to set this globally.

## Climate-DT Examples

- [Climate DT Example Directory](climate-dt)
  - [Climate DT python Script](climate-dt/climate-dt.py)
  - [Climate DT notebook example](climate-dt/climate-dt-earthkit-example.ipynb)
  - [Climate DT notebook domain example](climate-dt/climate-dt-earthkit-example-domain.ipynb)
  - [Climate DT notebook healpix regrid](climate-dt/healpix-data.ipynb)

## Extremes-DT Examples

- [Extremes DT Example Directory](extremes-dt)
  - [Extremes DT python Script](extremes-dt/extremes-dt.py)
  - [Extremes DT notebook example](extremes-dt/extremes-dt-earthkit-example.ipynb)
  - [Extremes DT notebook domain example](extremes-dt/extremes-dt-earthkit-example-domain.ipynb)
  - [Extremes DT notebook regrid example](extremes-dt/extremes-dt-earthkit-example-regrid.ipynb)