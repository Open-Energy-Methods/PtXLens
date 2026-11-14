"""L3-B manufacturer and BAFU stationary-Type-I foreground evidence intake.

A complete questionnaire is not a supplier-certified bill of materials.
This module creates 19 source-anchored requirements and independently audits
only source-supported additions. No manufacturer pricing/material emissions
are fabricated, no BAFU process is assumed, and the original published
empty-equipment mass is never silently treated as purchased raw steel.

Private quote and datasheet bytes remain outside Git. The validator records
only the source-document fingerprints and non-sensitive aggregate readiness.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
from pathlib import Path

from .f2_l1_stationary_bom_bridge import load_f2_bom, SOURCE_SHA256

SCHEMA="ptxlens.l3b_stationary_typeI_manufacturer_FOREGROUND_evidence_intake.v1"
REVIEW_SCHEMA="ptxlens.l3b_independent_stationary_typeI_supplier_BAFU_readiness_v1"
MODES=("max_inventory","usable_service")
FORBIDDEN_BAFU_VEHICLE_PROCESS="b4739ad2-aa38-368d-8ada-63f5417c8b55"
EXPECTED_DOC_BOM={
    "typeI_200bar_bare_reference_vessels",
    "steel_alloy_material_grade_and_inclusions",
    "rack_frames_and_anchors",
    "high_pressure_headers_and_interconnects",
    "isolation_valves_and_actuators",
    "non_return_valves_and_filters",
    "pressure_relief_and_vent_stack",
    "pressure_regulation_delivery_header",
    "compressor_recips_and_seals",
    "compressor_motor_drive_VFD",
    "intercooler_aftercooler_heat_exchange",
    "cooling_pumps_and_fans",
    "gas_quality_dryer_and_sample_system",
    "pressure_temperature_flow_metering",
    "hydrogen_leak_detection_ESD_ATEX",
    "civil_foundations_and_construction",
    "inspections_fatigue_cycle_testing",
    "installation_and_transport",
    "decommission_and_EOL",
}

class StationarySourceEvidenceError(ValueError):pass

def require(x,msg):
    if not x:raise StationarySourceEvidenceError(msg)

def canonical_sha(s):
    return isinstance(s,str) and len(s)==64 and all(c in "0123456789abcdef" for c in s) and len(set(s))>1

def source_scope(mode):
    require(mode in MODES,"unknown independent pressure/inventory scenario")
    source=load_f2_bom()
    row=source["modes"][mode]
    req=row["required_incremental_system_foreground_BOM"]
    require(len(req)==19 and {x["line_id"] for x in req}==EXPECTED_DOC_BOM,
            "source pressure equipment/BOP foreground scope has changed")
    n=row["incremental_only_research_sensitivity"]["net_additional_published_reference_vessel_count"]
    expected=802 if mode=="max_inventory" else 902
    require(n==expected,"source original Type I incremental vessel count changed")
    return req,n

def blank_source_questionnaire(mode):
    req,n=source_scope(mode)
    lines=[]
    for row in req:
        vessel=row["line_id"]=="typeI_200bar_bare_reference_vessels"
        lines.append({
           "line_id":row["line_id"],
           "scope_status":"SOURCE_NOT_YET_DOCUMENTED",
           "reference_paper_discrete_vessel_count_not_OEM_quote":n if vessel else None,
           "supplier_name":None,
           "vendor_model_and_revision":None,
           "source_doc_private_relative_path":None,
           "source_doc_sha256":None,
           "engineering_qualification":{
              "rated_pressure_value":None,
              "rated_pressure_unit":None,
              "rated_max_temperature_K":None,
              "PED_stationary_installation_documented":False,
              "hydrogen_compatibility_documented":False,
              "design_life_years":None,
              "design_pressure_cycles":None,
           },
           "OEM_foreground":{
              "installed_quantity":None,
              "installed_quantity_unit":None,
              "manufacturer_equipment_empty_kg":None,
              "raw_input_material_bill_kg_by_grade":None,
              "manufacturing_loss_scrap_kg":None,
              "fabrication_energy_kwh":None,
              "fabrication_energy_region":None,
              "transport_mode_and_tkm":None,
              "EOL_recovery_and_allocations":None,
           },
           "supplier_quote":{
              "currency":None,
              "year":None,
              "valid_until_ISO":None,
              "scope_installed_or_ex_works":None,
              "net_price_excl_tax":None,
              "included_logistics_assembly_compressor_cooling":None,
              "annual_incremental_opex":None,
           },
           "BAFU_mapping":{
              "database":"BAFU:2026 v1.1",
              "unit_matching_verified":False,
              "process_uuid":None,
              "reference_flow_uuid":None,
              "exchange_reference_unit":None,
              "process_product_name_and_geography":None,
              "original_process_dataset_sha256":None,
              "is_cradle_to_gate_primary_process_or_full_equipment":None,
              "independent_reviewer_approved":False,
           },
           "independent_external_reviewer_signoff":False,
        })
    return {
        "schema_version":SCHEMA,
        "programme":"OEM-PTX-2026-01",
        "mode":mode,
        "source_F2_original_BOM_SHA256":SOURCE_SHA256,
        "source_historical_model_H2_capacity_E_and_ES_kg":[20000,40000],
        "source_reference_typeI_200bar_absolute_313K_screen_not_vendor_certification":True,
        "source_peer_reviewed_200bar_gauge_reference_vs_200bar_absolute_screen_DIFFERENT":True,
        "reference_paper_2400kg_per_empty_vessel_not_raw_steel_kg":True,
        "evidence_file_location":"PRIVATE_OUTSIDE_GIT_ONLY",
        "source_native_BAFU_executed_on_added_hardware":False,
        "all_19_scope_lines_supplier_manufacturing_and_LCI_sourced":False,
        "lines":lines,
    }

def validate_private_evidence(doc, private_root, *, native_v11_identity_review=None):
    """Validate genuine quote/datasheet bytes for each declared supplied item.

    Return source traceability/coverage counts, never a procurement quote
    or an LCIA result. Strict full qualification is intentionally unavailable
    until named independent manufacturer/reviewer accepts the design.
    """
    require(isinstance(doc,dict) and doc.get("schema_version")==SCHEMA,
            "invalid OEM BOM schema")
    mode=doc.get("mode")
    requirements,n=source_scope(mode)
    require(doc.get("source_F2_original_BOM_SHA256")==SOURCE_SHA256 and
            doc.get("evidence_file_location")=="PRIVATE_OUTSIDE_GIT_ONLY" and
            doc.get("reference_paper_2400kg_per_empty_vessel_not_raw_steel_kg") is True and
            doc.get("source_peer_reviewed_200bar_gauge_reference_vs_200bar_absolute_screen_DIFFERENT") is True,
            "source paper, 2023 model pressure or raw-steel accounting misrepresented")
    root=Path(private_root).resolve(strict=True)
    require(root.is_dir(),"private evidence root not found")
    entries=doc.get("lines")
    require(isinstance(entries,list) and len(entries)==19 and
            {x.get("line_id") for x in entries}==EXPECTED_DOC_BOM,
            "stationary pressure equipment requires exact 19-line foreground BOM")
    statuses={}
    count_evidence=0
    quote_count=0
    mapped_count=0
    manufacturer_material_count=0
    evidence_sha={}
    for row in entries:
        ident=row["line_id"]
        status=row.get("scope_status")
        require(status in ("SOURCE_NOT_YET_DOCUMENTED","OEM_DATASHEET_ONLY",
                           "OEM_QUOTE_NO_MATERIAL_LCI","OEM_MATERIAL_BREAKDOWN_PENDING_MAPPING",
                           "OEM_AND_NATIVE_BAFU_MAPPING_REVIEWED"),
                "unknown or prematurely completed supplier evidence status")
        require(ident not in statuses,"duplicate OEM equipment line")
        statuses[ident]=status
        is_vessel=ident=="typeI_200bar_bare_reference_vessels"
        require(row.get("reference_paper_discrete_vessel_count_not_OEM_quote")==(
            n if is_vessel else None),
            "reference paper equipment quantities changed or mistaken for a vendor quote")
        ref=row.get("source_doc_private_relative_path")
        refsha=row.get("source_doc_sha256")
        supplier=row.get("supplier_name")
        if status=="SOURCE_NOT_YET_DOCUMENTED":
            require(ref is None and refsha is None and supplier is None,
                    "undocumented component cannot claim source quotes or OEM")
            continue
        require(isinstance(supplier,str) and supplier.strip()
                and isinstance(row.get("vendor_model_and_revision"),str)
                and row["vendor_model_and_revision"].strip(),
                "OEM evidence lacks named manufacturer and product revision")
        require(isinstance(ref,str) and ref and not Path(ref).is_absolute()
                and ".." not in Path(ref).parts and canonical_sha(refsha),
                "supplier source path or hash not private/safe")
        source=(root/ref).resolve(strict=True)
        require(source.is_relative_to(root) and source.is_file() and not source.is_symlink()
                and len(source.read_bytes())>0 and
                hashlib.sha256(source.read_bytes()).hexdigest()==refsha,
                "private OEM original bytes not recoverable or hash mismatch")
        evidence_sha[ident]=refsha
        count_evidence+=1
        qual=row.get("engineering_qualification",{})
        pressure=qual.get("rated_pressure_value")
        unit=qual.get("rated_pressure_unit")
        if ident=="typeI_200bar_bare_reference_vessels":
            require(type(pressure) in (int,float) and math.isfinite(pressure)
                    and pressure>0 and unit in ("bar_absolute","bar_gauge") and
                    pressure+(1.01325 if unit=="bar_gauge" else 0)>=200.0,
                    "OEM Type I bank cannot prove source 200bar absolute design rating")
            require(qual.get("PED_stationary_installation_documented") is True and
                    qual.get("hydrogen_compatibility_documented") is True,
                    "OEM hydrogen stationary PED and material suitability not documented")
        fg=row.get("OEM_foreground",{})
        quote=row.get("supplier_quote",{})
        if status in ("OEM_QUOTE_NO_MATERIAL_LCI",
                      "OEM_MATERIAL_BREAKDOWN_PENDING_MAPPING",
                      "OEM_AND_NATIVE_BAFU_MAPPING_REVIEWED"):
            require(quote.get("currency") in ("EUR","SEK","CHF")
                    and type(quote.get("year")) is int
                    and 2020<=quote["year"]<=2035
                    and quote.get("scope_installed_or_ex_works") in ("INSTALLED","EX_WORKS")
                    and type(quote.get("net_price_excl_tax")) in (int,float)
                    and math.isfinite(quote["net_price_excl_tax"])
                    and quote["net_price_excl_tax"]>=0,
                    "manufacturer quoted monetary year, exclusion and scope are incomplete")
            quote_count+=1
        if status in ("OEM_MATERIAL_BREAKDOWN_PENDING_MAPPING",
                      "OEM_AND_NATIVE_BAFU_MAPPING_REVIEWED"):
            material=fg.get("raw_input_material_bill_kg_by_grade")
            require(isinstance(material,dict) and len(material)>0 and
                    all(isinstance(k,str) and k and type(v) in (int,float) and
                        math.isfinite(v) and v>=0 for k,v in material.items()),
                    "supplier foreground material bill/steel grade missing or unphysical")
            manufacturer_material_count+=1
        mapping=row.get("BAFU_mapping",{})
        require(mapping.get("process_uuid")!=FORBIDDEN_BAFU_VEHICLE_PROCESS,
                "vehicle composite tank H2-capacity LCI is not stationary steel kg")
        if status=="OEM_AND_NATIVE_BAFU_MAPPING_REVIEWED":
            # A manually entered UUID and a checked reviewer box are NOT
            # evidence of native BAFU material provider or reference-unit
            # identity. Require actual independently produced source original
            # v1.1 crosswalk certificate from the 135MB local .zolca replay.
            from .l3b_bafu_original_native_v11_reconcile import (
                REVIEW_SCHEMA as NATIVE_REVIEW_SCHEMA, NATIVE_SHA as NATIVE_V11_SHA,
            )
            require(isinstance(native_v11_identity_review,dict) and
                    native_v11_identity_review.get("schema_version")==NATIVE_REVIEW_SCHEMA and
                    native_v11_identity_review.get("source_private_BAFU_v11_original_zolca_SHA256")==NATIVE_V11_SHA,
                    "actual original v1.1 native ID/unit source review certificate required")
            native_row=native_v11_identity_review.get("reference_processes",{}).get(
                mapping.get("process_uuid"))
            require(isinstance(native_row,dict) and
                    native_row.get("identity_review_status")==
                      "ORIGINAL_NATIVE_V11_PROCESS_AND_QUANTITATIVE_REFERENCE_ID_VERIFIED_ONLY",
                    "proposed background supplier lacks native original v1.1 process identity")
            require(mapping.get("unit_matching_verified") is True and
                    isinstance(mapping.get("process_uuid"),str) and
                    mapping.get("reference_flow_uuid")==native_row.get("native_v11_reference_flow_uuid") and
                    mapping.get("exchange_reference_unit")==native_row.get("native_v11_reference_flow_unit") and
                    native_row.get("native_v11_reference_flow_type")=="PRODUCT_FLOW" and
                    mapping.get("independent_reviewer_approved") is True and
                    row.get("independent_external_reviewer_signoff") is True,
                    "native BAFU original quantitative-reference flow/unit or independent review missing")
            mapped_count+=1
    # IMPORTANT: A supplied filled template alone does not perform native LCIA
    # or prove that a quote covers the actual buildable system.
    return {
        "schema_version":REVIEW_SCHEMA,"mode":mode,
        "source_F2_original_BOM_SHA256":SOURCE_SHA256,
        "reference_incremental_200bar_paper_vessels_count_not_actual_quote":n,
        "source_scope_lines":len(entries),
        "OEM_primary_documents_verifiably_retained_private":count_evidence,
        "supplier_quotations_with_currency_year_and_scope":quote_count,
        "OEM_grade_specific_raw_material_BOM_lines":manufacturer_material_count,
        "native_BAFU_process_mapping_locally_reviewed_lines":mapped_count,
        "line_evidence_sha256":evidence_sha,
        "all_19_scope_lines_source_complete":all(x=="OEM_AND_NATIVE_BAFU_MAPPING_REVIEWED" for x in statuses.values()),
        "installed_pressure_design_globally_P_and_ID_verified":False,
        "native_BAFU_2026_stationary_typeI_whole_plant_LCIA_ACTUALLY_executed":False,
        "actual_supplier_station_investment_cost_quote_eligible_to_claim":False,
        "P0_two_independent_private_backups_restored":False,
        "full_L3_B_economic_and_environmental_release_ALLOWED":False,
    }

def main(argv=None):
    import argparse
    a=argparse.ArgumentParser(description=__doc__)
    mode=a.add_mutually_exclusive_group(required=True)
    mode.add_argument("--make-blank-mode",choices=MODES)
    mode.add_argument("--audit-private-manifest")
    a.add_argument("--private-evidence-root")
    a.add_argument("--native-v11-identity-review",
                   help="private original BAFU v1.1 process/reference-flow identity audit JSON")
    a.add_argument("--output",required=True)
    args=a.parse_args(argv)
    out=Path(args.output)
    require(not out.exists(),"will not overwrite supplier or original research evidence")
    if args.make_blank_mode:
        result=blank_source_questionnaire(args.make_blank_mode)
    else:
        require(args.private_evidence_root is not None,
                "private evidence directory required for checking original supplier bytes")
        result=validate_private_evidence(
            json.loads(Path(args.audit_private_manifest).read_text(encoding="utf-8")),
            args.private_evidence_root,
            native_v11_identity_review=(json.loads(Path(args.native_v11_identity_review).read_text(encoding="utf-8"))
                                        if args.native_v11_identity_review else None))
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\\n",encoding="utf-8")
    print("L3-B stationary manufacturer / native BAFU evidence",result["mode"],
          "NOT actual OEM installed quote, complete native LCA, LCOH or v1.0")


if __name__=="__main__":
    main()
