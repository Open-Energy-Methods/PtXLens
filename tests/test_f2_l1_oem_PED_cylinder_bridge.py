"""Source-verified heiserTEC Type I PED 50L 330bar OEM mass alternative, not
200bar Type I 1.8m3 paper vessel, not 210bar 36x87L stationary bundle and
never 12x50L 935kg TPED mobile bundle. NEN EN17533 individual cylinders
do NOT certify a complete manifolded pressure assembly.
"""
import json
import math
import pytest
import ptxlens.f2_l1_oem_PED_cylinder_bridge as x


def test_distinct_real_330bar_oem_cylinder_weight_source_and_ineligible_native_LCI():
    r=x.generate_OEM_crosscheck()
    assert r["schema_version"]==x.SCHEMA
    assert r["original_2023_source_operating_hydrogen_is_modelled"]
    assert r["source_F2_OEM_50L_json_sha256"]==x.SRC_SHA256
    assert r["EN17533_2025_standards_for_cylinder_not_manifold_or_piping"]
    assert r["OEM_330bar_product_not_2023_site_certified_at_200bara"]
    assert r["two_distinct_typeI_cylinder_reference_products_not_interchangeable"]
    assert not r["financial_and_climate_compare_release_eligible"]
    assert set(r["scenarios"])=={"max_inventory","usable_service"}


@pytest.mark.parametrize("mode,cnt,kg,other_cnt,other_kg",[
  ("max_inventory",28878,2469069.,802,1924800.),
  ("usable_service",32468,2776014.,902,2164800.)
])
def test_real_oem_specific_product_dimensionally_sound_and_separate_from_2023_reference(
        mode,cnt,kg,other_cnt,other_kg):
    r=x.generate_OEM_crosscheck()["scenarios"][mode]
    assert r["OEM_heisertec_330bar_PED_50L_reference_at_derated_200bara_313K_additional_cylinders"]==cnt
    assert r["OEM_heisertec_330bar_PED_50L_reference_at_derated_200bara_313K_additional_empty_hardware_kg"]==kg
    assert r["IJHE_200bar_TypeI_1_8m3_literature_additional_vessels"]==other_cnt
    assert r["IJHE_200bar_TypeI_1_8m3_literature_additional_empty_hardware_kg"]==other_kg
    assert r["OEM_330bar_is_separate_pressure_rating_and_50L_geometry_not_a_vendor_200bar_station_offer"]
    assert not r["same_stationary_210bar_COSMOS_36x87L_bundle_empty_mass_known"]
    assert r["published_50L_PED_cylinder_standalone_mass_must_not_be_used_for_36x87L_COSMOS_modules"]
    assert r["OEM_200bar_derated_313K_cycling_not_site_certified"]
    assert r["steel_raw_input_from_weight_without_materials_fabrication_provider_NOT_allowed"]
    assert r["original_F3C_same_hour_source_target_SHA256"]!=None
    assert r["full_native_BAFU2026_v11_co2e_kg"] is None
    assert r["whole_plant_EUR2023_discounted_cost"] is None


@pytest.mark.parametrize("field,bogus",[
    ("manufacturer_oem_product_330bar_nominal_pressure_not_same_as_200bar_screen",False),
    ("standard_for_individual_cylinders_not_manifolded_assemblies",False),
    ("manufacturer_50L_85_5kg_is_H2_pressure_cylinder_not_mobile_module_frame",False),
    ("whole_plant_comparison_release_ready",True),
])
def test_sha_locked_manufacturer_data_cannot_be_relabelled_as_BAFU_steel_or_Ped_site_certification(tmp_path,monkeypatch,field,bogus):
    obj=json.loads(x.SRC.read_text())
    obj[field]=bogus
    p=tmp_path/"changed.json";p.write_text(json.dumps(obj))
    monkeypatch.setattr(x,"SRC",p)
    with pytest.raises(x.InvalidOEMMassEvidence,match="unregistered source manufacturer"):
        x.verify_OEM_source()


def test_intact_source_rejected_if_vendor_BOM_mysteriously_claimed_completed(monkeypatch):
    original=x.verify_OEM_source()
    original["modeled_source_inventory_modes"]["max_inventory"]["actual_completed_manufacturer_BOM"]=True
    monkeypatch.setattr(x,"verify_OEM_source",lambda: original)
    with pytest.raises(x.InvalidOEMMassEvidence,match="falsely approved full hardware"):
        x.generate_OEM_crosscheck()
