"""Hash-registered, source-verified PtXFlex F3 2023 hypothetical H2 top-up gate.

Only mathematical delivery-node shortage filling, not a demonstrated backup
supplier. No physical 20-bar/purity/regulatory quality, cost, LCI or lifecycle
cost data can be inferred from these historic-model dispatch results.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from .f3_reconciled_source_bridge import read_verified_f3_evidence

ROOT=Path(__file__).resolve().parents[2]/"data/results"
EXPECTED_BACKUP_SHA256={
    "max_inventory":"c65fda894ef4b30e09339ad88a3972625af78c17802fd0cb9a2fc25d3205882f",
    "usable_service":"d893c6388f14d276b2ef5d4bff4b6c8057dd252067f307f83b9baafcfa1e5308",
}
SCHEMA="ptxflex.F3_2023_hypothetical_source_hourly_H2_backup_load_envelope.v1"
SOURCE_E="069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051"
SOURCE_ES="cd4101fe62c3f1b8aa2d7508d3651d2fee40d2bafe6d5b87e40d5f4d055070f9"


class InvalidBackstopSource(ValueError):
    pass


def _n(x,name):
    if isinstance(x,bool) or not isinstance(x,(float,int)) or not math.isfinite(x):
        raise InvalidBackstopSource(name+" is not finite numeric")
    return float(x)


def verify_source_backup_load(mode, *,path=None):
    if mode not in EXPECTED_BACKUP_SHA256:
        raise InvalidBackstopSource("unregistered 2023 physical bank semantics")
    f=Path(path) if path is not None else ROOT/f"F3_2023_original_E_source_hypothetical_backup_{mode}.json"
    raw=f.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_BACKUP_SHA256[mode]:
        raise InvalidBackstopSource("unapproved or altered 2023 E backup load evidence SHA256")
    data=json.loads(raw)
    rec=read_verified_f3_evidence()
    src=rec["modes"][mode]["cases"]["E"]
    if (data.get("schema_version")!=SCHEMA or data.get("capacity_semantics")!=mode
            or data.get("source_pressure_screen_case")!="E"
            or data.get("source_E_zip_sha256")!=SOURCE_E
            or data.get("source_EplusS_zip_sha256")!=SOURCE_ES):
        raise InvalidBackstopSource("original source identifiers or schema changed")
    if abs(_n(data.get("source_2023_original_E_reference_delivered_kg"),"source reference")-
           rec["reference_E_delivered_hourly_target_total_kg"])>.002:
        raise InvalidBackstopSource("different original annual H2 delivery target")
    if abs(_n(data.get("original_full_2023_modelled_demand_kg"),"full contract")-18250000.)>.002:
        raise InvalidBackstopSource("original full demand changed")
    if data.get("additional_shortage_is_relative_to_E_delivered_reference_not_full_contract") is not True:
        raise InvalidBackstopSource("mistaken full H2 industrial contract claim")
    lower=_n(data.get("stageA_original_MILP_min_shortage_certified_lower_bound_kg"),"certified lower")
    upper=_n(data.get("stageA_original_feasible_dispatch_shortage_upper_bound_kg"),"incumbent upper")
    load=_n(data.get("single_incumbent_hypothetical_topup_annual_kg"),"annual topup")
    peak=_n(data.get("single_incumbent_hypothetical_topup_max_kg_per_hour"),"maximum hourly topup")
    peak24=_n(data.get("single_incumbent_hypothetical_topup_24h_peak_kg"),"24h topup")
    if not 0<lower<=upper+2e-4 or abs(load-upper)>2e-4 or not 0<peak<=peak24<=load+1e-3:
        raise InvalidBackstopSource("unphysical shortfall interval or backup-load envelope")
    if abs(lower-src["minimum_additional_modelled_H2_shortfall_lower_bound_kg"])>.002 or abs(
            upper-src["minimum_additional_modelled_H2_shortfall_upper_bound_kg"])>.002:
        raise InvalidBackstopSource("hourly backup demand not same original F3 source pressure case")
    h=data.get("single_incumbent_hypothetical_topup_occupied_hours")
    event=data.get("single_incumbent_contiguous_event_count")
    longest=data.get("single_incumbent_longest_event_hours")
    if (not all(isinstance(v,int) and not isinstance(v,bool) for v in (h,event,longest))
            or not 0<event<=h<=8760 or not 0<longest<=h):
        raise InvalidBackstopSource("unphysical 2023 source hourly deficiency event count")
    if (data.get("source_8760_sequential_hourly_indices") is not True
            or data.get("modelled_hydrogen_not_measured_plant_production") is not True
            or data.get("hourly_shortage_magnitude_is_a_modelled_feasible_incumbent_not_global_optimum") is not True):
        raise InvalidBackstopSource("missing modelling and optimality caveats")
    for x in ("external_H2_supplier_physically_specified",
              "external_H2_gas_purity_quality_verified",
              "external_H2_pressure_regulation_and_transport_verified",
              "external_backup_supply_ramp_availability_and_reliability_verified",
              "backup_full_lca_or_tea_complete",
              "matched_service_LCA_TEA_comparison_permitted"):
        if data.get(x) is not False:
            raise InvalidBackstopSource("unverified backup physical, cost, or environmental gate: "+x)
    for x in ("incremental_backup_H2_kgCO2e_per_kg","incremental_backup_cost_EUR_per_kg"):
        if x not in data or data[x] is not None:
            raise InvalidBackstopSource("unsourced backup marginal cost or GWP must stay null")
    return data


def service_equivalence_barrier():
    """Couple source-derived hour-by-hour need to strict downstream gate."""
    scenarios={}
    for mode in EXPECTED_BACKUP_SHA256:
        x=verify_source_backup_load(mode)
        scenarios[mode]={
            "backup_annual_topup_for_one_source_feasible_incumbent_kg":
                x["single_incumbent_hypothetical_topup_annual_kg"],
            "backup_peak_hourly_requirement_for_that_incumbent_kg_h":
                x["single_incumbent_hypothetical_topup_max_kg_per_hour"],
            "backup_peak_24h_requirement_for_that_incumbent_kg":
                x["single_incumbent_hypothetical_topup_24h_peak_kg"],
            "backup_capacity_costs_emissions_and_quality_specified":False,
            "eligible_for_matched_service_native_BAFU_and_DCF":False,
            "source_output_sha256":EXPECTED_BACKUP_SHA256[mode]
        }
    return {
        "modelled_reference_service_not_original_full_H2_demand":True,
        "original_source_hourly_shortage_proof_f3_imported":True,
        "hypothetical_source_backstop_required":True,
        "real_source_physically_usable_backstop_supplier_available":False,
        "comparative_LCA_TEA_allowed":False,
        "scenarios":scenarios
    }
