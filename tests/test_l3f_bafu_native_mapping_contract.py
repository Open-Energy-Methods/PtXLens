"""L3-F native BAFU 2026 v1.1 evidence metadata, no false GWP."""
import hashlib
import json
import zipfile

import pytest

from ptxlens import l3f_bafu_native_mapping_contract as m
from ptxlens.l3d_bafu_incremental_inventory_gate import NativeInventoryBlocked


def test_real_source_19_F2_categories_and_matched_service_per_year():
    d=m.build()
    assert d["schema_version"]==m.SCHEMA
    assert d["matched_service_H2_daily_kg"]==30000.
    assert [x["delivered_H2_kg"] for x in d["year_specific_matched_hydrogen_functional_units"]]==[
        10950000.,10980000.
    ]
    rows=d["separate_19_manufacturer_and_provider_flow_requirements"]
    assert len(rows)==19
    assert len({r["original_F2_source_BOM_line_id"] for r in rows})==19
    assert all(r["actual_fabricated_material_INPUT_kg_not_empty_equipment"] is None for r in rows)
    assert all(r["native_openLCA_process_UUID"] is None for r in rows)
    assert d["original_native_BAFU_2026_v11_incremental_total_kgCO2e"] is None
    assert d["scientific_v1_0_native_LCA_gate_passed"] is False


def test_BAFU_gwp_must_NOT_be_inferred_from_electricity_signs():
    d=m.build()
    op=d["separate_year_specific_operational_energy"]
    assert op[0]["delta_annual_net_grid_import_MWh"]>0
    assert op[1]["delta_annual_net_grid_import_MWh"]<0
    assert all(x["CO2e_delta_not_inferable_from_energy_or_prices"] for x in op)
    assert d["hourly_relevant_import_export_emission_factors_authenticated"] is False
    assert d["environmental_superiority_accepted"] is False


def test_source_BAFU_blank_contract_incomplete_not_zero_impacts():
    r=m.audit_proposed_mapping_structure(m.build())
    assert r["original_F2_categories"]==19
    assert len(r["incomplete_source_specific_manufacturer_native_exchange_entries"])>=19
    assert r["full_native_BAFU_LCIA_proven"] is False
    assert "NOT LCIA" in m.markdown(m.build())


def test_native_provider_unit_for_nominal_H2_capacity_is_rejected():
    d=m.build()
    d["separate_19_manufacturer_and_provider_flow_requirements"][0][
        "native_openLCA_exchange_denominator"]="kg_h2_nominal_capacity"
    r=m.audit_proposed_mapping_structure(d)
    assert any("cannot_be_used_as_virgin_steel_input" in z for z in
               r["fundamentally_incompatible_units_or_unsupported_LCIA_claims"])


def test_actual_manufactured_steel_flow_not_derivable_from_empty_vessel_mass():
    d=m.build()
    d["separate_19_manufacturer_and_provider_flow_requirements"][0][
        "native_openLCA_exchange_denominator"]="kg_empty_equipment"
    r=m.audit_proposed_mapping_structure(d)
    assert r["full_native_BAFU_LCIA_proven"] is False
    assert any("reference_unit_cannot_be_used" in z for z in
               r["fundamentally_incompatible_units_or_unsupported_LCIA_claims"])


def test_fully_filled_fake_metadata_does_not_establish_real_native_LCIA():
    d=m.build()
    for r in d["separate_19_manufacturer_and_provider_flow_requirements"]:
        r["actual_fabricated_material_INPUT_kg_not_empty_equipment"]=100.
        r["source_qualifying_independent_OEM_material_receipt_sha256"]="a"*64
        r["native_openLCA_process_UUID"]="123e4567-e89b-42d3-a456-426614174000"
        r["native_openLCA_reference_flow_UUID"]="123e4567-e89b-42d3-a456-426614174001"
        r["native_openLCA_exchange_denominator"]="kg_steel_input"
        r["native_openLCA_exchange_amount_in_reference_unit"]=100.
    x=m.audit_proposed_mapping_structure(d)
    assert x["incomplete_source_specific_manufacturer_native_exchange_entries"]==[]
    assert x["full_native_BAFU_LCIA_proven"] is False
    assert x["real_manufacturer_foreground_verified"] is False


def test_false_manual_LCIA_certification_is_flagged():
    d=m.build()
    d["separate_19_manufacturer_and_provider_flow_requirements"][0][
        "process_mapping_certified"]=True
    x=m.audit_proposed_mapping_structure(d)
    assert any("manual_claim" in k for k in
               x["fundamentally_incompatible_units_or_unsupported_LCIA_claims"])


def test_missing_original_source_BOM_line_cannot_be_silently_omitted():
    d=m.build()
    d["separate_19_manufacturer_and_provider_flow_requirements"].pop()
    with pytest.raises(NativeInventoryBlocked):
        m.audit_proposed_mapping_structure(d)


def test_optional_local_private_zolca_hash_is_not_native_provider_validation(tmp_path):
    p=tmp_path/"private_BAFU_2026_v11.zolca"
    with zipfile.ZipFile(p,"w") as z:
        z.writestr("not-a-native-process.txt","synthetic")
    sha=hashlib.sha256(p.read_bytes()).hexdigest()
    r=m.fingerprint_local_zolca(p,expected_sha256=sha)
    assert r["local_private_original_zolca_SHA256"]==sha
    assert r["archive_members_count_NOT_process_count"]==1
    assert r["original_BAFU_2026_v11_version_or_native_process_UUIDs_proven"] is False
    assert r["native_openLCA_product_system_material_LCIA_replayed"] is False
    assert "private_BAFU_2026_v11" not in json.dumps(r)


def test_different_SHA_and_bad_native_archive_rejected(tmp_path):
    p=tmp_path/"data.zolca"
    with zipfile.ZipFile(p,"w") as z:z.writestr("synthetic.txt","text")
    with pytest.raises(NativeInventoryBlocked):
        m.fingerprint_local_zolca(p,expected_sha256="0"*64)
    p.write_bytes(b"not a real zolca")
    with pytest.raises(NativeInventoryBlocked,match="ZIP"):
        m.fingerprint_local_zolca(p)
