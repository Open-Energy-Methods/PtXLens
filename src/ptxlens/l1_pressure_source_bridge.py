"""PtXLens scientific source-boundary gate for actual PtXFlex F2/F3 evidence.

Requires physical vessel reference mass and H2 gas heel to retain their
own units. Rejects fake E numerical totals when the source E pressure
configuration was infeasible. Does NOT reconstruct arbitrary BAFU native
factors from a generic tank name, nor manufacture compressor/cooler BOM.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path

PATH=Path(__file__).resolve().parents[2]/"data/results/F3_2023_original_pressure_screen_PtXLens_L1_source_bridge.json"


class PhysicallyIncompatibleEvidence(ValueError):
    pass


def validate_l1_bridge(obj):
    if obj["schema_version"]!="ptxlens.l1_f3_2023_source_pressure_system_bom_and_compatibility.v0.1":
        raise PhysicallyIncompatibleEvidence("wrong physical-science source data schema")
    if obj["upstream_derived_json_sha256"]!="a8240205a15d905ffe48e8443a69c227b9bfe1b1788229b67b6daeac218a74c1":
        raise PhysicallyIncompatibleEvidence("unverified derived 2023 source artifact")
    if obj["technology_source_doi"]!="10.1016/j.ijhydene.2025.152849":
        raise PhysicallyIncompatibleEvidence("physical pressure vessel lacks source")
    if obj["source_original_E_zip_sha256"]!="069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051":
        raise PhysicallyIncompatibleEvidence("original E changed")
    if obj["source_original_EplusS_zip_sha256"]!="cd4101fe62c3f1b8aa2d7508d3651d2fee40d2bafe6d5b87e40d5f4d055070f9":
        raise PhysicallyIncompatibleEvidence("original E+S changed")
    if obj["source_compressor_charge_electrical_kwh_per_kg"]<=0 or obj["full_original_nominal_H2_demand_kg"]!=18250000:
        raise PhysicallyIncompatibleEvidence("invalid original service or compression")
    if obj["manufacturer_steel_grade_wall_material_breakdown_kg"] is not None:
        raise PhysicallyIncompatibleEvidence("reference empty mass cannot establish metallurgical BOM")
    for key in ("native_storage_manufacturing_GWP_kgCO2e","full_cradle_to_gate_GWP_kgCO2e_per_H2_kg","full_LCOH_EUR_per_kg","installed_motor_and_cooler_hardware_mass_kg"):
        if obj[key] is not None:
            raise PhysicallyIncompatibleEvidence("unverified whole-plant GWP/cost/machine factor not permitted: "+key)
    if any((obj[k] for k in (
         "source_plants_measured",
         "original_BAFU_vehicle_tank_compatible_with_TypeI_steel_reference",
         "native_BAFU_v11_process_inspected_for_this_physical_design",
         "physically_matched_E_vs_ES_environmental_comparison_eligible"))):
        raise PhysicallyIncompatibleEvidence("false process technology/validation claim")
    for mode,source_cases in obj["cases"].items():
        if mode not in ("max_inventory","usable_service"):
            raise PhysicallyIncompatibleEvidence("unregistered original vs physical-capacity interpretation")
        for label in ("E","E_plus_S"):
            entry=source_cases[label]
            count=entry["vessels"]
            mass=entry["empty_reference_vessel_mass_kg"]
            heel=entry["gas_heel_kg"]
            if not isinstance(count,int) or count<=0 or not math.isclose(mass,count*2400,abs_tol=.001):
                raise PhysicallyIncompatibleEvidence("source vessel empty mass is not kgH2 stored")
            if not 0<heel<obj["common_original_model_H2_hourly_delivery_target_kg"]:
                raise PhysicallyIncompatibleEvidence("EOS residual H2 heel out of bounds")
            if label=="E":
                if entry["screen_result"]!="INFEASIBLE_FIXED_HOURLY_DELIVERY":
                    raise PhysicallyIncompatibleEvidence("E pressure screen unexpectedly claimed feasible")
                if any(entry[k] is not None for k in ("annual_wholesale_settlement_eur2023","annual_compressor_MWh","annual_delivered_H2_kg")):
                    raise PhysicallyIncompatibleEvidence("infeasible E cannot be assigned modelled same-service outputs")
            else:
                if entry["screen_result"]!="FULL_YEAR_MODELLED_DELIVERY_SOLVER_VERIFIED":
                    raise PhysicallyIncompatibleEvidence("source-verified E+S trajectory status changed")
                if not math.isclose(entry["annual_delivered_H2_kg"],obj["common_original_model_H2_hourly_delivery_target_kg"],abs_tol=.001):
                    raise PhysicallyIncompatibleEvidence("E+S delivered service SHA/denominator inconsistent")
                if entry["annual_compressor_MWh"]<=0:
                    raise PhysicallyIncompatibleEvidence("physically screened E+S charge energy missing")
        if source_cases["E_plus_S"]["vessels"]<=source_cases["E"]["vessels"]:
            raise PhysicallyIncompatibleEvidence("40t bank cannot have fewer source vessels than 20t")
    if not obj["native_BAFU_v11_process_inspected_for_this_physical_design"] and not obj["original_BAFU_vehicle_tank_compatible_with_TypeI_steel_reference"]:
        return obj
    raise PhysicallyIncompatibleEvidence("source-native provider compatibility unresolved")


def read_current():
    return validate_l1_bridge(json.loads(PATH.read_text(encoding="utf-8")))


def validate_upstream_artifact(path):
    original=Path(path).read_bytes()
    expected=read_current()["upstream_derived_json_sha256"]
    if hashlib.sha256(original).hexdigest()!=expected:
        raise PhysicallyIncompatibleEvidence("tampered or wrong original source-derived F3 artifact")
    doc=json.loads(original)
    if not doc.get("source_input_weather_and_price_identical_8760h"):
        raise PhysicallyIncompatibleEvidence("source wind/price profiles not identical")
    for mode in ("max_inventory","usable_service"):
        for k in ("E","E_plus_S"):
            if doc["scenarios"][mode][k]["source_based_screened_duty"]["vessel_count"]!=read_current()["cases"][mode][k]["vessels"]:
                raise PhysicallyIncompatibleEvidence("source vessel physical mass/count changed")
    return True
