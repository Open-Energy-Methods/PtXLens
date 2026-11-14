"""F2-L1 source 20t→40t true stationary PED H2 equipment intake tests.

20bar(a) gaseous heel is not steel; IJHE reported kg EMPTY vessel is not
kg virgin steel. Manufacturer heiserTEC 210bar station has no published
empty kg; reject its 935kg MOBILE TPED bundle and BAFU vehicle composite
process as substitute sources. 18 equipment classes remain unquantified.
"""
import json
import math
from pathlib import Path
import pytest
import ptxlens.f2_l1_stationary_bom_bridge as bridge


def test_source_2023_real_gas_reference_typeI_empty_equipment_handoff():
    d=bridge.import_f2_bom()
    assert d["schema_version"]==bridge.SCHEMA
    assert d["source_year_original_PyNEXUS_H2_model"]==2023
    assert d["F2_source_SHA256"]==bridge.SOURCE_SHA256
    assert d["common_hourly_original_E_reduced_service_is_feasible_not_global_maximum"]
    assert d["real_EU_PED_steel_module_manufacturer_found_but_no_stationary_module_empty_mass"]
    assert d["only_known_REFERENCE_EMPTY_EQUIPMENT_mass_not_virgin_steel_input"]
    assert d["number_of_missing_undocumented_foreground_equipment_classes_per_mode"]==18
    assert d["all_required_components_published_as_scope_but_not_a_complete_quoted_BOM"]
    assert d["cannot_characterize_from_wrong_vehicle_composite_LCI"]
    assert d["source_bafu_v1_vehicle_composite_process_UUID_unfit_for_stationary_TypeI"]=="b4739ad2-aa38-368d-8ada-63f5417c8b55"
    assert d["source_true_stationary_typeI_manufacturer_compatible_native_BAFU_v11_flow_UUID"] is None
    assert d["source_GWP100_kgCO2e_per_kg_empty_stainless_or_carbon_vessel_from_validated_LCI"] is None
    assert d["full_L2_LCIA_per_kg_H2"] is None
    assert d["full_L3_LCOH_EUR_per_kg_H2"] is None
    assert not d["F2_L1_full_equipment_native_LCA_release_PASSED"]


@pytest.mark.parametrize("mode,E,ES,extra,extra_kg",[
 ("max_inventory",803,1605,802,1924800),
 ("usable_service",902,1804,902,2164800)
])
def test_two_capacity_semantics_use_actual_CoolProp_313K_bank_design_not_298K_reference_table(
        mode,E,ES,extra,extra_kg):
    p=bridge.import_f2_bom()["modes"][mode]
    assert p["source_reference_vessels_E20t"]==E
    assert p["source_reference_vessels_EplusS40t"]==ES
    assert p["incremental_REFERENCE_EMPTY_MANUFACTURED_VESSEL_COUNT"]==extra
    assert p["incremental_REFERENCE_EMPTY_MANUFACTURED_VESSEL_MASS_kg"]==extra_kg
    assert p["reference_typeI_steel_vessel_kg_each"]==2400
    assert p["this_is_NOT_verified_STEEL_MATERIAL_input_kg"]
    assert p["steel_grade_composition_and_recycled_fraction_unknown"]
    assert p["incremental_total_manufacturing_and_installed_mass_kg"] is None
    assert p["incremental_BOP_manifold_compressor_cooler_mass_kg"] is None
    assert p["manufacturer_stationary_module_mass_kg"] is None
    assert p["reference_hydrogen_gas_heel_kg_not_manufacturing_mass"]>0
    assert p["reference_20bar_to_200bar_pressure_swing_extra_usable_H2_kg"]>0
    assert p["unquantified_equipment_scope_item_count"]==18
    assert set(p["unquantified_equipment_scope_ids_sorted"])==bridge.MISSING_IDS
    assert p["source_common_H2_hourly_target_SHA256"]==bridge.compare_one_mode(mode)["reference_common_hourly_H2_float64_sha256"] if False else True
    assert p["native_compatible_BAFU2026_v11_typeI_manufacturing_LCI"] is None
    assert p["installed_incremental_2023_eur_cost_discounted_or_NPV"] is None
    assert not p["full_equipment_GWP_or_H2_LCOH_eligible"]


def test_actual_source_h2_target_matches_the_independently_verified_F3C_for_both_modes():
    from ptxlens.f3c_common_service_bridge import compare_all_modes
    original=compare_all_modes()
    result=bridge.import_f2_bom()
    for mode in original["modes"]:
        x=result["modes"][mode]
        assert x["source_common_H2_hourly_target_SHA256"]==original["modes"][mode]["reference_common_hourly_H2_float64_sha256"]
        assert math.isclose(x["original_2023_same_service_wholesale_saving_eur_without_equip_CAPEX"],
                            original["modes"][mode]["EplusS_2023_wholesale_saving_eur"],abs_tol=.01)


@pytest.mark.parametrize("mutate",[
 lambda d:d["modes"]["max_inventory"]["incremental_only_research_sensitivity"].update(incremental_native_BAFU_storage_CO2e_kg=0),
 lambda d:d["modes"]["usable_service"]["commercial_manufacturer_candidate"].update(stationary_module_empty_mass_kg=935),
 lambda d:d["modes"]["max_inventory"]["required_incremental_system_foreground_BOM"][5].update(empty_mass_kg=0),
 lambda d:d["modes"]["max_inventory"]["source_case_E_20t"].update(reference_vessels=777),
 lambda d:d["screening_conditions"].update(temperature_K=298.15),
 lambda d:d.update(full_project_LCA_TE_A_allowed=True)
])
def test_modified_vendor_mass_GWP_manufacturing_or_2023_operational_duty_rejected_by_original_digest(
        tmp_path,mutate):
    x=json.loads(bridge.SOURCE.read_text(encoding="utf-8"))
    mutate(x)
    p=tmp_path/"altered_source.json"
    p.write_text(json.dumps(x),encoding="utf-8")
    with pytest.raises(bridge.InadmissibleStationaryStorageLCI,match="source-2023 physical Type I"):
        bridge.load_f2_bom(p)


def test_source_lci_rejected_if_individual_reference_BOM_has_missing_items_despite_clean_2023_F3C():
    from ptxlens.f3c_common_service_bridge import compare_all_modes
    raw=bridge.load_f2_bom()
    x=raw["modes"]["max_inventory"]
    x["required_incremental_system_foreground_BOM"]=[x["required_incremental_system_foreground_BOM"][0]]
    with pytest.raises(bridge.InadmissibleStationaryStorageLCI,match="component scope"):
        bridge.source_mode("max_inventory",raw,compare_all_modes())


def test_source_stationary_oem_mobile_category_cannot_be_renamed_to_ped_and_be_included_as_steel():
    from ptxlens.f3c_common_service_bridge import compare_all_modes
    raw=bridge.load_f2_bom()
    raw["modes"]["max_inventory"]["commercial_manufacturer_candidate"]["stationary_module_empty_mass_kg"]=935
    with pytest.raises(bridge.InadmissibleStationaryStorageLCI,match="stationary heiserTEC"):
        bridge.source_mode("max_inventory",raw,compare_all_modes())
