"""
DestinE Climate DT Generation 2 data portfolio.

Catalogue of all variables available from the Climate DT
Generation 2 monthly (clmn) and hourly (clte) streams, organised by levtype.

Based on:
  clmn: https://confluence.ecmwf.int/display/DDCZ/DestinE+ClimateDT+Phase+2+clmn+Parameters
  clte: https://confluence.ecmwf.int/display/DDCZ/DestinE+ClimateDT+Phase+2+clte+Parameters

Usage:
    from destine_portfolio import PORTFOLIO_GEN2_CLMN, PORTFOLIO_GEN2_CLTE
    lt = PORTFOLIO_GEN2_CLMN["sfc"]  # dict with levtype, levels, variables
    lt["levtype"]                 # "sfc"
    lt["variables"]["avg_2t"]     # {"dims": D_SFC, "long_name": ..., "units": ...}
"""

# ── Dimension tuples ────────────────────────────────────────────────
D_SFC = ("model", "time", "cell")
D_LEV = ("model", "time", "level", "cell")
D_O2D = ("model", "time", "cell")

# Storyline dims: outer dimension is "climate" (experiment) instead of "model"
D_STORY_SFC = ("climate", "time", "cell")
D_STORY_LEV = ("climate", "time", "level", "cell")

# ── Surface (sfc) ──────────────────────────────────────────────────
SFC_VARIABLES = {
    # Single-level / surface atmosphere (instant params in clte)
    "avg_tclw":     {"dims": D_SFC, "long_name": "Time-mean total column liquid water",             "units": "kg m**-2"},
    "avg_tciw":     {"dims": D_SFC, "long_name": "Time-mean total column cloud ice water",          "units": "kg m**-2"},
    "avg_sp":       {"dims": D_SFC, "long_name": "Time-mean surface pressure",                      "units": "Pa"},
    "avg_tcw":      {"dims": D_SFC, "long_name": "Time-mean total column water",                    "units": "kg m**-2"},
    "avg_tcwv":     {"dims": D_SFC, "long_name": "Time-mean total column water vapour",             "units": "kg m**-2"},
    "avg_sd":       {"dims": D_SFC, "long_name": "Time-mean snow depth water equivalent",           "units": "kg m**-2"},
    "avg_msl":      {"dims": D_SFC, "long_name": "Time-mean mean sea level pressure",               "units": "Pa"},
    "avg_tcc":      {"dims": D_SFC, "long_name": "Time-mean total cloud cover",                     "units": "%"},
    "avg_10u":      {"dims": D_SFC, "long_name": "Time-mean 10 metre U wind component",             "units": "m s**-1"},
    "avg_10v":      {"dims": D_SFC, "long_name": "Time-mean 10 metre V wind component",             "units": "m s**-1"},
    "avg_2t":       {"dims": D_SFC, "long_name": "Time-mean 2 metre temperature",                   "units": "K"},
    "avg_2d":       {"dims": D_SFC, "long_name": "Time-mean 2 metre dewpoint temperature",          "units": "K"},
    "avg_10ws":     {"dims": D_SFC, "long_name": "Time-mean 10 metre wind speed",                   "units": "m s**-1"},
    "avg_skt":      {"dims": D_SFC, "long_name": "Time-mean skin temperature",                      "units": "K"},
    # Hourly-mean params in clte
    "avg_surfror":  {"dims": D_SFC, "long_name": "Time-mean surface runoff rate",                   "units": "kg m**-2 s**-1"},
    "avg_ssurfror": {"dims": D_SFC, "long_name": "Time-mean sub-surface runoff rate",               "units": "kg m**-2 s**-1"},
    "avg_tsrwe":    {"dims": D_SFC, "long_name": "Time-mean total snowfall rate water equivalent",  "units": "kg m**-2 s**-1"},
    "avg_ishf":     {"dims": D_SFC, "long_name": "Time-mean surface sensible heat flux",            "units": "W m**-2"},
    "avg_slhtf":    {"dims": D_SFC, "long_name": "Time-mean surface latent heat flux",              "units": "W m**-2"},
    "avg_sdswrf":   {"dims": D_SFC, "long_name": "Time-mean surface downward short-wave radiation flux",  "units": "W m**-2"},
    "avg_sdlwrf":   {"dims": D_SFC, "long_name": "Time-mean surface downward long-wave radiation flux",   "units": "W m**-2"},
    "avg_snswrf":   {"dims": D_SFC, "long_name": "Time-mean surface net short-wave radiation flux",       "units": "W m**-2"},
    "avg_snlwrf":   {"dims": D_SFC, "long_name": "Time-mean surface net long-wave radiation flux",        "units": "W m**-2"},
    "avg_tnswrf":   {"dims": D_SFC, "long_name": "Time-mean top net short-wave radiation flux",     "units": "W m**-2"},
    "avg_tnlwrf":   {"dims": D_SFC, "long_name": "Time-mean top net long-wave radiation flux",      "units": "W m**-2"},
    "avg_iews":     {"dims": D_SFC, "long_name": "Time-mean eastward turbulent surface stress",     "units": "N m**-2"},
    "avg_inss":     {"dims": D_SFC, "long_name": "Time-mean northward turbulent surface stress",    "units": "N m**-2"},
    "avg_ie":       {"dims": D_SFC, "long_name": "Time-mean moisture flux",                         "units": "kg m**-2 s**-1"},
    "avg_tnswrfcs": {"dims": D_SFC, "long_name": "Time-mean top net short-wave radiation flux, clear sky",     "units": "W m**-2"},
    "avg_tnlwrfcs": {"dims": D_SFC, "long_name": "Time-mean top net long-wave radiation flux, clear sky",      "units": "W m**-2"},
    "avg_snswrfcs": {"dims": D_SFC, "long_name": "Time-mean surface net short-wave radiation flux, clear sky", "units": "W m**-2"},
    "avg_snlwrfcs": {"dims": D_SFC, "long_name": "Time-mean surface net long-wave radiation flux, clear sky",  "units": "W m**-2"},
    "avg_tdswrf":   {"dims": D_SFC, "long_name": "Time-mean top downward short-wave radiation flux","units": "W m**-2"},
    "avg_tprate":   {"dims": D_SFC, "long_name": "Time-mean total precipitation rate",              "units": "kg m**-2 s**-1"},
}

# ── Pressure levels (pl) ───────────────────────────────────────────
# 19 levels: 1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10, 5, 1
PL_VARIABLES = {
    "avg_pv":   {"dims": D_LEV, "long_name": "Time-mean potential vorticity",                "units": "K m**2 kg**-1 s**-1"},
    "avg_z":    {"dims": D_LEV, "long_name": "Time-mean geopotential",                       "units": "m**2 s**-2"},
    "avg_t":    {"dims": D_LEV, "long_name": "Time-mean temperature",                        "units": "K"},
    "avg_u":    {"dims": D_LEV, "long_name": "Time-mean U component of wind",                "units": "m s**-1"},
    "avg_v":    {"dims": D_LEV, "long_name": "Time-mean V component of wind",                "units": "m s**-1"},
    "avg_q":    {"dims": D_LEV, "long_name": "Time-mean specific humidity",                  "units": "kg kg**-1"},
    "avg_w":    {"dims": D_LEV, "long_name": "Time-mean vertical velocity",                  "units": "Pa s**-1"},
    "avg_r":    {"dims": D_LEV, "long_name": "Time-mean relative humidity",                  "units": "%"},
    "avg_clwc": {"dims": D_LEV, "long_name": "Time-mean specific cloud liquid water content","units": "kg kg**-1"},
}

# ── Height levels (hl) ─────────────────────────────────────────────
# Height levels >10 m only (to avoid overlap with sfc 10u/10v/2t).
# IFS-only in Phase 1 and Phase 2.
HL_VARIABLES = {
    "avg_u": {"dims": D_LEV, "long_name": "Time-mean U component of wind", "units": "m s**-1"},
    "avg_v": {"dims": D_LEV, "long_name": "Time-mean V component of wind", "units": "m s**-1"},
}

# ── Soil / snow levels (sol) ────────────────────────────────────────
# Snow: 5 levels (1–5), IFS-only
# Soil: 4 levels for IFS (1–4), 5 for ICON (1–5)
SOL_VARIABLES = {
    "avg_sd":  {"dims": D_LEV, "long_name": "Time-mean snow depth water equivalent",   "units": "kg m**-2"},
    "avg_vsw": {"dims": D_LEV, "long_name": "Time-mean volumetric soil moisture",      "units": "m**3 m**-3"},
}

# ── 2-D ocean / sea ice (o2d) ──────────────────────────────────────
O2D_VARIABLES = {
    # Sea ice
    "avg_sithick": {"dims": D_O2D, "long_name": "Time-mean sea ice thickness",                      "units": "m"},
    "avg_siconc":  {"dims": D_O2D, "long_name": "Time-mean sea ice area fraction",                  "units": "Fraction"},
    "avg_siue":    {"dims": D_O2D, "long_name": "Time-mean eastward sea ice velocity",               "units": "m s**-1"},
    "avg_sivn":    {"dims": D_O2D, "long_name": "Time-mean northward sea ice velocity",              "units": "m s**-1"},
    "avg_sivol":   {"dims": D_O2D, "long_name": "Time-mean sea ice volume per unit area",            "units": "m**3 m**-2"},
    "avg_snvol":   {"dims": D_O2D, "long_name": "Time-mean snow volume over sea ice per unit area",  "units": "m**3 m**-2"},
    # Ocean surface
    "avg_sos":       {"dims": D_O2D, "long_name": "Time-mean sea surface practical salinity",                              "units": "g kg**-1"},
    "avg_tos":       {"dims": D_O2D, "long_name": "Time-mean sea surface temperature",                                    "units": "K"},
    "avg_hc300m":    {"dims": D_O2D, "long_name": "Time-mean vertically-integrated heat content in the upper 300 m",      "units": "J m**-2"},
    "avg_hc700m":    {"dims": D_O2D, "long_name": "Time-mean vertically-integrated heat content in the upper 700 m",      "units": "J m**-2"},
    "avg_hcbtm":     {"dims": D_O2D, "long_name": "Time-mean total column heat content",                                  "units": "J m**-2"},
    "avg_zos":       {"dims": D_O2D, "long_name": "Time-mean sea surface height",                                         "units": "m"},
}

# ── 3-D ocean (o3d) ────────────────────────────────────────────────
# Level count varies by model: ICON 72, FESOM 69, NEMO 75.
# We use 1–75 (NEMO max); out-of-range levels return NaN.
O3D_VARIABLES = {
    "avg_so":     {"dims": D_LEV, "long_name": "Time-mean sea water practical salinity",       "units": "g kg**-1"},
    "avg_thetao": {"dims": D_LEV, "long_name": "Time-mean sea water potential temperature",    "units": "K"},
    "avg_von":    {"dims": D_LEV, "long_name": "Time-mean northward sea water velocity",      "units": "m s**-1"},
    "avg_uoe":    {"dims": D_LEV, "long_name": "Time-mean eastward sea water velocity",       "units": "m s**-1"},
    "avg_wo":     {"dims": D_LEV, "long_name": "Time-mean upward sea water velocity",         "units": "m s**-1"},
}

# ── Master catalogue ───────────────────────────────────────────────
PORTFOLIO_GEN2_CLMN = {
    "sfc": {
        "levtype": "sfc",
        "freq": "MS",
        "levels": None,
        "variables": SFC_VARIABLES,
    },
    "pl": {
        "levtype": "pl",
        "freq": "MS",
        "levels": [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10, 5, 1],
        "variables": PL_VARIABLES,
    },
    "hl": {
        "levtype": "hl",
        "freq": "MS",
        "levels": [100],  # 100 m above ground; IFS-only
        "variables": HL_VARIABLES,
    },
    "sol": {
        "levtype": "sol",
        "freq": "MS",
        "levels": [1, 2, 3, 4, 5],  # snow uses 1-5; soil uses 1-4 (IFS) / 1-5 (ICON)
        "variables": SOL_VARIABLES,
    },
    "o2d": {
        "levtype": "o2d",
        "freq": "MS",
        "levels": None,
        "variables": O2D_VARIABLES,
    },
    "o3d": {
        "levtype": "o3d",
        "freq": "MS",
        "levels": list(range(1, 76)),  # NEMO 75, ICON 72, FESOM 69 — padded to max
        "variables": O3D_VARIABLES,
    },
}

# Backwards-compatible alias
PORTFOLIO_GEN2 = PORTFOLIO_GEN2_CLMN


# ════════════════════════════════════════════════════════════════════
#  CLTE (hourly) stream — Climate DT Generation 2
# ════════════════════════════════════════════════════════════════════
# Instantaneous and hourly-mean atmosphere fields; daily-mean ocean/ice.
# SFC instant + PL/HL/SOL use standard ECMWF shortNames (no avg_ prefix).
# SFC hourly-mean fluxes and ocean (o2d/o3d) keep the avg_ prefix.

# ── Surface (sfc) — instantaneous atmosphere (hourly) ──────────────
CLTE_SFC_INST_VARIABLES = {
    "tclw":  {"dims": D_SFC, "long_name": "Total column cloud liquid water",      "units": "kg m**-2"},
    "tciw":  {"dims": D_SFC, "long_name": "Total column cloud ice water",         "units": "kg m**-2"},
    "sp":    {"dims": D_SFC, "long_name": "Surface pressure",                     "units": "Pa"},
    "tcw":   {"dims": D_SFC, "long_name": "Total column water",                   "units": "kg m**-2"},
    "tcwv":  {"dims": D_SFC, "long_name": "Total column water vapour",            "units": "kg m**-2"},
    "sd":    {"dims": D_SFC, "long_name": "Snow depth water equivalent",          "units": "kg m**-2"},
    "msl":   {"dims": D_SFC, "long_name": "Mean sea level pressure",              "units": "Pa"},
    "tcc":   {"dims": D_SFC, "long_name": "Total cloud cover",                    "units": "%"},
    "10u":   {"dims": D_SFC, "long_name": "10 metre U wind component",            "units": "m s**-1"},
    "10v":   {"dims": D_SFC, "long_name": "10 metre V wind component",            "units": "m s**-1"},
    "2t":    {"dims": D_SFC, "long_name": "2 metre temperature",                  "units": "K"},
    "2d":    {"dims": D_SFC, "long_name": "2 metre dewpoint temperature",         "units": "K"},
    "10si":  {"dims": D_SFC, "long_name": "10 metre wind speed",                  "units": "m s**-1"},
    "skt":   {"dims": D_SFC, "long_name": "Skin temperature",                     "units": "K"},
}

# ── Surface (sfc) — hourly-mean fluxes/radiation ───────────────────
CLTE_SFC_MEAN_VARIABLES = {
    "avg_surfror":  {"dims": D_SFC, "long_name": "Time-mean surface runoff rate",                                          "units": "kg m**-2 s**-1"},
    "avg_ssurfror": {"dims": D_SFC, "long_name": "Time-mean sub-surface runoff rate",                                      "units": "kg m**-2 s**-1"},
    "avg_tsrwe":    {"dims": D_SFC, "long_name": "Time-mean total snowfall rate water equivalent",                         "units": "kg m**-2 s**-1"},
    "avg_ishf":     {"dims": D_SFC, "long_name": "Time-mean surface sensible heat flux",                                   "units": "W m**-2"},
    "avg_slhtf":    {"dims": D_SFC, "long_name": "Time-mean surface latent heat flux",                                     "units": "W m**-2"},
    "avg_sdswrf":   {"dims": D_SFC, "long_name": "Time-mean surface downward short-wave radiation flux",                   "units": "W m**-2"},
    "avg_sdlwrf":   {"dims": D_SFC, "long_name": "Time-mean surface downward long-wave radiation flux",                    "units": "W m**-2"},
    "avg_snswrf":   {"dims": D_SFC, "long_name": "Time-mean surface net short-wave radiation flux",                        "units": "W m**-2"},
    "avg_snlwrf":   {"dims": D_SFC, "long_name": "Time-mean surface net long-wave radiation flux",                         "units": "W m**-2"},
    "avg_tnswrf":   {"dims": D_SFC, "long_name": "Time-mean top net short-wave radiation flux",                            "units": "W m**-2"},
    "avg_tnlwrf":   {"dims": D_SFC, "long_name": "Time-mean top net long-wave radiation flux",                             "units": "W m**-2"},
    "avg_iews":     {"dims": D_SFC, "long_name": "Time-mean eastward turbulent surface stress",                            "units": "N m**-2"},
    "avg_inss":     {"dims": D_SFC, "long_name": "Time-mean northward turbulent surface stress",                           "units": "N m**-2"},
    "avg_ie":       {"dims": D_SFC, "long_name": "Time-mean moisture flux",                                                "units": "kg m**-2 s**-1"},
    "avg_tnswrfcs": {"dims": D_SFC, "long_name": "Time-mean top net short-wave radiation flux, clear sky",                 "units": "W m**-2"},
    "avg_tnlwrfcs": {"dims": D_SFC, "long_name": "Time-mean top net long-wave radiation flux, clear sky",                  "units": "W m**-2"},
    "avg_snswrfcs": {"dims": D_SFC, "long_name": "Time-mean surface net short-wave radiation flux, clear sky",             "units": "W m**-2"},
    "avg_snlwrfcs": {"dims": D_SFC, "long_name": "Time-mean surface net long-wave radiation flux, clear sky",              "units": "W m**-2"},
    "avg_tdswrf":   {"dims": D_SFC, "long_name": "Time-mean top downward short-wave radiation flux",                       "units": "W m**-2"},
    "avg_tprate":   {"dims": D_SFC, "long_name": "Time-mean total precipitation rate",                                     "units": "kg m**-2 s**-1"},
}

CLTE_SFC_VARIABLES = {**CLTE_SFC_INST_VARIABLES, **CLTE_SFC_MEAN_VARIABLES}

# ── Pressure levels (pl) — hourly instantaneous ────────────────────
CLTE_PL_VARIABLES = {
    "pv":   {"dims": D_LEV, "long_name": "Potential vorticity",                "units": "K m**2 kg**-1 s**-1"},
    "z":    {"dims": D_LEV, "long_name": "Geopotential",                       "units": "m**2 s**-2"},
    "t":    {"dims": D_LEV, "long_name": "Temperature",                        "units": "K"},
    "u":    {"dims": D_LEV, "long_name": "U component of wind",                "units": "m s**-1"},
    "v":    {"dims": D_LEV, "long_name": "V component of wind",                "units": "m s**-1"},
    "q":    {"dims": D_LEV, "long_name": "Specific humidity",                  "units": "kg kg**-1"},
    "w":    {"dims": D_LEV, "long_name": "Vertical velocity",                  "units": "Pa s**-1"},
    "r":    {"dims": D_LEV, "long_name": "Relative humidity",                  "units": "%"},
    "clwc": {"dims": D_LEV, "long_name": "Specific cloud liquid water content","units": "kg kg**-1"},
}

# ── Height levels (hl) — hourly instantaneous, IFS-only ────────────
CLTE_HL_VARIABLES = {
    "u": {"dims": D_LEV, "long_name": "U component of wind", "units": "m s**-1"},
    "v": {"dims": D_LEV, "long_name": "V component of wind", "units": "m s**-1"},
}

# ── Soil / snow levels (sol) — hourly instantaneous ─────────────────
CLTE_SOL_VARIABLES = {
    "sd":  {"dims": D_LEV, "long_name": "Snow depth water equivalent",    "units": "kg m**-2"},
    "vsw": {"dims": D_LEV, "long_name": "Volumetric soil moisture",       "units": "m**3 m**-3"},
}

# ── 2-D ocean / sea ice (o2d) — daily mean ─────────────────────────
CLTE_O2D_VARIABLES = {
    # Sea ice
    "avg_sithick": {"dims": D_O2D, "long_name": "Time-mean sea ice thickness",                      "units": "m"},
    "avg_siconc":  {"dims": D_O2D, "long_name": "Time-mean sea ice area fraction",                  "units": "Fraction"},
    "avg_siue":    {"dims": D_O2D, "long_name": "Time-mean eastward sea ice velocity",               "units": "m s**-1"},
    "avg_sivn":    {"dims": D_O2D, "long_name": "Time-mean northward sea ice velocity",              "units": "m s**-1"},
    "avg_sivol":   {"dims": D_O2D, "long_name": "Time-mean sea ice volume per unit area",            "units": "m**3 m**-2"},
    "avg_snvol":   {"dims": D_O2D, "long_name": "Time-mean snow volume over sea ice per unit area",  "units": "m**3 m**-2"},
    # Ocean surface
    "avg_sos":   {"dims": D_O2D, "long_name": "Time-mean sea surface practical salinity",                         "units": "g kg**-1"},
    "avg_tos":   {"dims": D_O2D, "long_name": "Time-mean sea surface temperature",                                "units": "K"},
    "avg_hc300m":{"dims": D_O2D, "long_name": "Time-mean vertically-integrated heat content in the upper 300 m",  "units": "J m**-2"},
    "avg_hc700m":{"dims": D_O2D, "long_name": "Time-mean vertically-integrated heat content in the upper 700 m",  "units": "J m**-2"},
    "avg_hcbtm": {"dims": D_O2D, "long_name": "Time-mean total column heat content",                              "units": "J m**-2"},
    "avg_zos":   {"dims": D_O2D, "long_name": "Time-mean sea surface height",                                     "units": "m"},
}

# ── 3-D ocean (o3d) — daily mean ───────────────────────────────────
CLTE_O3D_VARIABLES = {
    "avg_so":     {"dims": D_LEV, "long_name": "Time-mean sea water practical salinity",       "units": "g kg**-1"},
    "avg_thetao": {"dims": D_LEV, "long_name": "Time-mean sea water potential temperature",    "units": "K"},
    "avg_von":    {"dims": D_LEV, "long_name": "Time-mean northward sea water velocity",      "units": "m s**-1"},
    "avg_uoe":    {"dims": D_LEV, "long_name": "Time-mean eastward sea water velocity",       "units": "m s**-1"},
    "avg_wo":     {"dims": D_LEV, "long_name": "Time-mean upward sea water velocity",         "units": "m s**-1"},
}

# ── Master catalogue — CLTE ────────────────────────────────────────
PORTFOLIO_GEN2_CLTE = {
    "sfc": {
        "levtype": "sfc",
        "freq": "h",
        "levels": None,
        "variables": CLTE_SFC_VARIABLES,
    },
    "pl": {
        "levtype": "pl",
        "freq": "h",
        "levels": [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10, 5, 1],
        "variables": CLTE_PL_VARIABLES,
    },
    "hl": {
        "levtype": "hl",
        "freq": "h",
        "levels": [100],  # 100 m above ground; IFS-only
        "variables": CLTE_HL_VARIABLES,
    },
    "sol": {
        "levtype": "sol",
        "freq": "h",
        "levels": [1, 2, 3, 4, 5],
        "variables": CLTE_SOL_VARIABLES,
    },
    "o2d": {
        "levtype": "o2d",
        "freq": "D",
        "levels": None,
        "variables": CLTE_O2D_VARIABLES,
    },
    "o3d": {
        "levtype": "o3d",
        "freq": "D",
        "levels": list(range(1, 76)),
        "variables": CLTE_O3D_VARIABLES,
    },
}


# ════════════════════════════════════════════════════════════════════
#  STORYLINE portfolio — CLTE variables with "climate" dimension
# ════════════════════════════════════════════════════════════════════
# Storyline simulations (activity "story-nudging") are IFS-FESOM only.
# The outer dimension is "climate" (experiment names like cont/hist/Tplus2.0K)
# instead of "model".

def _story_vars(clte_vars, dim_sfc, dim_lev):
    """Re-dim clte variables: replace model→climate in dim tuples."""
    out = {}
    for name, spec in clte_vars.items():
        new_spec = dict(spec)
        if spec["dims"] in (D_SFC, D_O2D):
            new_spec["dims"] = dim_sfc
        elif spec["dims"] == D_LEV:
            new_spec["dims"] = dim_lev
        out[name] = new_spec
    return out

PORTFOLIO_GEN2_STORYLINE = {
    "sfc": {
        "levtype": "sfc",
        "freq": "h",
        "levels": None,
        "variables": _story_vars(CLTE_SFC_VARIABLES, D_STORY_SFC, D_STORY_LEV),
    },
    "pl": {
        "levtype": "pl",
        "freq": "h",
        "levels": [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10, 5, 1],
        "variables": _story_vars(CLTE_PL_VARIABLES, D_STORY_SFC, D_STORY_LEV),
    },
    "hl": {
        "levtype": "hl",
        "freq": "h",
        "levels": [100],
        "variables": _story_vars(CLTE_HL_VARIABLES, D_STORY_SFC, D_STORY_LEV),
    },
    "sol": {
        "levtype": "sol",
        "freq": "h",
        "levels": [1, 2, 3, 4, 5],
        "variables": {
            **_story_vars(CLTE_SOL_VARIABLES, D_STORY_SFC, D_STORY_LEV),
            "sot": {"dims": D_STORY_LEV, "long_name": "Soil temperature", "units": "K"},
        },
    },
    "o2d": {
        "levtype": "o2d",
        "freq": "D",
        "levels": None,
        "variables": _story_vars(CLTE_O2D_VARIABLES, D_STORY_SFC, D_STORY_LEV),
    },
    "o3d": {
        "levtype": "o3d",
        "freq": "D",
        "levels": list(range(1, 76)),
        "variables": _story_vars(CLTE_O3D_VARIABLES, D_STORY_SFC, D_STORY_LEV),
    },
}


# ════════════════════════════════════════════════════════════════════
#  Variable lookup helpers
# ════════════════════════════════════════════════════════════════════

# Time ranges per experiment (inclusive).
# Monthly stores use year ranges; hourly/daily stores use full timestamps.
_EXPERIMENT_TIME_RANGES = {
    "cont":      {"start": "1990-01-01", "end": "1999-12-31"},   # min 10 years from 1990
    "hist":      {"start": "1990-01-01", "end": "2014-12-31"},
    "SSP3-7.0":  {"start": "2015-01-01", "end": "2049-12-31"},
}

# Per-model end year for the SSP3-7.0 scenario (inclusive).
# Update these values as new simulation data becomes available.
_MODEL_ENDYEAR_RELEASE = {
    "IFS-NEMO":  2049,
    "IFS-FESOM": 2049,
    "ICON":      2040,
}

_STORYLINE_TIME_RANGES = {
    "cont":      {"start": "2017-01-01", "end": "2024-12-31"},
    "hist":      {"start": "2017-01-01", "end": "2024-12-31"},
    "Tplus2.0K": {"start": "2017-01-01", "end": "2024-12-31"},
}

_STREAMS = {
    "clmn": {
        "portfolio": PORTFOLIO_GEN2_CLMN,
        "label": "monthly",
        "models": ["IFS-NEMO", "IFS-FESOM", "ICON"],
        "nside": {"standard": 128, "high": 1024},
        "experiments": ["cont", "hist", "SSP3-7.0"],
        "time_ranges": _EXPERIMENT_TIME_RANGES,
    },
    "clte": {
        "portfolio": PORTFOLIO_GEN2_CLTE,
        "label": "hourly",
        "models": ["IFS-NEMO", "IFS-FESOM", "ICON"],
        "nside": {"standard": 128, "high": 1024},
        "experiments": ["cont", "hist", "SSP3-7.0"],
        "time_ranges": _EXPERIMENT_TIME_RANGES,
    },
    "storyline": {
        "portfolio": PORTFOLIO_GEN2_STORYLINE,
        "label": "hourly (storyline)",
        "models": ["IFS-FESOM"],
        "nside": {"standard": 128, "high": 512},
        "experiments": ["cont", "hist", "Tplus2.0K"],
        "time_ranges": _STORYLINE_TIME_RANGES,
    },
}


def find_variable(query=None):
    """Search the Climate DT portfolio for a variable.

    Parameters
    ----------
    query : str, optional
        A shortName (e.g. ``"2t"``, ``"avg_2t"``), or a substring to
        match against long_name (e.g. ``"temperature"``).
        Fuzzy: ``"2t"`` also matches ``"avg_2t"`` and vice-versa.
        If omitted, returns the full catalogue.

    Returns
    -------
    pandas.DataFrame
        One row per stream × levtype match, with columns:
        stream, shortName, levtype, freq, access, long_name, units,
        models, nside.
    """
    import pandas as pd

    rows = []
    for stream_name, info in _STREAMS.items():
        portfolio = info["portfolio"]
        for lt_key, lt_spec in portfolio.items():
            for var_name, var_spec in lt_spec["variables"].items():
                if query is not None:
                    q = query.lower()
                    bare = var_name.removeprefix("avg_")
                    hit = (q == var_name.lower()
                           or q == bare.lower()
                           or q == f"avg_{bare}".lower()
                           or q in var_spec["long_name"].lower())
                    if not hit:
                        continue
                freq_label = {"MS": "monthly", "h": "hourly", "D": "daily"}
                rows.append({
                    "stream/activity": stream_name,
                    "shortName": var_name,
                    "levtype": lt_spec["levtype"],
                    "freq": freq_label.get(lt_spec["freq"], lt_spec["freq"]),
                    "access": f'{info["label"]}/{lt_spec["levtype"]}',
                    "long_name": var_spec["long_name"],
                    "units": var_spec["units"],
                    "models": ", ".join(info["models"]),
                    "experiments": ", ".join(info["experiments"]),
                    "nside": str(info["nside"]),
                })

    df = pd.DataFrame(rows)
    if len(df):
        df = df.sort_values(["shortName", "stream/activity", "levtype"]).reset_index(drop=True)
    return df


def access_snippet(query, stream="clte", experiment=None, model=None):
    """Print a ready-to-copy ``from_climate_dt()`` call for a variable.

    Parameters
    ----------
    query : str
        A shortName (e.g. ``"2t"``). Fuzzy matching as in ``find_variable``.
    stream : str
        ``"clmn"``, ``"clte"``, or ``"storyline"``.
    experiment : str or list of str, optional
        Override the experiment(s). Defaults to ``"hist"`` for clmn/clte,
        or ``["cont", "hist", "Tplus2.0K"]`` for storyline.
    model : str, optional
        Override the model. Defaults to ``"IFS-NEMO"`` for clmn/clte,
        ``"IFS-FESOM"`` for storyline.
    """
    df = find_variable(query)
    df = df[df["stream/activity"] == stream]
    if df.empty:
        print(f"No match for '{query}' in stream '{stream}'.")
        return

    # Prefer exact shortName match over long_name substring hits,
    # and prefer levtypes available for all models (pl > hl, o2d > o3d, etc.)
    _LT_PRIO = {"sfc": 0, "pl": 1, "o2d": 2, "o3d": 3, "sol": 4, "hl": 5}
    exact = df[df["shortName"].str.lower().isin([query.lower(), f"avg_{query.lower()}"])]
    candidates = exact if not exact.empty else df
    row = candidates.sort_values(
        "levtype", key=lambda s: s.map(_LT_PRIO).fillna(9)
    ).iloc[0]
    info = _STREAMS[stream]

    freq_kw = "monthly" if row["freq"] == "monthly" else "hourly"
    models = [model] if model else info["models"]
    models_str = ", ".join(f'"{m}"' for m in models)

    # Resolve experiment and its time range
    if stream == "storyline":
        exp = experiment or info["experiments"]
        exp_key = exp[0] if isinstance(exp, list) else exp
    else:
        exp = experiment or "hist"
        exp_key = exp

    tr = info["time_ranges"].get(exp_key, {"start": "1990-01-01", "end": "1990-12-31"})
    start_year = int(tr["start"][:4])
    end_year = int(tr["end"][:4])

    # Clamp end year per model for SSP3-7.0 based on data availability
    icon_note = False
    if exp_key == "SSP3-7.0" and stream != "storyline":
        model_end_years = [_MODEL_ENDYEAR_RELEASE.get(m, end_year) for m in models]
        if len(models) == 1:
            # Single model: use that model's end year
            end_year = model_end_years[0]
        else:
            # Multiple models: use the maximum (ICON returns NaN beyond its limit)
            if min(model_end_years) < max(model_end_years):
                icon_note = True
            end_year = max(model_end_years)
        tr = dict(tr)  # copy to avoid mutating the original
        tr["end"] = f"{end_year}-12-31"

    lines = [
        "from polytope_zarr import PolytopeZarrStore\n",
    ]

    if icon_note:
        lines.append(f"# Note: ICON returns NaN after {_MODEL_ENDYEAR_RELEASE['ICON']}; "
                     f"IFS-NEMO/IFS-FESOM available to {_MODEL_ENDYEAR_RELEASE['IFS-NEMO']}")

    lines.append("store = PolytopeZarrStore.from_climate_dt(")
    lines.append(f'    models=[{models_str}],')

    if stream == "storyline":
        lines.append(f'    experiment={exp},')
        lines.append(f'    activity="story-nudging",')
    else:
        lines.append(f'    experiment="{exp}",')

    lines.append(f'    levtype="{row["levtype"]}",')
    lines.append(f'    frequency="{freq_kw}",')

    if freq_kw == "monthly":
        lines.append(f'    years=range({start_year}, {end_year + 1}),')
    else:
        lines.append(f'    start_date="{tr["start"]}T00:00:00",')
        lines.append(f'    end_date="{tr["end"]}T23:00:00",')

    lines.append('    resolution="standard",')
    lines.append(")")
    lines.append("")
    lines.append("ds = store.open()")

    # Quick-look plot of the first timestep
    var = row["shortName"]
    first_model = models[0]
    if freq_kw == "monthly":
        first_time = f"{start_year}-01-01"
    else:
        first_time = f"{tr['start']}T00:00"

    sel_dim = "climate" if stream == "storyline" else "model"

    # Check if this levtype has vertical levels
    lt_key = row["levtype"]
    portfolio = info["portfolio"]
    levels = portfolio[lt_key]["levels"]

    if stream == "storyline":
        first_sel_val = exp[0] if isinstance(exp, list) else exp
    else:
        first_sel_val = first_model

    sel_parts = f'{sel_dim}="{first_sel_val}", time="{first_time}"'
    if levels is not None:
        first_level = levels[0]
        sel_parts += f", level={first_level}"

    lines.append("")
    lines.append("import healpy as hp")
    lines.append(f'field = ds["{var}"].sel({sel_parts})')
    title_label = first_sel_val if stream == "storyline" else first_model
    lines.append(f'hp.mollview(field.values, title="{title_label} — {var} — {first_time}",')
    lines.append(f'           unit="{row["units"]}", cmap="RdYlBu_r", nest=True, flip="geo")')

    code = "\n".join(lines)
    try:
        from IPython.display import display, Markdown
        display(Markdown(f"```python\n{code}\n```"))
    except ImportError:
        print(code)
