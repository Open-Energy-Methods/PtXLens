"""PtXLens L1 source-hash verified stationary Type I bank foreground intake.

Imports the genuine PtXFlex original F2 Type I literature-vessel 200bar
incremental empty equipment mass; verifies 20t E vs 40t E+S count/volume/
EOS working-heel and source-2023 F3-C modeled duty.

This is an engineering **requirement ledger** ONLY. No manufacturer-qualified
steel grade, heat treatment, rack/manifold/cooler/compressor mass, vendor quote
or installed site is present. Cannot lawfully substitute BAFU:2026 vehicle
composite H2-storage process per kg H2 for kg of stationary steel equipment.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from .f3c_common_service_bridge import compare_all_modes,REGISTERED as ORIGINAL_F3C_SHA

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/"data/results/F2_L1_2023_source_incremental_20t_to_40t_stationary_typeI_200bar_BOM_SCOPE_NOT_complete_native_LCI.json"
REGISTRY=ROOT/"research/F2_L1_STATIONARY_TYPEI_OEM_AND_STANDARDS_SOURCE_REGISTER_v1.json"
SOURCE_SHA256="1315d1181b9d1eab6d3368425c9571dbe295c3360935d2972403bf3c60e2dc47"
SOURCE_SCHEMA="ptxflex.f2_l1_typeI_200bar_incremental_stationary_h2_equipment_requirements.v1"
SCHEMA="ptxlens.f2_l1_typeI_stationary_eu_pressure_equipment_foreground_E20t_ES40t_source_gate.v1"
MISSING_IDS={
 "steel_alloy_material_grade_and_inclusions","rack_frames_and_anchors",
 "high_pressure_headers_and_interconnects","isolation_valves_and_actuators",
 "non_return_valves_and_filters","pressure_relief_and_vent_stack",
 "pressure_regulation_delivery_header","compressor_recips_and_seals",
 "compressor_motor_drive_VFD","intercooler_aftercooler_heat_exchange",
 "cooling_pumps_and_fans","gas_quality_dryer_and_sample_system",
 "pressure_temperature_flow_metering","hydrogen_leak_detection_ESD_ATEX",
 "civil_foundations_and_construction","inspections_fatigue_cycle_testing",
 "installation_and_transport","decommission_and_EOL"
}
MISSING_LCI_NATIVE_SOURCE="BAFU:2026 v1.1 Type I stationary alloy-specific, manufacturer-technosphere linked foreground not yet created"
INCOMPATIBLE_VEHICLE_LCI_UUID="b4739ad2-aa38-368d-8ada-63f5417c8b55"


class InadmissibleStationaryStorageLCI(ValueError):pass


def required(x,message):
    if not x:raise InadmissibleStationaryStorageLCI(message)


def load_f2_bom(path=SOURCE):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:
        raise InadmissibleStationaryStorageLCI("unrecognized / modified original PtXFlex source-2023 physical Type I bank H2 hardware register")
    x=json.loads(raw)
    if x.get("schema_version")!=SOURCE_SCHEMA or x.get("modelled_original_PyNEXUS_year")!=2023:
        raise InadmissibleStationaryStorageLCI("wrong Type I engineering hardware vs 2023 source time model")
    require_all=("two_storage_capacity_semantics_not_combined",
                 "reported_reference_vessel_mass_is_empty_equipment_not_hydrogen_or_raw_steel_input",
                 "heiserTEC_stationary_PED_vs_mobile_TPED_confusion_rejected",
                 "no_vendor_site_validated_cylinder_fatigue_P_and_ID_or_BOM")
    for k in require_all:required(x.get(k) is True,"source scope control not retained: "+k)
    required(x.get("full_project_LCA_TE_A_allowed") is False,
             "source reference shells cannot be asserted to be full native BAFU physical LCA")
    ref=x.get("source_evidence_refs",{})
    required(set(ref)=={"peer_reviewed_200bar_IJHE","actual_210bar_stationary_PED_product",
                        "EIGA_2024_safety_equipment","industrial_H2_compressor_family",
                        "EU_pressure_equipment_directive"},
             "source OEM PED and EU safety equipment evidence missing")
    conditions=x.get("screening_conditions",{})
    required(conditions.get("temperature_K")==313 and
             conditions.get("max_storage_pressure_bar_absolute")==200 and
             conditions.get("minimum_H2_delivery_pressure_bar_absolute")==20 and
             conditions.get("rating_reinterpreted_as_absolute_for_screening_only") is True,
             "unsupported source vessel bar pressure/cycle conditions")
    registry=json.loads(REGISTRY.read_text())
    required(registry.get("schema_version")=="oem.ptx.f2_l1_stationary_h2_equipment_source_register.v1" and
             registry.get("installation_BOM_complete") is False and
             registry.get("native_compatible_BAFU2026_v11_product_link_verified") is False and
             registry.get("assumed_steel_manufacturing_kgCO2e_per_kg") is None,
             "unapproved manufacturer/life-cycle source mismatch")
    r={t.get("id"):t for t in registry.get("source_references",[])}
    required(r["heisertec_cosmos_stationary_2026"]["vendor_example"]["stationary_module_nominal_empty_mass_kg"] is None and
             r["heisertec_cosmos_mobile_not_stationary_mass"]["mobile_example"]["nominal_empty_mobile_complete_bundle_kg"]==935 and
             r["heisertec_cosmos_mobile_not_stationary_mass"]["permanently_excluded_from_200bar_stationary_typeI_LCI_mass_transfer"] is True,
             "mobile TPED bundle mass mistakenly used as stationary PED Type I steel inventory")
    return x


def source_mode(mode,doc,original_f3c):
    entry=doc["modes"].get(mode)
    required(isinstance(entry,dict),"missing separately reconciled 20t/40t source inventory interpretation")
    a=entry["source_case_E_20t"]
    b=entry["source_case_EplusS_40t"]
    inc=entry["incremental_only_research_sensitivity"]
    req=entry["required_incremental_system_foreground_BOM"]
    required(a["source_model_capacity_kg"]==20000 and b["source_model_capacity_kg"]==40000,
             "wrong original E/ES source kg H2 storage capacity")
    required(a["source_capacity_semantics"]==b["source_capacity_semantics"]==mode,
             "2023 gross vs usable H2 inventory semantic confusion")
    delta=b["reference_vessels"]-a["reference_vessels"]
    equipment_mass=float(inc["net_additional_published_empty_vessel_equipment_mass_kg"])
    required(delta==inc["net_additional_published_reference_vessel_count"] and
             delta>0 and equipment_mass==delta*2400.0 and
             a["paper_empty_vessels_total_equipment_kg"]==a["reference_vessels"]*2400 and
             b["paper_empty_vessels_total_equipment_kg"]==b["reference_vessels"]*2400,
             "peer-reviewed 2400kg empty vessel equipment mass or 20t to 40t count not conserved")
    required(inc["source_vessel_mass_is_NOT_virgin_steel_input_kg"] is True and
             inc["incremental_native_BAFU_storage_CO2e_kg"] is None and
             inc["incremental_installed_storage_CAPEX_eur"] is None and
             inc["incremental_installed_compressor_equipment_mass_kg"] is None and
             inc["incremental_cooling_equipment_mass_kg"] is None,
             "source empty manufactured shell cannot be treated as full virgin steel LCIA or final GWP")
    required(len(req)==19 and req[0]["line_id"]=="typeI_200bar_bare_reference_vessels" and
             {t["line_id"] for t in req[1:]}==MISSING_IDS,
             "source manufacturer safety/auxiliary component scope not complete")
    required(req[0]["empty_mass_kg"]==equipment_mass and
             req[0]["raw_virgin_steel_mass_kg"] is None and
             req[0]["evidence_class"]=="PEER_REVIEWED_PER_VESSEL_EMPTY_EQUIPMENT_MASS_NOT_OEM_SPEC",
             "lit per-vessel reference confused with manufacturing material inventory")
    for x in req[1:]:
        required(x["quantity"] is None and x["empty_mass_kg"] is None and
                 x["manufacturer_quote_eur"] is None and
                 x["contribution_to_full_LCI"]=="UNRESOLVED_NONZERO_NOT_ASSUMED_ZERO",
                 "unknown foreground equipment LCI incorrectly zero-filled or fabricated")
    vendor=entry["commercial_manufacturer_candidate"]
    required(vendor["OEM"]=="heiserTEC" and vendor["stationary_module_empty_mass_kg"] is None and
             vendor["mobile_TPED_935kg_reference_may_be_applied_to_stationary_PED"] is False and
             vendor["validity_of_using_210bar_vendor_module_as_certified_200bara_313K_installation"] is False and
             vendor["OEM_commercial_bare_module_quote_eur"] is None,
             "stationary heiserTEC 210bar catalogue cannot turn into a certified 200bar priced unit")
    required(entry["unknown_non_vessel_equipment_total_mass_kg"] is None and
             entry["complete_source_fabrication_and_installed_mass_kg"] is None and
             entry["complete_manufacturer_warrantied_typeI_bank_BOM"] is False and
             entry["BAFU2026_v11_standalone_typeI_native_LCI_created"] is False and
             entry["full_LCA_or_utility_production_cost_ready"] is False,
             "missing equipment, LCIA or CAPEX suddenly counted as complete")
    for c in ("E","E_plus_S"):
        audited=entry["2023_source_case_operations_not_station_hardware_sizing"][c]
        required(audited["source_2023_optimized_hourly_H2_service_SHA256"]==
                 original_f3c["modes"][mode]["reference_common_hourly_H2_float64_sha256"] and
                 audited["source_2023_real_vessel_installation_not_approved"] is True,
                 "source equipment loads falsely disconnected from verified same-hour F3C source model")
    eos_min=a["residual_heel_kg_at_assumed_20bara_313K"]/a["reference_vessels"]
    eos_min_es=b["residual_heel_kg_at_assumed_20bara_313K"]/b["reference_vessels"]
    required(0<eos_min<10 and math.isclose(eos_min,eos_min_es,abs_tol=1e-7),
             "source Type I 20bar EOS heel per reference cylinder not identical")
    required(abs((b["withdrawable_h2_between_200_and_20_bara_kg"]-
                  a["withdrawable_h2_between_200_and_20_bara_kg"])-
                 inc["extra_hydrogen_working_capacity_due_to_ceiling_kg"])<1e-6,
             "extra usable hydrogen 20bar pressure swing mass not conserved")
    return {
       "capacity_semantics":mode,
       "source_reference_vessels_E20t":a["reference_vessels"],
       "source_reference_vessels_EplusS40t":b["reference_vessels"],
       "incremental_REFERENCE_EMPTY_MANUFACTURED_VESSEL_COUNT":delta,
       "incremental_REFERENCE_EMPTY_MANUFACTURED_VESSEL_MASS_kg":equipment_mass,
       "reference_typeI_steel_vessel_kg_each":2400,
       "this_is_NOT_verified_STEEL_MATERIAL_input_kg":True,
       "steel_grade_composition_and_recycled_fraction_unknown":True,
       "incremental_total_manufacturing_and_installed_mass_kg":None,
       "incremental_BOP_manifold_compressor_cooler_mass_kg":None,
       "manufacturer_stationary_module_mass_kg":None,
       "reference_helium_or_gas_heel_kg_that_is_not_manufacturing_mass":inc["incremental_heel_gas_stock_kg"],
       "reference_20bar_to_200bar_pressure_swing_extra_usable_H2_kg":inc["extra_hydrogen_working_capacity_due_to_ceiling_kg"],
       "unquantified_equipment_scope_item_count":len(MISSING_IDS),
       "unquantified_equipment_scope_ids_sorted":sorted(MISSING_IDS),
       "real_stationary_OEM_HEISERTEC_PED_210bar_module_rated_mass_not_specified":True,
       "real_Burckhardt_compressor_relevant_family_but_no_30_to_200bar_2200kg_h_vendor_quote":True,
       "prohibited_BAFU_vehicle_composite_tank_process_UUID":INCOMPATIBLE_VEHICLE_LCI_UUID,
       "source_common_H2_hourly_target_SHA256":original_f3c["modes"][mode]["reference_common_hourly_H2_float64_sha256"],
       "original_2023_same_service_wholesale_saving_eur_without_equip_CAPEX":original_f3c["modes"][mode]["EplusS_2023_wholesale_saving_eur"],
       "native_compatible_BAFU2026_v11_typeI_manufacturing_LCI":None,
       "installed_incremental_2023_eur_cost_discounted_or_NPV":None,
       "full_equipment_GWP_or_H2_LCOH_eligible":False,
    }


def import_f2_bom():
    f2=load_f2_bom()
    f3=compare_all_modes()
    required(f3.get("native_BAFU_complete_LCA_and_discounted_LCOH_missing") is True,
             "foreign F3-C bridge erroneously claimed complete process system")
    modes=f2.get("modes")
    required(isinstance(modes,dict) and set(modes)=={"max_inventory","usable_service"},
             "unregistered H2 reference capacity semantics")
    return {
       "schema_version":SCHEMA,
       "programme":"OEM-PTX-2026-01",
       "source_year_original_PyNEXUS_H2_model":2023,
       "F2_source_SHA256":SOURCE_SHA256,
       "original_f3c_source_results":ORIGINAL_F3C_SHA,
       "common_hourly_original_E_reduced_service_is_feasible_not_global_maximum":True,
       "real_EU_PED_steel_module_manufacturer_found_but_no_stationary_module_empty_mass":True,
       "only_known_REFERENCE_EMPTY_EQUIPMENT_mass_not_virgin_steel_input":True,
       "number_of_missing_undocumented_foreground_equipment_classes_per_mode":len(MISSING_IDS),
       "all_required_components_published_as_scope_but_not_a_complete_quoted_BOM":True,
       "cannot_characterize_from_wrong_vehicle_composite_LCI":True,
       "source_bafu_v1_vehicle_composite_process_UUID_unfit_for_stationary_TypeI":INCOMPATIBLE_VEHICLE_LCI_UUID,
       "source_true_stationary_typeI_manufacturer_compatible_native_BAFU_v11_flow_UUID":None,
       "source_GWP100_kgCO2e_per_kg_empty_stainless_or_carbon_vessel_from_validated_LCI":None,
       "no_installed_compression_or_BOP_or_cooling_source_quantity":True,
       "full_L2_LCIA_per_kg_H2":None,
       "full_L3_LCOH_EUR_per_kg_H2":None,
       "source_manufacturer_ped_site_conformity":False,
       "F2_L1_full_equipment_native_LCA_release_PASSED":False,
       "modes":{mode:source_mode(mode,f2,f3) for mode in ("max_inventory","usable_service")},
    }
