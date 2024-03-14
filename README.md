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

The script automatically places your token in `~/.polytopeapirc` where the client will pick it up.

3. Run the example scripts in this repostory to download data, and customise them as you wish.

## Access using your ECMWF credentials

To run the examples in this repository, you simply need to:

1. Install polytope-client from PyPI:
```
pip install --upgrade polytope-client
```

2. Register for an ECMWF account* at ecmwf.int and retrieve your API key from https://api.ecmwf.int/v1/key/

3. Modify the example scripts in this repository to include your email address and API key. Or alternatively see the documentation at https://github.com/ecmwf/polytope-client to see how to set this globally.
