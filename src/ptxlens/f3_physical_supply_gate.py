"""Import source-verified F3 prospective industrial H2 backup architecture.

Source-based 2023 H2 demand and 2026 Dutch operator technical references
belong to different temporal evidence classes. This imports the candidate
design basis ONLY, never a certified 2023 supply plant or matched LCA/TEA.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from .f3_backup_service_gate import verify_source_backup_load

ROOT=Path(__file__).resolve().parents[2]
PATH=ROOT/"data/results/F3_2023_2026_prospective_h2_delivery_architecture.json"
REGISTRY=ROOT/"research/f3_backup_physical_source_register_v1.json"
REGISTERED_SHA256="dbb42012e9a4375adc703aa336a66cfc83994f3b2ab15a7a9b98aa9b94596ce3"


class IneligibleH2PhysicalSupply(ValueError):
    pass


def verify_prospective_design_basis(path=PATH):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=REGISTERED_SHA256:
        raise IneligibleH2PhysicalSupply("unsigned/changed source-derived PtXFlex candidate design basis")
    d=json.loads(raw)
    reg=json.loads(REGISTRY.read_text(encoding="utf-8"))
    if d.get("schema_version")!="ptxflex.f3_prospective_backup_delivery_design_basis.v1":
        raise IneligibleH2PhysicalSupply("wrong original-source/2026 prospective candidate schema")
    if (d.get("reference_weather_and_wholesale_price_year")!=2023
            or d.get("external_network_architecture_source_year")!=2026
            or d.get("prospective_2026_infrastructure_is_not_observed_2023_site_supply") is not True):
        raise IneligibleH2PhysicalSupply("future infrastructure backdated as 2023 observed physical source")
    if (d.get("published_hynetwork_pressure_is_network_entry_not_customer_exit_guarantee") is not True
            or d.get("published_hynetwork_quality_annex_is_not_end_use_grade_contract") is not True):
        raise IneligibleH2PhysicalSupply("source network operating regime recast as physical customer guarantee")
    if d.get("source_reference_ids")!=[r["id"] for r in reg["source_references"]]:
        raise IneligibleH2PhysicalSupply("cross-repository industrial source register mismatch")
    for key in ("actual_site_location","physical_hydrogen_connection_and_supply_contract",
                "end_use_purity_grade_and_impurity_limits"):
        if key not in d or d[key] is not None:
            raise IneligibleH2PhysicalSupply("unsupported quantified/certified site property "+key)
    for key in ("backup_LCA_process_inventory_available",
                "backup_whole_system_EUR_DCF_available",
                "physically_verified_common_hourly_service",
                "comparative_environmental_or_cost_superiority_eligible",
                "source_specific_20bar_absolute_delivery_pressure_verified"):
        if d.get(key) is not False:
            raise IneligibleH2PhysicalSupply("prospective candidate falsely marked ready for LCIA/TEA: "+key)
    if d.get("fixed_original_model_required_delivery_pressure_bar_absolute")!=20:
        raise IneligibleH2PhysicalSupply("changed original physical delivery pressure requirement")
    if set(d.get("modes",{}))!={"max_inventory","usable_service"}:
        raise IneligibleH2PhysicalSupply("missing original source E physical storage semantics")
    for mode,rec in d["modes"].items():
        source=verify_source_backup_load(mode)
        annual=rec.get("source_specific_feasible_incumbent_topup_annual_kg")
        peak=rec.get("source_specific_incumbent_peak_hour_topup_kg_h")
        if not all(isinstance(n,(float,int)) and not isinstance(n,bool) and math.isfinite(n) for n in (annual,peak)):
            raise IneligibleH2PhysicalSupply("nonfinite backup screen physical duty")
        if abs(annual-source["single_incumbent_hypothetical_topup_annual_kg"])>.002 or abs(
                peak-source["single_incumbent_hypothetical_topup_max_kg_per_hour"])>.002:
            raise IneligibleH2PhysicalSupply("mismatched original E source load")
        paths=rec.get("pathways",{})
        if set(paths)!={"contracted_dedicated_H2_pipeline","gaseous_tube_trailer_delivery","additional_on_site_electrolysis"}:
            raise IneligibleH2PhysicalSupply("omitted source candidate physical backup route")
        pipe=paths["contracted_dedicated_H2_pipeline"]
        trailer=paths["gaseous_tube_trailer_delivery"]
        if pipe.get("the_30barg_value_is_not_site_customer_exit_pressure") is not True:
            raise IneligibleH2PhysicalSupply("wrong interpretation of HNS 2026 transport Annex 7")
        if any(pipe.get(k) is not None for k in ("customer_guaranteed_min_exit_pressure_bar_absolute",
                    "customer_firm_hourly_nomination_capacity_kg_h","customer_h2_impurity_certification",
                    "hourly_2023_supply_availability","full_plant_LCI_and_capex")):
            raise IneligibleH2PhysicalSupply("invented connection pressure, site supply or process LCI")
        if (trailer.get("payload_equivalents_are_not_actual_required_vehicle_trips") is not True
                or trailer.get("recovered_usable_H2_from_tank_down_to_20bar_absolute_kg") is not None
                or trailer.get("actual_deliverable_peak_flow_kg_h") is not None
                or trailer.get("full_plant_LCI_and_cost") is not None):
            raise IneligibleH2PhysicalSupply("US composite benchmark wrongly presented as Dutch actual trailer supply")
        if rec.get("environmental_and_tea_comparison_eligible") is not False:
            raise IneligibleH2PhysicalSupply("functional service and full LCA/TEA incorrectly certified")
    return d


def native_lca_tea_admissibility():
    x=verify_prospective_design_basis()
    return {
        "programme":"OEM-PTX-2026-01",
        "physical_candidate_sha256":REGISTERED_SHA256,
        "source_2023_modelled_hydrogen_demand_and_2026_supply_framework_not_measured_together":True,
        "site_location_and_physically_guaranteed_h2_available":False,
        "exit_delivery_flow_pressure_purity_and_reliability_qualified":False,
        "additional_backup_manufacturing_operations_and_transport_lci_complete":False,
        "native_BAFU_2026_v11_full_system_matched_service_GWP":None,
        "full_system_discounted_EUR2023_LCOH":None,
        "comparative_environmental_or_tea_result_allowed":False,
        "candidate_route_choice":x["candidate_route_priority"],
        "next_dependency":"site-specific contracted H2 delivery and pressure/quality/flow verification, then provider-matched LCI and full DCF",
    }
