"""PtXFlex F3 2023 H2 supplier/transport exit boundary controls: fail-closed LCA bridge.

A Hynetwork 2026 customer connection agreement is NOT a gas purchase contract.
The original PyNEXUS 52.5N/3.5E offshore ERA5 grid is NOT a real H2 customer
site. 2023 modelling + 2026 prospective infrastructure cannot prove a historical
H2 backup supplier. Mathematically covered synthetic 8760h load, if present,
must never be accepted as native BAFU 2026 v1.1 GWP or full DCF evidence.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from .f3_backup_service_gate import verify_source_backup_load
from .f3_physical_supply_gate import verify_prospective_design_basis

ROOT=Path(__file__).resolve().parents[2]
CANDIDATE=ROOT/"data/results/F3_2023_shortage_2026_HNS_exit_and_supplier_boundary_control.json"
SOURCE_REGISTRY=ROOT/"research/f3_h2_exit_and_supplier_source_evidence_v1.json"
RESULT_SHA256="e918364ad469dd29791d8c9a01f1dc5f9a37435f8247c65a87ba6c388f1e2d25"
SOURCE_SPARSE_SHA={
    "max_inventory":"9acefa605c878e19f369f57cd94519fc9dd926beda284135529b7d89ce31208e",
    "usable_service":"9c66837c105e5c17e2fbdceb50250a2ea7940ac0a2a321a08ffec8cf81622999",
}


class IneligibleContractualH2Source(ValueError):
    pass


def audited_H2_supplier_qualification_result(path=CANDIDATE):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=RESULT_SHA256:
        raise IneligibleContractualH2Source("unregistered source-verified F3 synthetic 2023 hourly supplier boundary result")
    x=json.loads(raw)
    r=json.loads(SOURCE_REGISTRY.read_text(encoding="utf-8"))
    verify_prospective_design_basis()
    if (r.get("schema_version")!="oem.ptx.f3_NL_h2_connection_supplier_independent_evidence.v1"
        or x.get("schema_version")!="ptxflex.f3_2023_H2_shortage_vs_prospective_contractual_supply_thresholds.v1"
        or x.get("model_year")!=2023
        or x.get("source_2026_Hynetwork_operator_terms_are_not_actual_2023_gas_supply") is not True
        or x.get("original_ERA5_wind_location_not_a_real_H2_customer_exit_location") is not True):
        raise IneligibleContractualH2Source("original E H2 site or 2023/2026 network time basis distorted")
    loc=r.get("original_PyNEXUS_annual_config",{})
    wind=loc.get("original_ERA5_wind_resource_location",{})
    if (wind.get("lat")!=52.5 or wind.get("lon")!=3.5
        or loc.get("weather_grid_not_a_pipeline_connection_coordinate") is not True
        or loc.get("industrial_H2_delivered_site_lat_lon") is not None
        or loc.get("industrial_H2_customer_name_or_address") is not None):
        raise IneligibleContractualH2Source("original offshore wind grid erroneously used as industrial H2 plant site")
    roles=r.get("commercial_and_technical_roles",{})
    if any(roles.get(k) is not True for k in (
        "hynetwork_is_not_H2_molecule_supply_guarantor",
        "supplier_or_shipper_is_distinct_from_network_operator",
        "requires_independent_signed_network_exit_connection_and_signed_H2_purchase_shipping_contract",
        "network_access_contract_alone_proves_no_guaranteed_gas")):
        raise IneligibleContractualH2Source("network TSO connection incorrectly treated as sale of molecules")
    if (x.get("network_operator_does_not_guarantee_hydrogen_supply") is not True
        or x.get("supplier_contract_exit_connection_contract_both_missing") is not True
        or x.get("all_scenarios_ARE_MATHEMATICAL_synthetic_no_buffer_tests") is not True
        or x.get("no_scenario_proves_supplier_availability_hydraulics_or_certified_end_use_quality") is not True
        or x.get("comparative_E_vs_ES_matched_service_permitted") is not False):
        raise IneligibleContractualH2Source("synthetic mathematical source wrongly qualified for plant LCA")
    if x.get("native_BAFU_full_comparative_GWP") is not None or x.get("full_EUR2023_system_DCF") is not None:
        raise IneligibleContractualH2Source("unavailable actual plant GWP or DCF invented")
    hhv=r.get("hynetwork_study_HHV_kWh_per_kg_derived")
    if (not isinstance(hhv,(int,float)) or isinstance(hhv,bool)
        or abs(hhv-12.74/0.090/3.6)>1e-9
        or abs(x.get("Hynetwork_CSA_HHV_kWh_kg",0)-hhv)>1e-9
        or r.get("contract_peak_capacity_kWh_per_hour_requires_correct_total_connection_flow_not_automatically_incremental_backstop") is not True):
        raise IneligibleContractualH2Source("wrong HNS CSA capacity energy basis or total-vs-backup flow")
    expected=set(SOURCE_SPARSE_SHA)
    modes=x.get("modes",{})
    if not isinstance(modes,dict) or set(modes)!=expected:
        raise IneligibleContractualH2Source("original physical 20t E capacity sensitivity incomplete")
    for mode,e in modes.items():
        old=verify_source_backup_load(mode)
        if e.get("source_2023_hourly_shortage_SHA256")!=SOURCE_SPARSE_SHA[mode]:
            raise IneligibleContractualH2Source("original sparse 8760h H2 source digest mismatch")
        annual=e.get("source_annual_additional_modelled_H2_kg")
        peak=e.get("max_2023_incumbent_replacement_H2_kg_h")
        if (any(not isinstance(z,(int,float)) or isinstance(z,bool) or not math.isfinite(z)
                for z in (annual,peak))
            or abs(annual-old["single_incumbent_hypothetical_topup_annual_kg"])>.002
            or abs(peak-old["single_incumbent_hypothetical_topup_max_kg_per_hour"])>.002
            or abs(e.get("incremental_topup_HNS_CSA_study_form_HHV_kWh_h",0)-peak*hhv)>1e-3):
            raise IneligibleContractualH2Source("source model H2 duty or Hynetwork energy unit mismatch")
        if (e.get("actual_connection_total_peak_HHV_kWh_h") is not None
            or not str(e.get("no_actual_h2_supplier_8760h_series","")).startswith("NOT_ASSESSABLE")):
            raise IneligibleContractualH2Source("unsourced signed site connection and hourly supplier falsely identified")
        cases=e.get("mathematical_boundary_cases",{})
        required={"EXACT_PEAK_FLOW_20BARA_PERFECT_UPTIME","BELOW_PEAK_FLOW_ONE_HALF",
                  "LOW_PRESSURE_AT_CUSTOMER_NODE","EXIT_OR_SUPPLIER_OFFLINE_AT_PEAK_HOUR",
                  "PRODUCT_QUALITY_FAILED_AT_PEAK_HOUR"}
        if set(cases)!=required:
            raise IneligibleContractualH2Source("synthetic pressure/flow/purity/reliability negative controls absent")
        theoretical=cases["EXACT_PEAK_FLOW_20BARA_PERFECT_UPTIME"]
        if (theoretical.get("unmet_h2_kg")!=0 or theoretical.get("unmet_h2_hours")!=0
            or theoretical.get("physical_supplier_verified") is not False
            or theoretical.get("full_lca_tea_eligible") is not False):
            raise IneligibleContractualH2Source("hypothetical perfect source was presented as real supplier")
        for key,case in cases.items():
            if case.get("physical_supplier_verified") is not False or case.get("full_lca_tea_eligible") is not False:
                raise IneligibleContractualH2Source("synthetic contract test marked as environmentally or economically admissible")
            if key!="EXACT_PEAK_FLOW_20BARA_PERFECT_UPTIME" and (
                not isinstance(case.get("unmet_h2_kg"),(float,int))
                or case["unmet_h2_kg"]<=0):
                raise IneligibleContractualH2Source("scientific negative flow, pressure or service control failed")
    return x


def native_BAFU_full_LCA_and_DCF_gate():
    x=audited_H2_supplier_qualification_result()
    return {
        "schema":"ptxlens.f3_dual_contract_2023_hourly_supplier_lcia_tea_gate.v1",
        "upstream_source_json_sha256":RESULT_SHA256,
        "original_2023_E_model_h2_shortage_source_verified":True,
        "2026_HNS_connection_contract_is_not_hydrogen_purchase_contract":True,
        "user_original_pyNEXUS_hydrogen_customer_site_location_known":False,
        "real_2023_network_customer_exit_connection_known":False,
        "actual_customer_exit_CDS_pressure_to_20_bar_absolute_verified":False,
        "supplier_separately_signed_purchase_shipper_nomination_verified":False,
        "source_8760h_producer_and_transport_firm_capacity_verified":False,
        "source_original_2023_hydrogen_assay_purity_at_end_use_known":False,
        "HNS_annexA_hhv_kWh_kg":x["Hynetwork_CSA_HHV_kWh_kg"],
        "real_customer_connection_total_peak_kWh_h":None,
        "full_original_h2_source_and_backup_storage_BOM_native_LCI":None,
        "matched_8760h_2023_modelled_h2_EOL_or_GWP":None,
        "source_backed_whole_plant_EUR_discounted_cashflow":None,
        "full_comparative_E_vs_ES_LCA_or_TEA_permitted":False,
    }
