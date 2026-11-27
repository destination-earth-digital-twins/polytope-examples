#!/usr/bin/env python3
"""
Polytope FULL-FIELD retrieval (no feature) of Extremes DT surface fields,
cropped to a bounding box with "area" and saved as GRIB.
One request per city, per date, per param.

Needs: earthkit-data, and a DestinE Polytope token in ~/.polytopeapirc
"""
import os
import earthkit.data

ADDRESS = "polytope.lumi.apps.dte.destination-earth.eu"
OUTDIR = "/Users/maes/Documents/Repos/MAINTAINED/polytope-examples/tmp"

#              lat_min, lat_max, lon_min, lon_max
CITIES = {
    # "cape_town": (-34.3, -33.5,  18.2,  19.0),
    "chicago":   ( 41.0,  42.5, -89.1, -86.6),
    "naples":    ( 40.4,  41.3,  13.7,  14.9),
    "santiago":  (-34.0, -33.0, -71.2, -70.2),
}

DATES = [
    "20250122", "20260124", "20250208", "20250209", "20260702", "20260714", "20260829", "20260831",
]

PARAMS = ["151", "165", "166", "167", "168"]

TIME = "0000"
STEP = "0/to/96/by/1"

os.makedirs(OUTDIR, exist_ok=True)

for city, (lat_min, lat_max, lon_min, lon_max) in CITIES.items():
    for date in DATES:
            request = {
                "class": "d1",
                "expver": "0001",
                "dataset": "extremes-dt",
                "stream": "oper",
                "type": "fc",
                "levtype": "sfc",
                "time": TIME,
                "step": STEP,
                "param": "151/165/166/167/168",
                "date": date,
                # bounding box, MARS order: North/West/South/East
                "area": f"{lat_max}/{lon_min}/{lat_min}/{lon_max}",
                # optional: interpolate to a regular lat/lon grid instead of the native grid
                # "grid": "0.04/0.04",
            }

            data_file = os.path.join(
                OUTDIR,
                f"extremes-dt_{city}_{date}.grib",
            )
            print(f"--> {city} {date}")

            try:
                data = earthkit.data.from_source(
                    "polytope", "destination-earth", request,
                    address=ADDRESS, stream=False,
                )
                data.to_target("file", data_file)
            except Exception as e:
                print(f"    FAILED: {e}")
                continue

            print(f"    saved {data_file}")