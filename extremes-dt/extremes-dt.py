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

# This request retrieves a parameter from the extremes-dt dataset, for the previous week

request = {
    "class": "d1",
    "expver": "0001",
    "dataset": "extremes-dt",
    "stream": "oper",
    "date": "-7/to/-1",
    "time": "0000",
    "type": "fc",
    "levtype": "sfc",
    "step": "0/to/120",
    "param": "31"
}

# The data will be saved in the current working directory
files = client.retrieve("destination-earth", request)

# If you want to download the data later, you can use the pointer option, which
# will return a URL to the data instead of downloading it.
# url = client.retrieve('destination-earth', request, pointer=True)
