"""Actual OpenPyTEA 3.2.2 capital-only cross-check using documented 2023
PyNEXUS case summaries and DOE 2024 published 2022-USD capital assumptions.

Not a full LCOH: OPEX and wholesale electricity deliberately excluded, and
the rate is an explicit analyst sensitivity, *not* DOE's H2A assumption.
"""
from __future__ import annotations
import importlib.metadata
import json
import math
from pathlib import Path

from .doe import DOE_URL, CAPEX_CASES_USD2022_KW


def openpytea_doe_capital(case, *, cost_usd2022_kw, discount_rate):
    if cost_usd2022_kw not in CAPEX_CASES_USD2022_KW:
        raise ValueError("requires DOE documented installed-cost case")
    if not isinstance(discount_rate,(int,float)) or not math.isfinite(discount_rate) or discount_rate < 0:
        raise ValueError("explicit nonnegative finance sensitivity rate required")
    if case["scenario"] not in ("E","E+S") or case["hours"] != 8760:
        raise ValueError("requires 2023 8760h audited PyNEXUS WP5 registry case")
    for f in ("archive_sha256","stage_b_sha256","price_csv_sha256"):
        if len(case[f]) != 64:
            raise ValueError("source identity missing")
    from openpytea.plant import Plant

    annual_h2 = case["delivered_h2_kg"]
    if annual_h2 <= 0 or case["online_hours"] <= 0:
        raise ValueError("source hydrogen and operating hours must be positive")
    initial_capital = float(case["electrolyser_mw"]*1000*cost_usd2022_kw)
    # Model uses discrete 1-based investment years; document conversion
    # from DOE's 40,000 operating-hour stack-life statement.
    replacement_years = []
    i = 1
    while True:
        year = math.ceil(40000*i/case["online_hours"])
        if year >= 30:
            break
        if year in replacement_years:
            raise ValueError("multiple replacements mapped to one year")
        replacement_years.append(year)
        i += 1
    years = [1] + replacement_years
    amounts = [initial_capital] + [0.11*initial_capital]*len(replacement_years)
    config = {
        "plant_name":"DOE-24005 PEM CAPEX-only / frozen PyNEXUS " + case["scenario"],
        "country":"United States",
        "currency":"USD",
        "process_type":"Fluids",
        "equipment":[],
        "interest_rate":discount_rate,
        "project_lifetime":30,
        "plant_utilization":1.0,
        "tax_rate":0,
        "working_capital":0,
        "fp":0,
        "loc_factor":1.0,
        "capex_ramp":[0.0],
        "production_ramp":[1.0]*30,
        "operator_hourly_rate":{"rate":0},
        "operators_per_shift":0,
        "variable_opex_inputs":{},
        "plant_products":{"hydrogen":{"production":annual_h2/365.0,"price":0}},
        "additional_capex_years":years,
        "additional_capex_cost":amounts,
        "fixed_capital_components":{"osbl":0.0,"dne":0.0,"contingency":0.0},
    }
    plant = Plant(config)
    value = float(plant.calculate_levelized_cost())
    if not math.isfinite(value) or value <= 0:
        raise ValueError("OpenPyTEA returned nonphysical capital-only result")
    pv_capex = sum(amt/(1+discount_rate)**year for year,amt in zip(years,amounts))
    pv_h2 = annual_h2*sum(1/(1+discount_rate)**year for year in range(1,31))
    checked = pv_capex/pv_h2
    if not math.isclose(value,checked,abs_tol=1e-5,rel_tol=1e-7):
        raise ValueError(f"OpenPyTEA capital schedule differs from independent cashflow: {value} vs {checked}")
    return {
        "schema_version":"ptxlens.openpytea_doe_capital_only.v0.1",
        "execution_status":"ACTUALLY_CALCULATED_OPENPYTEA",
        "openpytea_version":importlib.metadata.version("OpenPyTEA"),
        "scenario":case["scenario"],
        "source_archive_sha256":case["archive_sha256"],
        "source_dispatch_sha256":case["stage_b_sha256"],
        "source_record":"PyNEXUS Oct 2026 frozen E/E+S computational 2023 NL data",
        "doe_assumption_url":DOE_URL,"capex_cost_usd2022_kw":cost_usd2022_kw,
        "finance_rate_sensitivity_NOT_DOE":discount_rate,
        "capital_years_one_based":years,"capital_spending_usd2022":amounts,
        "annual_delivered_model_h2_kg_repeated_30_years":annual_h2,
        "openpytea_capital_only_usd2022_per_kg":value,
        "independent_discounted_cashflow_usd2022_per_kg":checked,
        "year_one_capex_timing":"in year 1; this differs from standard time-zero CRF",
        "excluded":"ALL electricity market settlement, OPEX, labour, tariffs, taxes, storage, wind assets, production ramp and validated 30y performance",
        "research_status":"documented capital-only sensitivity; NOT total levelized hydrogen production cost",
    }


def run_registry(registry_file, cost_usd2022_kw, discount_rate, out_file):
    reg=json.loads(Path(registry_file).read_text(encoding="utf-8"))
    if reg.get("schema_version") != "ptxlens.source_register.v0.1":
        raise ValueError("incompatible source register")
    results=[
        openpytea_doe_capital(reg[key],cost_usd2022_kw=cost_usd2022_kw,discount_rate=discount_rate)
        for key in ("base","storage")
    ]
    path=Path(out_file)
    if path.exists():
        raise FileExistsError("refusing to overwrite OpenPyTEA evidence")
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(results,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return results
