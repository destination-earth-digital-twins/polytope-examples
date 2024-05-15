from polytope.api import Client

# You can pass your email and apikey here, or put them in ~/.polytopeapirc (as JSON)
# You can also set POLYTOPE_USER_EMAIL and POLYTOPE_USER_KEY in your environment
client = Client(
    address="polytope.lumi.apps.dte.destination-earth.eu",
    # user_email='<YOUR EMAIL>',
    # user_key='<YOUR ECMWF API KEY>' or '<YOUR_DESP_KEY>'
)

# Optionally revoke previous requests
client.revoke("all")

# This request matches a single parameter of the extremes DT, at 4km resolution
# which began production on 2023-12-11

request = {
    "class": "rd",
    "expver": "i7yv",
    "stream": "oper",
    "date": "20231211/to/20231220",
    "time": "0000",
    "type": "fc",
    "levtype": "sfc",
    "step": "0",
    "param": "31",
}

# The data will be saved in the current working directory
files = client.retrieve("destination-earth", request)

# If you want to download the data later, you can use the pointer option, which
# will return a URL to the data instead of downloading it.
# url = client.retrieve('destination-earth', request, pointer=True)
