from polytope.api import Client

# You can pass your email and apikey here, or put them in ~/.polytopeapirc (as JSON)
# You can also set POLYTOPE_USER_EMAIL and POLYTOPE_USER_KEY in your environment
client = Client(address='polytope.apps.lumi.ewctest.link', 
                    user_email='<YOUR EMAIL>', 
                    user_key='<YOUR ECMWF API KEY>')

# Optionally revoke previous requests
client.revoke('all')

# This request matches a single parameter of the extremes DT, at 4km resolution
# which began production on 2023-12-11

request = {
    'activity': 'ScenarioMIP',
    'class': 'd1',
    'dataset': 'climate-dt',
    'date': '20200102',
    'experiment': 'SSP3-7.0',
    'expver': '0001',
    'generation': '1',
    'levtype': 'sfc',
    'model': 'IFS-NEMO',
    'param': '134/165/166',
    'realization': '1',
    'resolution': 'standard',
    'stream': 'clte',
    'time': '0100/0200/0300/0400/0500/0600',
    'type': 'fc'
}

# The data will be saved in the current working directory
files = client.retrieve('destination-earth', request)

# If you want to download the data later, you can use the pointer option, which
# will return a URL to the data instead of downloading it.
# url = client.retrieve('destination-earth', request, pointer=True)
