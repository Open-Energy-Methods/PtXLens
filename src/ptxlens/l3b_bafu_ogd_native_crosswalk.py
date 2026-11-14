"""L3-B source-audited BAFU v1 OGD -> native v1.1 foreground candidate crosswalk.

Three distinct assertions:
1. Official Swiss OGD "BAFU:2026 v1" IPCC GWP100 rows identify process
   UUID/name/geography/reference unit, not their manufacturing input exchanges.
2. The original private native v1.1 .zolca (exact registered SHA) plus
   openLCA-core quantitative references can confirm SAME process identities.
3. Actual OEM grade-specific quantities and production/technology provider
   linkages are STILL required before any LCA exchange is approved.

A product 'High pressure hydrogen storage tank' based on per kg H2 capacity,
which the original BAFU v1 source categorizes under VEHICLE components, is
categorically forbidden as per kg finished Type I steel equipment.
Never output numeric GWP, invent installed kg steel, or mark missing impact 0.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re

from .bafu_real_screen import PROCESSES
from .l3b_stationary_manufacturer_bafu_foreground_intake import (
    source_scope,EXPECTED_DOC_BOM,MODES,FORBIDDEN_BAFU_VEHICLE_PROCESS,
)

SCHEMA="ptxlens.l3b_source_OGD_v1_to_native_v11_stationary_material_candidate_crosswalk.v1"
NATIVE_SHA="e63b7e7ef5cde04bfe1176a783a55b5f72e2b73f42c36632b6150af39d348c4c"
SOURCE="https://data.bafu.admin.ch/api"
VERSION="BAFU:2026 v1"
METHOD="IPCC 2021"
CATEGORY="GWP 100"
FINGERPRINTS=("stainless_18_8","aluminium_primary","copper","grid_nl_high_voltage")
DISALLOWED_ALIAS="h2_high_pressure_tank"
# Process-token groups are SEARCH leads, not approved supplier substitutions.
# A 'kg' reference alone cannot prove a finished equipment or raw metal mass.
SEARCH_GROUPS={
    "low_alloy_steel":{"terms":("steel, low-alloyed","low-alloy steel","steel, unalloyed"),"reference_units":("kg",)},
    "stainless_steel":{"terms":("chromium steel 18/8","stainless steel"),"reference_units":("kg",)},
    "structural_steel":{"terms":("steel, low-alloyed","structural steel","reinforcing steel"),"reference_units":("kg",)},
    "metal_forming":{"terms":("steel rolling","sheet rolling","metal working","steel forging","machining, steel"),"reference_units":("kg",)},
    "copper":{"terms":("copper, at regional storage","copper, at plant"),"reference_units":("kg",)},
    "aluminium":{"terms":("aluminium, primary, at plant","aluminium alloy"),"reference_units":("kg",)},
    "electricity":{"terms":("electricity, high voltage, at grid","electricity, medium voltage"),"reference_units":("MJ","kWh")},
    "concrete":{"terms":("concrete, normal","concrete, at plant","cement, portland"),"reference_units":("kg","m3")},
    "steel_recycling":{"terms":("steel, recycling","steel scrap","steel, secondary"),"reference_units":("kg",)},
    "road_freight":{"terms":("transport, freight, lorry","transport, lorry"),"reference_units":("t*km","tonne kilometre")},
    "manufacturing_heat":{"terms":("heat, natural gas","heat, industrial"),"reference_units":("MJ","kWh")},
}
# Every item is a COST/LCA FOREGROUND EQUIPMENT class. The process search
# groups point only to potential SUBCOMPONENT material/processing providers.
# They are not direct native process links for a complete plant assembly.
BOM_STAGE_GROUPS={
 "typeI_200bar_bare_reference_vessels":("low_alloy_steel","stainless_steel","metal_forming","electricity"),
 "steel_alloy_material_grade_and_inclusions":("low_alloy_steel","stainless_steel","metal_forming"),
 "rack_frames_and_anchors":("structural_steel","metal_forming","electricity"),
 "high_pressure_headers_and_interconnects":("stainless_steel","metal_forming"),
 "isolation_valves_and_actuators":("stainless_steel","copper","aluminium","electricity"),
 "non_return_valves_and_filters":("stainless_steel","metal_forming"),
 "pressure_relief_and_vent_stack":("stainless_steel","metal_forming"),
 "pressure_regulation_delivery_header":("stainless_steel","copper","metal_forming"),
 "compressor_recips_and_seals":("stainless_steel","low_alloy_steel","metal_forming"),
 "compressor_motor_drive_VFD":("copper","aluminium","electricity"),
 "intercooler_aftercooler_heat_exchange":("stainless_steel","aluminium","copper"),
 "cooling_pumps_and_fans":("low_alloy_steel","copper","aluminium"),
 "gas_quality_dryer_and_sample_system":("stainless_steel","metal_forming"),
 "pressure_temperature_flow_metering":("stainless_steel","copper"),
 "hydrogen_leak_detection_ESD_ATEX":("copper","stainless_steel","electricity"),
 "civil_foundations_and_construction":("concrete","structural_steel","road_freight"),
 "inspections_fatigue_cycle_testing":("electricity","manufacturing_heat"),
 "installation_and_transport":("road_freight","electricity"),
 "decommission_and_EOL":("steel_recycling","road_freight","electricity"),
}
assert set(BOM_STAGE_GROUPS)==EXPECTED_DOC_BOM
UUID=re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

class BafuCrosswalkEvidenceError(ValueError): pass

def need(condition,message):
    if not condition:raise BafuCrosswalkEvidenceError(message)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda:stream.read(1048576),b""):
            h.update(block)
    return h.hexdigest()

def original_public_catalogue(csvpath,manifestpath):
    provenance=json.loads(Path(manifestpath).read_text(encoding="utf-8"))
    need(provenance.get("schema_version")=="ptxlens.bafu_2026_complete_gwp100_source_manifest.v0.2" and
         provenance.get("database_version")==VERSION and
         provenance.get("impact_method")==METHOD and
         provenance.get("impact_category")==CATEGORY and
         provenance.get("all_16_hex_partitions_covered") is True and
         provenance.get("uuid_partitions_attempted")=="0123456789abcdef" and
         provenance.get("endpoint")==SOURCE and
         provenance.get("confirmed_native_openlca_product_system_completeness") is False,
         "not the original complete Swiss OGD BAFU v1 GWP100 process catalogue")
    rawsha=sha(csvpath)
    need(rawsha==provenance.get("catalogue_sha256"),
         "official public process catalogue bytes failed registered SHA256")
    index={}
    with Path(csvpath).open(encoding="utf-8",newline="") as file:
        rows=csv.DictReader(file)
        for row in rows:
            key=row.get("uuid")
            need(isinstance(key,str) and UUID.fullmatch(key) and key not in index,
                 "duplicate or invalid original official process UUID")
            need(row.get("version")==VERSION and row.get("impactMethod")==METHOD and
                 row.get("impactCategory")==CATEGORY and
                 row.get("processName") and row.get("referenceUnit") and
                 row.get("impactCategoryUnit"),
                 "mixed source version, unit or impact category")
            index[key]=row
    need(len(index)==11947 and len(index)==provenance.get("provider_records"),
         "incomplete official 2026 v1 catalogue, expected exactly 11,947 processes")
    for alias in (*FINGERPRINTS,DISALLOWED_ALIAS):
        expected_id,name,geo,unit=PROCESSES[alias]
        entry=index.get(expected_id)
        need(entry is not None and
             (entry["processName"],entry["location"],entry["referenceUnit"])==(name,geo,unit),
             "source-registered process UUID/name/location/unit changed: "+alias)
    need(PROCESSES[DISALLOWED_ALIAS][0]==FORBIDDEN_BAFU_VEHICLE_PROCESS,
         "prohibited vehicle tank source UUID drifted")
    return index,rawsha

def discover_candidates(index,*,max_per_group=8):
    need(type(max_per_group) is int and 1<=max_per_group<=20,
         "candidates require bounded independent manual review set")
    result={}
    for group,rule in SEARCH_GROUPS.items():
        available=[]
        for row in index.values():
            name=row["processName"].casefold()
            unit=row["referenceUnit"]
            matched=[token for token in rule["terms"] if token in name]
            if not matched or unit not in rule["reference_units"]:
                continue
            if row["uuid"]==FORBIDDEN_BAFU_VEHICLE_PROCESS:
                continue
            # Search priority is reproducible, does not assert suitability.
            quality=max(len(t) for t in matched)
            loc=row["location"]
            available.append((-quality,0 if loc in ("RER","NL","CH") else 1,
                              name,row["uuid"],row,matched))
        available.sort(key=lambda x:x[:4])
        candidates=[]
        for _,__,___,____,r,tokens in available[:max_per_group]:
            candidates.append({
               "uuid":r["uuid"],"source_version":VERSION,"process_name":r["processName"],
               "location":r["location"],"reference_unit":r["referenceUnit"],
               "source_match_tokens":tokens,
               "source_GWP100_factor_deliberately_not_imported":True,
               "source_claim":"PUBLISHED_BAFU_V1_NAME_UNIT_GEO_CANDIDATE_ONLY",
               "native_v11_quantitative_reference_verified":False,
               "manufacturer_material_and_technology_match_approved":False,
               "native_BAFU_supplier_exchange_link_approved":False,
               "physical_mass_or_output_coefficient_kg":None,
               "full_plant_GWP_contribution_kgCO2e":None,
            })
        result[group]={
            "name_matches_before_review_cap":len(available),
            "presented_candidate_count":len(candidates),
            "possibly_relevant_processes_not_native_approved":candidates,
            "no_matching_source_is_not_zero_impact":True,
        }
    return result

def crosswalk(mode,catalogue,manifest):
    need(mode in MODES,"unknown bank gross-vs-usable interpretation")
    index,source_sha=original_public_catalogue(catalogue,manifest)
    group=discover_candidates(index)
    source_rows,n=source_scope(mode)
    need(set(x["line_id"] for x in source_rows)==EXPECTED_DOC_BOM,"original F2 scope drifted")
    items=[]
    for row in source_rows:
        name=row["line_id"]
        items.append({
         "foreground_equipment_class":name,
         "published_reference_incremental_vessel_count_NOT_actual_supplier_order":
             n if name=="typeI_200bar_bare_reference_vessels" else None,
         "manufacturer_raw_alloy_kg_by_grade":None,
         "manufacturer_fabrication_process_energy_kwh":None,
         "manufacturer_machining_scrap_kg":None,
         "installed_subcomponent_quantity":None,
         "native_BAFU_v11_approved_supplier_process_uuid":None,
         "native_original_v11_reference_flow_uuid":None,
         "native_original_v11_reference_unit":None,
         "crosswalk_review_stage":"OFFICIAL_BAFU_V1_PUBLIC_PROCESS_CANDIDATES_ONLY",
         "potential_BACKGROUND_material_and_service_groups":list(BOM_STAGE_GROUPS[name]),
         "potential_background_provider_UUIDs_v1_not_native_approval":
             {g:[c["uuid"] for c in group[g]["possibly_relevant_processes_not_native_approved"]]
              for g in BOM_STAGE_GROUPS[name]},
         "not_an_assumed_complete_manufactured_equipment_process":True,
         "unknown_material_or_process_burden_not_zero":True,
        })
    need(len(items)==19,"missing source BOM classes")
    return {
       "schema_version":SCHEMA,
       "programme":"OEM-PTX-2026-01",
       "source_version_public_impact_metadata":VERSION,
       "source_endpoint":SOURCE,
       "source_official_catalogue_raw_csv_sha256":source_sha,
       "source_official_catalogue_process_count":11947,
       "original_licensed_BAFU_v11_native_zolca_expected_sha256":NATIVE_SHA,
       "original_licensed_BAFU_v11_actually_imported_or_read_for_this_crosswalk":False,
       "source_OGD_precalculated_GWP100_does_not_equal_original_native_LCI_exchange":True,
       "source_original_BAFU_v1_high_pressure_composite_vehicle_tank_UUID_rejected":
           FORBIDDEN_BAFU_VEHICLE_PROCESS,
       "material_provider_search_not_equipment_assembly_or_LCA_mapping":True,
       "reference_2400kg_empty_vessel_is_not_OEM_raw_virgin_steel_kg":True,
       "case":mode,
       "source_reference_additional_vessels_model_not_vendor":n,
       "unresolved_nonzero_foreground_classes_count":19,
       "public_v1_groups":group,
       "foreground_equipment":items,
       "manufacturer_qualified_installed_BOM_provided":False,
       "native_v11_flow_tech_and_provider_mapping_approved_count":0,
       "complete_native_BAFU_TypeI_storage_environmental_model":False,
       "full_GWP100_or_LCOH_or_investment_releasable":False,
       "P0_durable_independent_source_recoveries_witnessed":False,
       "legal_original_BAFU_v11_database_redistributed":False,
    }

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--mode",required=True,choices=MODES)
    parser.add_argument("--catalogue",required=True)
    parser.add_argument("--manifest",required=True)
    parser.add_argument("--output",required=True)
    a=parser.parse_args(argv)
    target=Path(a.output)
    need(not target.exists(),"do not overwrite source crosswalk")
    result=crosswalk(a.mode,a.catalogue,a.manifest)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print("Official BAFU v1 process identifiers registered",result["source_official_catalogue_process_count"],
          "; class candidates",sum(v["presented_candidate_count"] for v in result["public_v1_groups"].values()),
          "; native v1.1 qualified supplier links=0. Full station GWP STOP.")

if __name__=="__main__":
    main()
