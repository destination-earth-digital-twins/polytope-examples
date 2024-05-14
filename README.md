<h3 align="center">
<img src="./docs/images/Logo_Destination_Earth_White.png" width=60%>
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

- [Climate DT Example Directory](Climate-DT)
  - [Climate DT python Script](Climate-DT/climate-dt.py)
  - [Climate DT notebook example](Climate-DT/climate-dt-earthkit-example.ipynb)
  - [Climate DT notebook domain example](Climate-DT/climate-dt-earthkit-example-domain.ipynb)
  - [Climate DT healpix regrid](Climate-DT/healpix-data.ipynb)

## Extremes-DT Examples

- [Extremes DT Example Directory](Extremes-DT)
  - [Extremes DT python Script](Extremes-DT/xxtremes-dt.py)
  - [Extremes DT notebook example](Extremes-DT/extremes-dt-earthkit-example.ipynb)
  - [Extremes DT notebook domain example](Extremes-DT/extremes-dt-earthkit-example-domain.ipynb)