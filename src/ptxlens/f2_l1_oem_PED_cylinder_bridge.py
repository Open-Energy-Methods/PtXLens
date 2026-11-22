"""PtXLens independent source-certified OEM steel PED 330bar cylinder sensitivity.

Manufacturer heiserTEC gives mass for a specific genuine PED hydrogen
cylinder 50L 330bar 85.5kg, not its stationary COSMOS 210bar 36x87L
bundle and not the mobile TPED 935kg bundle. The F2 EOS hypothetical
200bar(a) 313K calculation is separately source-hash frozen. This checks
quantities, ORIGINAL 2023 E20t/ES40t and station-scope BAFU omissions.

No OEM-documented source-fabrication mass fractions or national PED/EN17533
conformity for the proposed station; do not treat mass as BAFU per kg steel
product, complete capital cost, GWP or deliverable installation.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from .f2_l1_stationary_bom_bridge import import_f2_bom

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/"data/results/F2_L1_OEM_heisertec_PED_330bar_50L_85_5kg_source_200bar_313K_NOT_certified_BOM.json"
REG=ROOT/"research/F2_L1_INDEPENDENT_OEM_PED_50L_330BAR_H2_CYLINDER_AND_EN17533_SOURCE_v1.json"
SRC_SHA256="9db1885bd42cc91049c4d2e7170aaf74782bf0d791ed88b877795e84fa4a8a57"
EXPECTED="ptxflex.f2_l1_independent_heiserTEC_330bar_PED_50L_OEM_mass_at_200bara_screen.v1"
SCHEMA="ptxlens.f2_l1_oem_330bar_PED_50L_vs_IJHE_200bar_typeI_reference_hardware_not_full_LCI.v1"


class InvalidOEMMassEvidence(ValueError):pass


def require(x,msg):
    if not x:raise InvalidOEMMassEvidence(msg)


def verify_OEM_source():
    raw=SRC.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==SRC_SHA256,"unregistered source manufacturer 330bar PED 50L H2 empty weight or gas inventory")
    d=json.loads(raw)
    require(d.get("schema_version")==EXPECTED and
            d.get("original_200bar_paper_F2_source_SHA256")=="1315d1181b9d1eab6d3368425c9571dbe295c3360935d2972403bf3c60e2dc47" and
            d.get("source_2023_PyNEXUS_project_not_actual_heiserTEC_installation") is True and
            d.get("manufacturer_oem_product_330bar_nominal_pressure_not_same_as_200bar_screen") is True and
            d.get("OEM_product_working_pressure_basis_gauge_absolute_unverified") is True and
            d.get("manufacturer_50L_85_5kg_is_H2_pressure_cylinder_not_mobile_module_frame") is True and
            d.get("standard_for_individual_cylinders_not_manifolded_assemblies") is True and
            d.get("whole_plant_comparison_release_ready") is False,
            "wrong OEM product, fabricated stationary bundle or unsupported national PED site qualification")
    m=json.loads(REG.read_text())
    require(m.get("schema_version")=="oem.ptx.f2_l1_stationary_PED_vessel_independent_OEM_product_source.v1" and
            m["manufacturer"]["catalogue_empty_cylinder_weight_kg"]==85.5 and
            m["manufacturer"]["working_pressure_catalogue_bar"]==330 and
            m["manufacturer"]["cylinder_water_volume_litre"]==50 and
            m["manufacturer"]["material_alloy_grade_certificate_available"] is False and
            m["local_standards"]["name"]=="NEN-EN 17533:2025" and
            m["local_standards"]["explicitly_excludes_manifolded_assemblies"] is True and
            m["system_complete_manufacturer_BOM_available"] is False,
            "missing independent OEM standard/pressure/empty weight or material conformity record")
    return d


def generate_OEM_crosscheck():
    o=verify_OEM_source()
    primary=import_f2_bom()
    profiles={}
    for mode,row in o["modeled_source_inventory_modes"].items():
        src=primary["modes"][mode]
        count=row["hypothetical_extra_cylinders_count"]
        mass=row["hypothetical_extra_OEM_empty_cylinder_hardware_mass_kg"]
        require(count>0 and mass==count*85.5 and
                row["hypothetical_200bara_EplusS40t_cylinder_count"]-
                row["hypothetical_200bara_E20t_cylinder_count"]==count,
                "actual manufacturer per-cylinder mass / 20t->40t count does not conserve")
        require(row["reference_IJHE200bar_extra_larger_vessel_count"]==
                src["incremental_REFERENCE_EMPTY_MANUFACTURED_VESSEL_COUNT"] and
                row["reference_IJHE200bar_extra_larger_vessel_mass_kg"]==
                src["incremental_REFERENCE_EMPTY_MANUFACTURED_VESSEL_MASS_kg"],
                "OEM 50L pressure cylinder illegally substituted for IJHE 1.8m3 200bar reference vessel")
        for key in ("actual_completed_manufacturer_BOM",):
            require(row[key] is False,"OEM cross-check falsely approved full hardware")
        for key in ("vendor_module_frame_manifold_valves_fabrication_mass_kg",
                    "manufacturer_grade_and_H2_fatigue_conformity_for_actual_200bar_313K_duty",
                    "native_BAFU2026_v1_1_typeI_compatible_manufacturing_GWP_kgCO2e",
                    "full_tank_inc_CAPEX_EUR"):
            require(row[key] is None,"missing physical station allocation/GWP/cost field cannot be guessed: "+key)
        require(row["mobile_TPED_935kg_empty_complete_bundle_weight_used_here"] is False and
                row["both_source_candidates_different_cylinder_dimensions_rated_pressure_not_identical_products"] is True,
                "mobile TPED or distinct OEM vs IJHE vessel conflated")
        profiles[mode]={
           "2023_modelled_source_case_capacity_semantics":mode,
           "IJHE_200bar_TypeI_1_8m3_literature_additional_vessels":src["incremental_REFERENCE_EMPTY_MANUFACTURED_VESSEL_COUNT"],
           "IJHE_200bar_TypeI_1_8m3_literature_additional_empty_hardware_kg":src["incremental_REFERENCE_EMPTY_MANUFACTURED_VESSEL_MASS_kg"],
           "OEM_heisertec_330bar_PED_50L_reference_at_derated_200bara_313K_additional_cylinders":count,
           "OEM_heisertec_330bar_PED_50L_reference_at_derated_200bara_313K_additional_empty_hardware_kg":mass,
           "OEM_330bar_is_separate_pressure_rating_and_50L_geometry_not_a_vendor_200bar_station_offer":True,
           "same_stationary_210bar_COSMOS_36x87L_bundle_empty_mass_known":False,
           "published_50L_PED_cylinder_standalone_mass_must_not_be_used_for_36x87L_COSMOS_modules":True,
           "OEM_200bar_derated_313K_cycling_not_site_certified":True,
           "steel_raw_input_from_weight_without_materials_fabrication_provider_NOT_allowed":True,
           "original_F3C_same_hour_source_target_SHA256":src["source_common_H2_hourly_target_SHA256"],
           "manufacturer_stationary_typeI_supplier_BOM_complete":False,
           "full_native_BAFU2026_v11_co2e_kg":None,
           "whole_plant_EUR2023_discounted_cost":None,
        }
    require(set(profiles)=={"max_inventory","usable_service"},"missing source original E 20t to 40t inventory mode")
    return {
       "schema_version":SCHEMA,"programme":"OEM-PTX-2026-01",
       "original_2023_source_operating_hydrogen_is_modelled":True,
       "source_F2_OEM_50L_json_sha256":SRC_SHA256,
       "source_IJHE_typeI_200bar_F2_registered_original_SHA256":"1315d1181b9d1eab6d3368425c9571dbe295c3360935d2972403bf3c60e2dc47",
       "EN17533_2025_standards_for_cylinder_not_manifold_or_piping":True,
       "OEM_330bar_product_not_2023_site_certified_at_200bara":True,
       "missing_steel_manufacturing_alloy_heat_treatment_rack_BO_P_CEH":True,
       "two_distinct_typeI_cylinder_reference_products_not_interchangeable":True,
       "financial_and_climate_compare_release_eligible":False,
       "scenarios":profiles,
    }
