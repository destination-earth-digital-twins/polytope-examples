import earthkit.data
import earthkit.maps
import earthkit.regrid

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

data = earthkit.data.from_source("polytope", "destination-earth", request, address="polytope.apps.lumi.ewctest.link", stream=False)

style = earthkit.maps.Style(
    levels=range(-40, 31, 5),
    units='celsius',
    extend='both',
)

earthkit.maps.quickplot(data, style=style)
