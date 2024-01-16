from polytope.api import Client


client = Client(address='polytope.apps.lumi.ewctest.link', 
                    user_email='<YOUR EMAIL>', 
                    user_key='<YOUR ECMWF API KEY>')

# Optionally revoke previous requests
client.revoke('all')

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
        "param": "31"
    }


files = client.retrieve('destination-earth', request)
