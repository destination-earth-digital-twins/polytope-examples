import io
import re

from setuptools import find_packages, setup

setup(
    name="polytope-examples",
    # version=__version__,
    description="""This repository describes the process for accessing Destination Earth DT data via the Polytope web service hosted on the LUMI Databridge.
 """,
    long_description="",
    url="https://github.com/destination-earth-digital-twins/polytope-examples",
    author="ECMWF",
    author_email="James.Hawkes@ecmwf.int, Adam.Warde@ecmwf.int, Tiago.Quintino@ecmwf.int",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
)
