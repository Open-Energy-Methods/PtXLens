"""Native BAFU 2026 database admission cannot be faked by F2 equipment mass.

Uses real Git-blob-pinned PUBLIC F2 source BOM, no licensed BAFU process bytes.
"""
import copy
import json
import pytest
from ptxlens import l3d_bafu_incremental_inventory_gate as m

def test_original_F2_vessel_reference_has_19_source_categories_in_both_modes():
    out=m.inspect_original()
    assert out["schema_version"]==m.SCHEMA
    assert len(out["ledger"])==38
    assert len({x["line_id"] for x in out["ledger"]})==19
    assert out["gross_reference_802_extra_empty_TypeI_vessels_kg"]==1924800
    assert out["usable_reference_902_extra_empty_TypeI_vessels_kg"]==2164800
    assert out["this_empty_equipment_mass_is_NOT_virgin_steel_consumption"] is True

def test_all_unverified_native_processes_and_manufacturer_items_remain_NULL():
    out=m.inspect_original()
    for item in out["ledger"]:
        assert item["native_BAFU_2026_dataset_process_UUID"] is None
        assert item["native_BAFU_2026_reference_product_UUID"] is None
        assert item["manufacturer_quotation_eur"] is None
        assert item["independent_material_composition_or_manufacturer_mass_kg"] is None
        assert item["measured_or_verified_incremental_LCIA_GWP_kgCO2e"] is None
        assert item["zero_impact_assumed"] is False
    for i in range(2):
        vessel=out["ledger"][19*i]
        assert vessel["reference_only_empty_equipment_mass_kg"]==[1924800,2164800][i]
        for other in out["ledger"][19*i+1:19*i+19]:
            assert other["reference_only_empty_equipment_mass_kg"] is None
            assert other["reference_vessel_count_ONLY_not_fabricated_bill_of_materials"] is None

def test_no_published_manufacturer_or_lca_result_from_sources():
    result=m.inspect_original()
    for field in ("source_known_equipment_mass_but_complete_native_LCI",
                  "manufacturer_actual_installed_system_BOM_and_price_verified",
                  "native_BAFU_2026_v11_all_38_foreground_links_connected",
                  "scientific_v1_0_release_allowed"):
        assert result[field] is False
    assert result["native_BAFU_2026_whole_station_manufacturing_emissions_kgCO2e"] is None
    with pytest.raises(m.NativeInventoryBlocked):
        m.verify_future_complete_native_mapping(result)

def test_malicious_fully_populated_metadata_does_not_fake_actual_native_provider():
    result=copy.deepcopy(m.inspect_original())
    result["manufacturer_actual_installed_system_BOM_and_price_verified"]=True
    result["native_BAFU_2026_v11_all_38_foreground_links_connected"]=True
    for item in result["ledger"]:
        item["native_BAFU_2026_dataset_process_UUID"]="fake-uuid"
        item["native_BAFU_2026_reference_unit"]="kg"
        item["native_mapping_status"]="NATIVE_DATASET_SOURCE_VERIFIED_AND_OPENLCA_RUN"
        item["measured_or_verified_incremental_LCIA_GWP_kgCO2e"]=0
    with pytest.raises(m.NativeInventoryBlocked,match="not implemented"):
        m.verify_future_complete_native_mapping(result)

def test_f2_source_git_blob_must_not_be_modified_to_claim_more_complete_lca(tmp_path):
    changed=tmp_path/"altered_f2.json"
    original=m.SOURCE.read_bytes()
    changed.write_bytes(original+b" ")
    with pytest.raises(m.NativeInventoryBlocked,match="drift"):
        m.inspect_original(changed)

def test_source_model_has_real_explicit_release_stop_on_bafu_mapping():
    doc=json.dumps(m.inspect_original(),sort_keys=True)
    assert '"scientific_v1_0_release_allowed": false' in doc
    assert "NULL" not in doc  # machine-readable native unknown is null, not string
    assert '"native_BAFU_2026_dataset_process_UUID": null' in doc
