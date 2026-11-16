"""Real 2026 BAFU published-process GWP sensitivity on original 2023 Dutch dispatch.

This is not a native, linked cradle-to-gate LCA. Every factor comes from the
official Swiss FOEN 2026 version-tagged IPCC 2021 GWP100 database API and is
verified by exact UUID / process name / location / unit. Every 2023 annual
energy and material mass originates from hash-verified original PyNEXUS output
and a published 2024 PEM materials source. Missing materials are NOT zero.
"""
from __future__ import annotations
import csv
import hashlib
import json
import math
from pathlib import Path

from .lca_screen import assess_observed_electricity_lifecycle
from .pem_stack_lci import scenario_foreground

VERSION="BAFU:2026 v1"
METHOD="IPCC 2021"
CATEGORY="GWP 100"
CITATION="Database of the Swiss Federal Administration, BAFU:2026, Federal Office for the Environment, 2026"
OGD_URL="https://data.bafu.admin.ch/en/dataproduct-economy-consumption-lca"

# Process identities selected only after exact manual review of official
# 11,947-record source catalogue. NO hardcoded impact factors.
PROCESSES={
 "grid_nl_high_voltage":(
     "437a439d-1994-3496-b51f-23868b6987aa",
     "Electricity, high voltage, at grid","NL","MJ"),
 "offshore_wind_legacy_2mw":(
     "23f2cd16-32d3-3312-85c9-8095bfe6815c",
     "xx Electricity, at wind power plant 2MW, offshore","OCE","MJ"),
 "water_nl_deionized":(
     "64b93c35-a87c-33d3-8983-01a8c951d462",
     "Water, deionised, water balance according to MoeK 2013, at plant","NL","kg"),
 "aluminium_primary":(
     "5cac9857-21f7-305d-b705-c83a02a94e6e",
     "Aluminium, primary, at plant","RER","kg"),
 "stainless_18_8":(
     "fc9385f8-fe2d-3399-b663-4b66e5062a3f",
     "Chromium steel 18/8, at plant","RER","kg"),
 "copper":(
     "3972eb0c-d60e-3537-9ad1-fd6b7bbafce8",
     "Copper, at regional storage","RER","kg"),
 "platinum":(
     "7a020379-c844-32ff-8fde-fb468f6661b5",
     "Platinum, at regional storage","RER","kg"),
 "hydrogen_pem_30bar_ch":(
     "99a1af16-58cd-3f11-a877-c43d3c8e5d78",
     "Hydrogen production, gaseous, 30 bar, from PEM electrolysis, from grid electricity","CH","kg"),
 "hydrogen_pem_30bar_ma":(
     "96a6a42f-a9b8-38d0-9148-bf1bab6687ec",
     "Hydrogen production, gaseous, 30 bar, from PEM electrolysis, from autonomous hybrid plant","MA","kg"),
 "h2_pipeline_ch":(
     "def44f32-461b-3b6f-9860-b92abe87fbd6",
     "Hydrogen supply, distributed by pipeline, produced by Electrolysis, PEM using electricity from grid","CH","kg"),
 "h2_high_pressure_tank":(
     "b4739ad2-aa38-368d-8ada-63f5417c8b55",
     "High pressure hydrogen storage tank","GLO","kg"),
 "membrane_finished_not_precursor":(
     "e8610445-cb47-3f69-8bd9-d2d580fd8e45",
     "Polymer electrolyte membrane (Nafion) production","RER","kg"),
 "iridium_metal_not_concentrate":(
     "8a6c655d-b743-3945-a1a6-e070f70c48b2",
     "Iridium production","GLO","kg"),
}
ACCEPTED_MATERIAL_BY_SOURCE_DESCRIPTION={
    "aluminium, primary, at plant":"aluminium_primary",
    "market for steel, chromium steel 18/8":"stainless_18_8",
    "copper, at regional storage":"copper",
    "market for platinum":"platinum"
}
UNRESOLVED_STACK_REASONS={
 "market for titanium":"No metallic titanium production process identified; titanium dioxide and titanium zinc plate are NOT Ti metal.",
 "nafion (sulfonyl fluoride)":"Published 16 kg precursor is not interchangeable with a finished Nafion membrane inventory.",
 "activated carbon production, granular from hard coal":"Only spent activated-carbon waste-treatment process appeared; no granular activated-carbon manufacturing source validated.",
 "market for platinum group metal concentrate, Iridium":"PGM iridium-bearing concentrate inventory is not equivalent to fully refined iridium metal. Exact elemental content unknown."
}


def verified_bafu_factors(csv_path, manifest_path):
    csv_path=Path(csv_path)
    manifest=json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    if (manifest.get("database_version")!=VERSION or
            manifest.get("impact_method")!=METHOD or
            manifest.get("impact_category")!=CATEGORY or
            manifest.get("all_16_hex_partitions_covered") is not True):
        raise ValueError("not the full, original 2026 source/version/method catalogue")
    raw=csv_path.read_bytes()
    sha=hashlib.sha256(raw).hexdigest()
    if sha!=manifest.get("catalogue_sha256"):
        raise ValueError("BAFU source GWP catalogue bytes changed")
    indexed={}
    with csv_path.open("r",encoding="utf-8",newline="") as fp:
        for row in csv.DictReader(fp):
            if row.get("uuid") in indexed:
                raise ValueError("BAFU source duplicate UUID")
            indexed[row["uuid"]]=row
    if len(indexed)!=11947 or len(indexed)!=manifest.get("provider_records"):
        raise ValueError("incomplete BAFU:2026 official data catalogue")
    factors={}
    for alias,(uuid,name,location,unit) in PROCESSES.items():
        record=indexed.get(uuid)
        if record is None:
            raise ValueError(f"required real source process {alias} absent")
        if (record["processName"]!=name or record["location"]!=location or
                record["referenceUnit"]!=unit or record["version"]!=VERSION or
                record["impactMethod"]!=METHOD or record["impactCategory"]!=CATEGORY):
            raise ValueError(f"published process UUID metadata mismatch for {alias}")
        val=float(record["value"])
        if not math.isfinite(val) or val < 0:
            # Negative avoided burdens valid in general, but accepted direct
            # product-supplier mappings here were reviewed as positive.
            raise ValueError(f"unexpected selected source reference impact for {alias}")
        factors[alias]={
            "source_process_uuid":uuid,"published_process_name":name,
            "published_process_location":location,"published_process_unit":unit,
            "original_IPCC_2021_GWP100_kgco2e_per_reference_unit":val,
            "source_last_dataset_update_year":record.get("lastDatasetUpdateYear"),
            "source_study":record.get("sourceStudy"),
            "source_study_author":record.get("sourceStudyAuthor")
        }
    return factors,sha


def assess_case(archive, stack_lci, *,factors):
    # Existing audit does the original per-hour demand, power and SHA checks.
    electricity=assess_observed_electricity_lifecycle(archive)
    stack=scenario_foreground(archive,stack_lci)
    if stack["scenario"]!=electricity["scenario"]:
        raise ValueError("original source scenario mismatch")
    # A published LCA factor per MJ, not per kWh: 1 kWh = 3.6 MJ.
    grid_factor=factors["grid_nl_high_voltage"]["original_IPCC_2021_GWP100_kgco2e_per_reference_unit"]
    offshore_factor=factors["offshore_wind_legacy_2mw"]["original_IPCC_2021_GWP100_kgco2e_per_reference_unit"]
    grid_mwh=electricity["energy_mwh"]["grid_import_for_electrolysis"]
    wind_mwh=electricity["energy_mwh"]["offshore_wind_for_electrolysis"]
    h2_kg=electricity["functional_unit_denominator_kg_h2"]
    electric_totals={
      "historical_grid_import_kgco2e":grid_mwh*3600*grid_factor,
      "onsite_wind_allocated_kgco2e":wind_mwh*3600*offshore_factor
    }
    supply_kg=sum(electric_totals.values())
    known_inputs=[]
    missing_inputs=[]
    matched_mass=0.0
    source_mass=0.0
    published_subset_per_kg_h2=0.0
    for item in stack["lifecycle_material_inputs"]:
        product=item["provider_description"]
        mass_per_kg_h2=item["scenario_mass_kg_per_kg_model_delivered_h2"]
        source_mass+=item["stack_reference_1mw_material_kg"]
        if product not in ACCEPTED_MATERIAL_BY_SOURCE_DESCRIPTION:
            missing_inputs.append({
                "foreground_mass_description":product,
                "reference_mass_per_1mw_stack_kg":item["stack_reference_1mw_material_kg"],
                "modelled_mass_per_kg_delivered_h2":mass_per_kg_h2,
                "reason":UNRESOLVED_STACK_REASONS.get(product,"No documented equivalent material supplier")
            })
            continue
        alias=ACCEPTED_MATERIAL_BY_SOURCE_DESCRIPTION[product]
        factor=factors[alias]
        if factor["published_process_unit"]!="kg":
            raise ValueError("BAFU material source factor unit mismatch")
        impact=mass_per_kg_h2*factor["original_IPCC_2021_GWP100_kgco2e_per_reference_unit"]
        matched_mass+=item["stack_reference_1mw_material_kg"]
        published_subset_per_kg_h2+=impact
        known_inputs.append({
            "source_material_description":product,
            "literature_stack_reference_1mw_material_mass_kg":item["stack_reference_1mw_material_kg"],
            "lifetime_modelled_input_kg_per_kg_model_delivered_h2":mass_per_kg_h2,
            "selected_published_BAFU_supplier":factor,
            "component_kgco2e_per_kg_h2":impact,
            "claim":"published-process-factor material COMPONENT, not linked source inventory LCIA"
        })
    if len(known_inputs)!=4 or len(missing_inputs)!=4 or source_mass<=0:
        raise ValueError("PM stack coverage unexpected; fail rather than count missing as zero")
    water_factor=factors["water_nl_deionized"]["original_IPCC_2021_GWP100_kgco2e_per_reference_unit"]
    water_sens={
        "published_BAFU_nl_deionized_kgco2e_per_kg_water":water_factor,
        "assumed_intake_liters_per_kg_H2_low":stack["water_foreground_inventory_litres_per_kg_h2_low"],
        "assumed_intake_liters_per_kg_H2_high":stack["water_foreground_inventory_litres_per_kg_h2_high"],
        "density_assumption_kg_per_litre":1.0,
        "published_factor_sensitivity_kgco2e_per_kg_H2_range":[
            water_factor*stack["water_foreground_inventory_litres_per_kg_h2_low"],
            water_factor*stack["water_foreground_inventory_litres_per_kg_h2_high"]
        ],
        "note":"water volume is LITERATURE estimated, not a metered PyNEXUS source input; held separate"
    }
    return {
        "scenario":stack["scenario"],
        "original_source_archive_sha256":stack["source_archive_sha256"],
        "historical_2023_modelled_H2_delivered_kg":h2_kg,
        "historical_2023_electricity_mwh":electricity["energy_mwh"],
        "BAFU_energy_supply_assessment_gwp_kgco2e":electric_totals,
        "BAFU_energy_supply_total_kgco2e":supply_kg,
        "BAFU_energy_supply_intensity_kgco2e_per_kg_model_delivered_H2":supply_kg/h2_kg,
        "assumed_30yr_study_stack_service_cycles":stack["assumed_stack_service_cycles_in_30_years"],
        "published_BAFU_subset_of_stack_materials":known_inputs,
        "published_stack_GWP_subset_kgco2e_per_kg_delivered_H2":published_subset_per_kg_h2,
        "unresolved_source_stack_materials":missing_inputs,
        "matched_source_mass_fraction_not_environmental_coverage":matched_mass/source_mass,
        "literature_assumed_water_sensitivity":water_sens,
        "BAFU_full_reference_hydrogen_benchmark_only":[
            factors["hydrogen_pem_30bar_ch"],
            factors["hydrogen_pem_30bar_ma"],
            factors["h2_pipeline_ch"]
        ],
        "functional_unit_mismatch_warning":"Source H2 delivered under original model: requires defined physical delivery quality, pressure and service; BAFU 30bar reference is NOT the 2023 NL plant.",
        "no_total_cradle_to_gate_GWP_computed":True,
        "full_product_system_LCA_claim_allowed":False,
    }


def write_assessment(e_archive,es_archive,catalogue,source_manifest,stack_lci,output_file):
    dst=Path(output_file)
    if dst.exists():raise FileExistsError("refusing to overwrite audited research output")
    factors,source_hash=verified_bafu_factors(catalogue,source_manifest)
    E=assess_case(e_archive,stack_lci,factors=factors)
    ES=assess_case(es_archive,stack_lci,factors=factors)
    if E["scenario"]!="E" or ES["scenario"] not in ("E_plus_S","E+S"):
        raise ValueError("unexpected original source model comparison")
    report={
      "schema_version":"ptxlens.BAFU_2026_real_observed_source_E_ES_partial_components.v0.1",
      "source_citation":CITATION,"source_url":OGD_URL,
      "published_version":VERSION,"published_method":METHOD,"published_category":CATEGORY,
      "official_source_GWP_catalogue_sha256":source_hash,
      "factor_source_registry":factors,
      "E":E,"E_plus_S":ES,
      "claim_level":"REAL published BAFU precharacterized process GWP component sensitivity; NOT native linked hydrogen product LCA",
      "matched_delivered_service":False,
      "no_total_cradle_to_gate_GWP_computed":True,
      "full_product_system_LCA_claim_allowed":False,
      "critical_hard_stops":[
         "Metallic titanium source missing (titanium dioxide is not metallic titanium); dominant stack mass omitted.",
         "Activated-carbon supply process missing (waste disposal is not input production).",
         "Iridium concentrate vs refined iridium and Nafion precursor vs finished membrane mismatch.",
         "Full electrolyser BoP manufacture, compressors, H2 storage vessel physical inventory and life/end-of-life absent.",
         "BAFU 2MW offshore electricity process name is prefixed xx (legacy), not modern Dutch North Sea infrastructure.",
         "BAFU 2026 factors are not time-resolved actual 2023 Dutch marginal/contractual grid impact.",
         "2023 original PyNEXUS H2 is physically modelled, not metered; hypothetical 30y repetition is not a forecast.",
         "Native BAFU .zolca inventory not yet provided under Nexus terms, imported and linked in original openLCA."
      ]
    }
    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
    return report


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--E",required=True)
    p.add_argument("--ES",required=True)
    p.add_argument("--catalogue",required=True)
    p.add_argument("--source-manifest",required=True)
    p.add_argument("--stack-source",default="data/lci/pem_stack_kanz_2024_1mw.json")
    p.add_argument("--output",required=True)
    args=p.parse_args()
    result=write_assessment(args.E,args.ES,args.catalogue,args.source_manifest,args.stack_source,args.output)
    for key in ("E","E_plus_S"):
        s=result[key]
        print(json.dumps({"case":key,
            "electricity_supply_BAFU_2026_kgCO2e_per_kg_modelled_H2":s["BAFU_energy_supply_intensity_kgco2e_per_kg_model_delivered_H2"],
            "four_sourced_stack_material_components_kgCO2e_per_kg_H2":s["published_stack_GWP_subset_kgco2e_per_kg_delivered_H2"],
            "missing_stack_materials":len(s["unresolved_source_stack_materials"]),
            "full_hydrogen_cradle_to_gate_LCA":False},sort_keys=True))
