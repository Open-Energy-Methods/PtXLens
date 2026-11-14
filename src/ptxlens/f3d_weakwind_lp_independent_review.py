"""F3-D independently source-verify follow-on LP-relaxed weak-wind necessary infeasibility.

The initial 2023 source wind ×0.9 paired MILPs had no accepted incumbents.
Later PtXFlex explicitly removed only integrality constraints and the
price objective (zero feasibility objective), keeping identical original
2023 8760-hour H2, grid, PEM, pressure, capacity, terminal, ramp constraints.
HiGHS status 2 on the LP SUPERSET rules out any source MILP feasible dispatch
under the source model, subject to numerical tolerances. It does not prove
a real hydrogen installation infeasible and does not supply economic costs.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from .f3d_independent_2023_stress_finance_bridge import (
    source_one,MODE_SHAS,MAIN_SRC_E,MAIN_SRC_ES
)

ROOT=Path(__file__).resolve().parents[2]
SCHEMA="ptxlens.f3d_independent_weakwind_2023_source_LP_status2_feasibility_proof_NOT_site_v1"
EXPECTED="ptxflex.f3d_2023_weak_wind_090_model_relaxed_LP_feasibility_status_source_locked.v1"
FILES={
 "max_inventory":"4d7b18e53ed46d8969b31e7c7fe6c59330ad524f74332beb4aa53a8845483cd8",
 "usable_service":"037d98d9c927c28ff8eacde479fae03bbe3d4a02ae4644fe6c6a8f8b9237a718"
}

class BadWeakWindProof(ValueError):pass

def require(x,msg):
    if not x:raise BadWeakWindProof(msg)

def verify_one(mode):
    require(mode in FILES,"unregistered 2023 0.9 wind source capacity semantics")
    path=ROOT/"data/results"/f"F3_D_2023_{mode}_wind090_original_source_LP_relaxation_NOT_plant_proof.json"
    raw=path.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==FILES[mode],
            "substituted or tampered original 2023 E+ES LP feasibility record")
    x=json.loads(raw)
    original=source_one(mode,"wind_090_multiplier")
    require(x.get("schema_version")==EXPECTED and x.get("source_year")==2023 and
            x.get("scenario_id")=="wind_090_multiplier" and x.get("mode")==mode and
            x.get("source_observed_E_SHA256")==MAIN_SRC_E and
            x.get("source_observed_EplusS_SHA256")==MAIN_SRC_ES and
            x.get("source_2023_common_h2_hourly_SHA256")==MODE_SHAS[mode] and
            x.get("same_hourly_H2_and_identical_price_wind_for_E_and_EplusS") is True and
            x.get("not_observed_new_2022_or_2024_weather") is True and
            x.get("paired_economic_preference_OR_certified_wholesale_savings_eur") is None and
            x.get("full_LCA_LCOH_and_v1_release_passed") is False,
            "source actual H2 hour, year, pressure and no-economics boundaries violated")
    require(x.get("source_hourly_2023_price_sha256")==
            original["source_2023_input_price_and_wind_provenance"]["source_price_2023_float64_sha256"] and
            x.get("counterfactual_source_2023_wind_power_sha256")==
            original["source_2023_input_price_and_wind_provenance"]["scenario_wind_float64_sha256"] and
            x.get("source_StageA_zip_SHA256")==
            original["original_source_StageA_archive_SHA256"],
            "LP did not actually solve original 2023 source MIP's altered weather and matched service")
    for case in ("E","E_plus_S"):
        r=x[case]
        require(r.get("schema_version")==
                "ptxflex.f3d_identical_model_binary_relaxed_h2_feasibility_diagnostic.v1" and
                r.get("tested_hours")==8760 and
                r.get("source_model_pressure_screened") is True and
                r.get("source_H2_required_annual_kg")==x["E"]["source_H2_required_annual_kg"] and
                r.get("solver_status_code")==2 and
                "infeasible" in r.get("solver_status_message","").lower() and
                r.get("LP_model_has_accepted_feasible_vector") is False and
                r.get("LP_relaxation_infeasible_as_reported_by_HiGHS") is True and
                r.get("MILP_infeasibility_supported_if_LP_status_2") is True and
                r.get("all_original_hourly_electricity_H2_storage_pressure_compressor_constraints_preserved") is True and
                r.get("LP_feasibility_objective_zero_ignores_2023_wholesale_cost") is True and
                r.get("LP_relaxed_binary_primal_NOT_a_valid_integer_dispatch") is True and
                r.get("actual_site_operational_infeasibility_certified") is False,
                "wrong LP superset: no proof original source MILP infeasible")
    require(x.get("both_original_source_E_and_ES_relaxed_LPs_reported_infeasible") is True,
            "one original source 2023 H2 case LP still unclassified")
    return x

def review_both():
    a=verify_one("max_inventory")
    b=verify_one("usable_service")
    return {
      "schema_version":SCHEMA,
      "programme":"OEM-PTX-2026-01",
      "source_original_ERA5_2023_and_ENTSOE_price2023_only":True,
      "counterfactual_wind_available_MW_multiplier":.9,
      "both_capacity_modes_and_both_E_and_EplusS_HiGHS_LP_status2":True,
      "solver_infeasible_LP_is_superset_of_original_binary_MILP":True,
      "modelled_source_hourly_target_unattainable_in_E_and_ES_under_wind_090":True,
      "full_real_site_hydrogen_unattainable_proven":False,
      "new_observed_2022_2024_data_retrieved":False,
      "relative_annual_wholesale_cost_under_stress_eur":None,
      "hypothetical_financial_capex_break_even_at_wind_090_eur":None,
      "native_full_BAFU_storage_manufacturing_GWP_kgCO2e":None,
      "real_full_LCOH_and_industrial_plant_certified":False,
      "mode_original_source_LP_SHA256":FILES,
      "source_2023_H2_targets_float64_SHA256":MODE_SHAS,
      "solver_note":"HiGHS LP status=2 under numerical tolerances for full 8760h E and ES in both separate capacity semantics, preserving all continuous physical source H2/electricity/pressure constraints, only integrality relaxed",
    }
