# NextGEMS Data

NextGEMS data is split by date across two simulations:

The historical simulation is stored under `class=ng`, `activity=CMIP6`, `experiment=hist` and an example can be found at [nextGEMS-historical-1990-2020-earthkit-example.ipynb](nextGEMS-historical-1990-2020-earthkit-example.ipynb).

The future projection (SSP3-7.0) simulation was produced before the necessary DGOV work could be carried out. Therefore, this simulation is provided using ClimateDT metadata with `realization=2` . Thus, this is stored under `class=d1`, `dataset=climate-dt`, `activity=ScenarioMIP`, `experiment=SSP3-7.0`, `realization=2` and an example can be found at [nextGEMS-scenario-2020-2050-earthkit-example.ipynb](nextGEMS-scenario-2020-2050-earthkit-example.ipynb).

Further information on the nextGEMS data can be found at [nextGEMS dataset information](https://confluence.ecmwf.int/display/DDCZ/NextGEMS+data+catalogue).