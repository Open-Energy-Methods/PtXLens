"""Annualized PtX cost and GWP screening, not a complete TEA or LCIA."""
import hashlib
import json
import math
from datetime import datetime, timedelta


SCHEMA = "ptxlens.dispatch.v0.1"
NONNEG = ("wind_mwh", "grid_import_mwh", "grid_export_mwh",
          "h2_produced_kg", "h2_delivered_kg", "h2_unserved_kg",
          "grid_gwp_kgco2e_mwh", "wind_gwp_kgco2e_mwh")


def num(x, name, minimum=None):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(f"{name} must be finite numeric")
    if minimum is not None and x < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return float(x)


def crf(rate, years):
    rate = num(rate, "rate", 0)
    years = num(years, "years", 1)
    if years != int(years):
        raise ValueError("years must be integral")
    return 1 / years if rate == 0 else rate / (1 - (1 + rate) ** -years)


def amounts(d, name):
    if not isinstance(d, dict):
        raise ValueError(f"{name} requires mapping")
    return {str(k): num(v, f"{name}.{k}", 0) for k, v in d.items()}


def check(d):
    if d.get("schema_version") != SCHEMA or not d.get("scenario_id"):
        raise ValueError("unsupported schema or missing scenario_id")
    evidence = d.get("evidence", {})
    if evidence.get("kind") not in ("synthetic", "pynexus_frozen", "ptxflex_verified"):
        raise ValueError("must identify synthetic or verified source")
    if evidence["kind"] == "pynexus_frozen" and any(
        not isinstance(evidence.get(k), str) or len(evidence[k]) != 64
        for k in ("source_commit", "manifest_sha256", "dispatch_sha256")
    ):
        raise ValueError("frozen artifact needs source commit and file hashes")
    m = d.get("metadata", {})
    if m.get("currency") != "EUR" or not isinstance(m.get("price_year"), int):
        raise ValueError("EUR and explicit price_year required")
    if not m.get("annualization_basis") or not m.get("gwp_method_statement"):
        raise ValueError("annualization and GWP source statement required")
    dt = num(m.get("dt_hours"), "dt_hours", 0)
    scale = num(m.get("annualization_factor"), "annualization_factor", 0)
    rows = d.get("hours")
    if not dt or not scale or not isinstance(rows, list) or not rows:
        raise ValueError("positive interval and nonempty rows required")
    if abs(dt * len(rows) * scale - 8760) > 1e-7:
        raise ValueError("must explicitly annualize to 8760 hours")
    if evidence["kind"] == "pynexus_frozen" and (len(rows) != 8760 or dt != 1 or scale != 1):
        raise ValueError("cannot rescale frozen annual PyNEXUS")
    previous = None
    for h in rows:
        t = h.get("timestamp_utc")
        if not isinstance(t, str) or not t.endswith("Z"):
            raise ValueError("UTC Z timestamp required")
        try:
            stamp = datetime.fromisoformat(t.replace("Z", "+00:00"))
        except ValueError as ex:
            raise ValueError("invalid time") from ex
        if previous is not None and stamp - previous != timedelta(hours=dt):
            raise ValueError("non-consecutive timestamps")
        previous = stamp
        for key in NONNEG:
            num(h.get(key), key, 0)
        num(h.get("grid_price_eur_mwh"), "grid_price_eur_mwh")
        if h["grid_import_mwh"] > 1e-9 and h["grid_export_mwh"] > 1e-9:
            raise ValueError("simultaneous buy/sell requires separate reconciliation")
    return rows, scale


def assess(d):
    """Compute explicit component screening; all factors are supplied by caller."""
    rows, scale = check(d)
    econ, env = d["economics"], d["environment"]
    rate = num(econ["discount_rate"], "discount_rate", 0)
    life = num(econ["lifetime_years"], "lifetime_years", 1)
    capex = sum(amounts(econ["capex_eur"], "capex_eur").values())
    repl = amounts(econ.get("replacement_cost_eur_by_year", {}), "replacement")
    embodied = sum(amounts(env["embodied_kgco2e"], "embodied").values())
    repl_gwp = amounts(env.get("replacement_kgco2e_by_year", {}), "replacement_gwp")
    for series in (repl, repl_gwp):
        if any(not k.isdigit() or not 0 < int(k) < life for k in series):
            raise ValueError("replacement must occur inside lifetime")
    if not isinstance(econ.get("wind_cost_basis"), str) or not econ["wind_cost_basis"]:
        raise ValueError("wind_cost_basis is mandatory")
    fixed = num(econ["fixed_opex_eur_year"], "fixed opex", 0)
    variable = num(econ["variable_opex_eur_kg"], "variable opex", 0)
    wind_value = num(econ["wind_value_eur_mwh"], "wind value", 0)
    upstream = num(env["other_upstream_kgco2e_kg_h2"], "upstream", 0)
    delivered = sum(h["h2_delivered_kg"] for h in rows) * scale
    shortfall = sum(h["h2_unserved_kg"] for h in rows) * scale
    if delivered <= 0:
        raise ValueError("zero delivered hydrogen: cannot normalize")
    annual_capital = crf(rate, life) * (capex + sum(v/(1+rate)**int(k) for k,v in repl.items()))
    costs = {
        "annualized_capital_eur": annual_capital,
        "fixed_opex_eur": fixed, "variable_opex_eur": variable * delivered,
        "wholesale_grid_settlement_eur": scale * sum(
            (h["grid_import_mwh"] - h["grid_export_mwh"]) * h["grid_price_eur_mwh"] for h in rows),
        "declared_wind_value_eur": scale * sum(h["wind_mwh"] * wind_value for h in rows)
    }
    ghg = {
        "electricity_factor_kgco2e": scale * sum(
            h["grid_import_mwh"]*h["grid_gwp_kgco2e_mwh"] +
            h["wind_mwh"]*h["wind_gwp_kgco2e_mwh"] for h in rows),
        "annualized_embodied_kgco2e": (embodied + sum(repl_gwp.values())) / life,
        "other_upstream_kgco2e": upstream * delivered,
    }
    return {
        "schema_version": "ptxlens.screening.v0.1", "scenario_id": d["scenario_id"],
        "evidence_kind": d["evidence"]["kind"],
        "input_sha256": hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest(),
        "method_claim": "illustrative component accounting, NOT full TEA, openLCA or LCIA",
        "annual_delivered_h2_kg": delivered, "annual_unserved_h2_kg": shortfall,
        "cost_eur_per_year": costs, "gwp_kgco2e_per_year": ghg,
        "screening_cost_eur_per_kg_delivered": sum(costs.values())/delivered,
        "screening_gwp_kgco2e_per_kg_delivered": sum(ghg.values())/delivered,
    }


def inventory(d):
    """OpenLCA inventory staging JSON; not a native openLCA database or calculation."""
    rows, scale = check(d)
    total = lambda k: scale * sum(h[k] for h in rows)
    return {
        "schema_version": "ptxlens.openlca_staging.v0.1",
        "status": "NOT calculated in openLCA; product flows, providers, LCIA method missing",
        "scenario_id": d["scenario_id"],
        "reference_product": {"name": "hydrogen, delivered", "unit": "kg", "amount": total("h2_delivered_kg")},
        "electricity_demands": [
            {"name": "grid", "unit": "MWh", "amount": total("grid_import_mwh")},
            {"name": "wind onsite", "unit": "MWh", "amount": total("wind_mwh")}],
        "grid_export_mwh": total("grid_export_mwh")
    }
