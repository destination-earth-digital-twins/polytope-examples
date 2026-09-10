"""
Look-up of the Polytope server that serves each DestinE Climate DT simulation.

Simulations are spread over several Polytope bridges (mn5, lumi, leo).  Rather
than hard-coding the address next to every request, the mapping lives in
``simulations.yaml`` next to this module and is resolved here from the four
keys that identify a simulation: model, activity, experiment and generation.

Usage:
    from destine_registry import resolve_address, infer_activity

    resolve_address("IFS-NEMO", experiment="hist")                 # -> mn5
    resolve_address("IFS-NEMO", experiment="hist", generation=1)   # -> leo
    resolve_address("IFS-FESOM", experiment="Tplus2.0K",
                    activity="story-nudging")                      # -> mn5

To add a simulation, edit ``simulations.yaml`` — no code change needed.
"""

from functools import lru_cache
from pathlib import Path

import yaml

REGISTRY_PATH = Path(__file__).with_name("simulations.yaml")

# Query keys that identify a simulation, in the order shown in error messages.
SELECTORS = ("model", "activity", "experiment", "generation")

_ALLOWED_RULE_KEYS = set(SELECTORS) | {"site", "notes"}

DEFAULT_GENERATION = 2


# ── Loading ─────────────────────────────────────────────────────────────

@lru_cache(maxsize=None)
def load_registry(path=None):
    """Load and validate the registry.  Cached per path."""
    path = Path(path) if path is not None else REGISTRY_PATH
    with open(path) as f:
        registry = yaml.safe_load(f)

    sites = registry.get("sites") or {}
    rules = registry.get("simulations") or []
    if not sites:
        raise ValueError(f"{path}: no 'sites' defined")
    if not rules:
        raise ValueError(f"{path}: no 'simulations' defined")

    for i, rule in enumerate(rules):
        unknown = set(rule) - _ALLOWED_RULE_KEYS
        if unknown:
            raise ValueError(
                f"{path}: simulations[{i}] has unknown key(s) "
                f"{sorted(unknown)}; allowed keys are "
                f"{sorted(_ALLOWED_RULE_KEYS)}"
            )
        if "site" not in rule:
            raise ValueError(f"{path}: simulations[{i}] has no 'site'")
        if rule["site"] not in sites:
            raise ValueError(
                f"{path}: simulations[{i}] refers to unknown site "
                f"{rule['site']!r}; known sites are {sorted(sites)}"
            )

    return registry


def known_sites(path=None):
    """Return the {site name: address} mapping from the registry."""
    return dict(load_registry(path)["sites"])


# ── Normalisation ───────────────────────────────────────────────────────

def _norm(value):
    """Case-insensitive comparison key; None stays None (matches anything)."""
    return None if value is None else str(value).strip().lower()


def canonical_experiment(experiment, path=None):
    """Map an experiment spelling onto the one used in the registry.

    e.g. ``"ssp370"`` -> ``"SSP3-7.0"``.  Unknown names are returned
    unchanged so new experiments work before an alias is added.
    """
    if experiment is None:
        return None
    aliases = load_registry(path).get("experiment_aliases") or {}
    lookup = {_norm(k): v for k, v in aliases.items()}
    return lookup.get(_norm(experiment), experiment)


def infer_activity(experiment, path=None):
    """Infer the activity implied by an experiment name.

    Raises ValueError for experiments the registry does not know about —
    add them to ``activity_by_experiment:`` in ``simulations.yaml``.
    """
    experiment = canonical_experiment(experiment, path)
    by_experiment = load_registry(path).get("activity_by_experiment") or {}
    lookup = {_norm(k): v for k, v in by_experiment.items()}
    try:
        return lookup[_norm(experiment)]
    except KeyError:
        raise ValueError(
            f"Cannot infer the activity of experiment {experiment!r}. "
            f"Known experiments: {sorted(by_experiment)}. "
            f"Pass activity= explicitly, or add the experiment to "
            f"'activity_by_experiment' in {REGISTRY_PATH.name}."
        ) from None


# ── Resolution ──────────────────────────────────────────────────────────

def _selector_matches(rule_value, query_value):
    """True when a single rule selector accepts the queried value."""
    if rule_value is None or query_value is None:
        return True  # an absent selector, or an unconstrained query, matches
    accepted = rule_value if isinstance(rule_value, (list, tuple)) else [rule_value]
    return _norm(query_value) in {_norm(v) for v in accepted}


def find_rules(model, experiment=None, activity=None,
               generation=DEFAULT_GENERATION, path=None):
    """Return every registry rule matching the query, in file order."""
    registry = load_registry(path)
    query = {
        "model": model,
        "activity": activity,
        "experiment": canonical_experiment(experiment, path),
        "generation": generation,
    }
    return [rule for rule in registry["simulations"]
            if all(_selector_matches(rule.get(key), value)
                   for key, value in query.items())]


def resolve_address(model, experiment=None, activity=None,
                    generation=DEFAULT_GENERATION, path=None):
    """Return the Polytope address serving a simulation.

    Parameters
    ----------
    model : str
        Model name, e.g. "ICON", "IFS-FESOM", "IFS-NEMO".
    experiment : str, optional
        Experiment name, e.g. "hist", "cont", "SSP3-7.0", "Tplus2.0K".
        Alternative spellings listed in the registry are accepted.
    activity : str, optional
        "baseline", "projections" or "story-nudging".  Inferred from
        *experiment* when omitted — pass it explicitly for storylines,
        whose "hist"/"cont" experiments otherwise look like baseline runs.
    generation : int or str, optional
        Climate DT generation.  Default 2.

    Raises
    ------
    LookupError
        When no registry rule covers the simulation, or when the query is
        so underspecified that it spans simulations on several servers.
    """
    if activity is None and experiment is not None:
        activity = infer_activity(experiment, path)

    keys = {"model": model, "activity": activity,
            "experiment": experiment, "generation": generation}
    query = " ".join(f"{k}={v!r}" for k, v in keys.items())
    sites = load_registry(path)["sites"]
    rules = find_rules(model, experiment=experiment, activity=activity,
                       generation=generation, path=path)
    if not rules:
        raise LookupError(
            f"No Polytope address registered for {query}. Add a rule to "
            f"{REGISTRY_PATH.name} if this simulation exists."
        )

    matched = {rule["site"] for rule in rules}
    if len(matched) > 1:
        unset = [k for k, v in keys.items() if v is None]
        raise LookupError(
            f"{query} is ambiguous: it matches simulations on "
            f"{sorted(matched)}. Narrow it down by passing "
            f"{', '.join(unset)}."
        )
    return sites[rules[0]["site"]]


def resolve_addresses(models, experiment=None, activity=None,
                      generation=DEFAULT_GENERATION, path=None):
    """Resolve several models at once, as ``{model: address}``."""
    return {
        m: resolve_address(m, experiment=experiment, activity=activity,
                           generation=generation, path=path)
        for m in models
    }
