"""Scientific source-unit gate: a high-pressure vehicle tank per kg H2
capacity is not a published empty Type I steel vessel manufacturing recipe.

Full licensed EcoSpold auditing requires the authorized PRIVATE original
BAFU v1 ZIP. Public CI only verifies derived source-safe metadata and
refuses fabricated/altered source files; it never distributes source LCI.
"""
from pathlib import Path
import json
import os
import pytest

from ptxlens.bafu_tank_process_audit import (
 BAFU_TANK_UUID,BAFU_SOURCE_V1_ZIP_SHA256,PhysicalSourceMismatch,
 inspect_original_bafu_tank,
)

DERIVED=Path(__file__).resolve().parents[1]/"data/results/BAFU2026_v1_storage_tank_source_unit_mismatch_audit.json"


def source():
    return json.loads(DERIVED.read_text(encoding="utf-8"))


def test_actual_original_source_functional_unit_is_not_steel_mass():
    d=source()
    assert d["source_reference_uuid"]==BAFU_TANK_UUID
    assert d["source_original_sha256"]==BAFU_SOURCE_V1_ZIP_SHA256
    assert d["source_reference_unit"]=="kg"
    assert "per 1 kg hydrogen" in d["source_general_comment_reference_basis"]
    assert "road" in d["source_local_subcategory"]
    assert d["named_material_inputs_kg_per_ambiguous_reference_unit"]["Carbon fiber, weaved, at factory"]==7.14
    assert d["material_inputs_sum_kg_per_ambiguous_reference_unit"]==12.6
    assert d["source_can_be_used_as_native_GWP_per_kg_stationary_Type_I_steel"] is False
    assert d["mapped_one_kg_source_to_one_kg_empty_vessel"] is False
    assert d["full_plant_E_or_ES_LCA_complete"] is False


def test_v1_bafu_does_not_certify_v11_native_supplier():
    d=source()
    assert d["native_BAFU_v11_tank_provider_exchanges_verified"] is False
    assert d["missing_equipment_impact_counted_as_zero"] is False
    assert d["mass_basis_ambiguous_exported_unit"] is True


def test_tampered_not_source_zip_is_refused(tmp_path):
    p=tmp_path/"fabricated_technosphere.zip"
    p.write_bytes(b"TEST_ONLY_UNKNOWN_SOURCE_BYTES")
    with pytest.raises(PhysicalSourceMismatch,match="SHA256"):
        inspect_original_bafu_tank(p)


def test_private_original_zip_reaudit_when_authorized_location_is_supplied():
    private=os.environ.get("BAFU_ORIGINAL_PRIVATE_V1_ZIP")
    if not private:
        pytest.skip("real restricted original file not in GitHub CI; set local BAFU_ORIGINAL_PRIVATE_V1_ZIP")
    actual=inspect_original_bafu_tank(private)
    assert actual["source_reference_uuid"]==source()["source_reference_uuid"]
    assert actual["named_material_inputs_kg_per_ambiguous_reference_unit"]==source()["named_material_inputs_kg_per_ambiguous_reference_unit"] if "named_material_inputs_kg_per_ambiguous_reference_unit" in actual else actual["named_input_materials_kg_per_unit_of_ambiguous_reference"]==source()["named_material_inputs_kg_per_ambiguous_reference_unit"]
