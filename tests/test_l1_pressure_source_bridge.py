"""Original-source PtXFlex physical screen import tests.

E source is infeasible at 20t max and 20t usable with source-selected
Type I 200bar bank and RVO compressor. A past ideal E price is NOT
silently substituted, and the native BAFU v1 composite tank is NOT
cast as 2400kg empty steel-vessel manufacturing per unit.
"""
import copy
import json
import pytest

from ptxlens.l1_pressure_source_bridge import (
    PhysicallyIncompatibleEvidence,read_current,validate_l1_bridge
)


def test_actual_source_matched_pressure_gate_is_not_complete_comparison():
    x=read_current()
    assert x["source_original_E_zip_sha256"]=="069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051"
    assert x["common_original_model_H2_hourly_delivery_target_kg"]==16335279.317376738
    assert not x["physically_matched_E_vs_ES_environmental_comparison_eligible"]
    assert x["full_cradle_to_gate_GWP_kgCO2e_per_H2_kg"] is None
    assert x["full_LCOH_EUR_per_kg"] is None
    assert x["native_storage_manufacturing_GWP_kgCO2e"] is None
    for m in ("max_inventory","usable_service"):
        assert x["cases"][m]["E"]["annual_wholesale_settlement_eur2023"] is None
        assert x["cases"][m]["E_plus_S"]["annual_compressor_MWh"]>0


def test_infeasible_E_cannot_be_given_ideal_working_price():
    x=copy.deepcopy(read_current())
    x["cases"]["max_inventory"]["E"]["annual_wholesale_settlement_eur2023"]=25748907.19
    with pytest.raises(PhysicallyIncompatibleEvidence,match="infeasible E"):
        validate_l1_bridge(x)


def test_tank_nominal_gas_capacity_is_not_empty_equipment_mass():
    x=copy.deepcopy(read_current())
    x["cases"]["max_inventory"]["E"]["empty_reference_vessel_mass_kg"]=20000
    with pytest.raises(PhysicallyIncompatibleEvidence,match="source vessel empty mass"):
        validate_l1_bridge(x)


def test_native_composite_vehicle_BAFU_supplier_not_typeI_steel():
    x=copy.deepcopy(read_current())
    x["original_BAFU_vehicle_tank_compatible_with_TypeI_steel_reference"]=True
    with pytest.raises(PhysicallyIncompatibleEvidence,match="false process technology"):
        validate_l1_bridge(x)


def test_unknown_manufacturer_BOM_is_not_zero():
    x=copy.deepcopy(read_current())
    x["manufacturer_steel_grade_wall_material_breakdown_kg"]=0
    with pytest.raises(PhysicallyIncompatibleEvidence,match="cannot establish metallurgical BOM"):
        validate_l1_bridge(x)


def test_unverified_native_manufacturing_GWP_cannot_be_assigned_zero():
    x=copy.deepcopy(read_current())
    x["native_storage_manufacturing_GWP_kgCO2e"]=0
    with pytest.raises(PhysicallyIncompatibleEvidence,match="unverified whole-plant"):
        validate_l1_bridge(x)


def test_wrong_source_derived_artifact_sha_rejected():
    x=copy.deepcopy(read_current())
    x["upstream_derived_json_sha256"]="0"*64
    with pytest.raises(PhysicallyIncompatibleEvidence,match="unverified derived 2023"):
        validate_l1_bridge(x)
