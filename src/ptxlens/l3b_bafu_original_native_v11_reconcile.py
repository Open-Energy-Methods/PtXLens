"""Reconcile public BAFU v1 leads with actual original BAFU v1.1 native IDs.

Only a private original .zolca of the exact recorded SHA, a Java openLCA
quantitative-reference export and the official OGD process candidate report
can produce a v1.1 identity certificate. Even a perfect identity match says
NOTHING about manufacturer material quantities, production technology,
qualified upstream supplier exchange, installed capital cost or final GWP.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re

from .l3b_bafu_ogd_native_crosswalk import (
    SCHEMA,NATIVE_SHA,FINGERPRINTS,DISALLOWED_ALIAS,
    FORBIDDEN_BAFU_VEHICLE_PROCESS,BafuCrosswalkEvidenceError,
    need,UUID,sha,
)
from .bafu_real_screen import PROCESSES

NATIVE_SCHEMA="ptxlens.BAFU2026_original_v11_native_quantitative_reference_identity.v1"
REVIEW_SCHEMA="ptxlens.L3B_BAFU2026_original_v11_quantitative_reference_candidate_REVIEW_NOT_provider_map.v1"
HEADERS=("schema_version","original_zolca_SHA256","process_UUID",
         "native_process_found","native_process_name","quantitative_flow_UUID",
         "quantitative_flow_name","quantitative_ref_unit")

def parse_private_native_table(path):
    evidence={}
    with Path(path).open(newline="",encoding="utf-8") as file:
        reader=csv.DictReader(file,delimiter="\t")
        need(tuple(reader.fieldnames or ())==HEADERS,
             "native openLCA v1.1 original export header changed")
        for row in reader:
            uid=row["process_UUID"]
            need(isinstance(uid,str) and UUID.fullmatch(uid) and uid not in evidence and
                 row.get("schema_version")==NATIVE_SCHEMA and
                 row.get("original_zolca_SHA256")==NATIVE_SHA and
                 row.get("native_process_found") in ("true","false"),
                 "invalid native v1.1 SHA, process UUID, duplicate or source export status")
            if row["native_process_found"]=="true":
                need(isinstance(row["quantitative_flow_UUID"],str) and
                     UUID.fullmatch(row["quantitative_flow_UUID"]) and
                     row.get("native_process_name") not in ("NULL",None,"") and
                     row.get("quantitative_flow_name") not in ("NULL",None,"") and
                     row.get("quantitative_ref_unit") not in ("NULL",None,""),
                     "native quantitative reference product identity incomplete")
            else:
                need(all(row.get(k)=="NULL" for k in (
                    "native_process_name","quantitative_flow_UUID",
                    "quantitative_flow_name","quantitative_ref_unit")),
                    "missing native provider erroneously contains product reference")
            evidence[uid]=row
            need(len(evidence)<=250,"native candidate manifest exceeds source review cap")
    need(bool(evidence),"native original BAFU v1.1 source audit empty")
    return evidence

def reconcile(crosswalk_json,original_zolca,native_process_tsv):
    original=Path(original_zolca)
    need(original.is_file() and not original.is_symlink() and
         original.stat().st_size==135424513 and sha(original)==NATIVE_SHA,
         "the EXACT original user-authorized BAFU v1.1 .zolca bytes are required")
    w=json.loads(Path(crosswalk_json).read_text(encoding="utf-8"))
    need(w.get("schema_version")==SCHEMA and
         w.get("source_official_catalogue_process_count")==11947 and
         w.get("source_version_public_impact_metadata")=="BAFU:2026 v1" and
         w.get("original_licensed_BAFU_v11_native_zolca_expected_sha256")==NATIVE_SHA and
         w.get("native_v11_flow_tech_and_provider_mapping_approved_count")==0 and
         w.get("full_GWP100_or_LCOH_or_investment_releasable") is False,
         "untrusted or prematurely approved public-v1 source class crosswalk")
    rows=parse_private_native_table(native_process_tsv)
    candidates={c["uuid"]:c for group in w["public_v1_groups"].values()
                for c in group["possibly_relevant_processes_not_native_approved"]}
    mandatory={PROCESSES[alias][0] for alias in (*FINGERPRINTS,DISALLOWED_ALIAS)}
    expected=set(candidates)|mandatory
    need(set(rows)==expected,
         "native original source reference export not same exact public candidate UUID set")
    outcome={}
    verified=0
    changed=0
    absent=0
    for uid,c in sorted(candidates.items()):
        x=rows[uid]
        if uid==FORBIDDEN_BAFU_VEHICLE_PROCESS:
            status="PROHIBITED_VEHICLE_COMPOSITE_OR_WRONG_FUNCTIONAL_BASIS"
        elif x["native_process_found"]=="false":
            status="ABSENT_IN_NATIVE_V11"
            absent+=1
        elif x["native_process_name"]!=c["process_name"] or
             x["quantitative_ref_unit"]!=c["reference_unit"]:
            status="V1_TO_NATIVE_V11_REFERENCE_NAME_OR_UNIT_REVISION_NEEDS_REVIEW"
            changed+=1
        else:
            status="ORIGINAL_NATIVE_V11_PROCESS_AND_QUANTITATIVE_REFERENCE_ID_VERIFIED_ONLY"
            verified+=1
        outcome[uid]={
            "source_public_v1_name":c["process_name"],
            "source_public_v1_reference_unit":c["reference_unit"],
            "native_v11_process_name":x["native_process_name"] if x["native_process_found"]=="true" else None,
            "native_v11_reference_flow_uuid":x["quantitative_flow_UUID"] if x["native_process_found"]=="true" else None,
            "native_v11_reference_flow_name":x["quantitative_flow_name"] if x["native_process_found"]=="true" else None,
            "native_v11_reference_flow_unit":x["quantitative_ref_unit"] if x["native_process_found"]=="true" else None,
            "identity_review_status":status,
            "OEM_site_material_process_functional_equivalence_certified":False,
            "supplier_default_provider_or_all_upstream_exchanges_approved":False,
            "material_input_quantity_kg":None,
            "native_product_system_GWP100_contribution":None,
        }
    # Even the four previously source-vetted v1 roles can be renamed/absent
    # in v1.1: require deliberate review rather than silently copying v1.
    primary={}
    for alias in (*FINGERPRINTS,DISALLOWED_ALIAS):
        uid,name,geo,unit=PROCESSES[alias]
        x=rows[uid]
        primary[alias]={
            "uuid":uid,"native_v11_found":x["native_process_found"]=="true",
            "source_public_v1_reference_unit":unit,
            "original_native_v11_reference_unit":x["quantitative_ref_unit"] if x["native_process_found"]=="true" else None,
            "original_v11_process_name_matches_published_v1":x["native_process_name"]==name if x["native_process_found"]=="true" else False,
            "source_v1_public_location":geo,
            "v11_native_location_NOT_exported_or_qualified":True,
            "native_still_UNQUALIFIED_for_stationary_TypeI_manufacturer_LCI":True,
        }
    return {
        "schema_version":REVIEW_SCHEMA,
        "source_public_BAFU_v1_catalogue_SHA256":w["source_official_catalogue_raw_csv_sha256"],
        "source_private_BAFU_v11_original_zolca_SHA256":NATIVE_SHA,
        "source_private_BAFU_v11_original_size_bytes":original.stat().st_size,
        "private_native_reference_export_sha256":sha(native_process_tsv),
        "mode":w["case"],
        "source_original_BAFU_v11_openLCA_Derby_private_export_observed":True,
        "source_native_process_identity_and_reference_unit_candidates_verified":verified,
        "source_candidates_changed_unit_name_or_revision":changed,
        "source_candidates_absent":absent,
        "reference_material_and_energy_process_v1_to_v11_provenance":primary,
        "reference_processes":outcome,
        "original_BAFU_v11_reference_unit_verified_does_not_equal_approved_technosphere_provider":True,
        "old_v1_vehicle_composite_per_kg_H2_capacity_tank_still_disallowed":True,
        "stationary_TypeI_manufacturer_raw_material_BOM_complete":False,
        "actual_native_supplier_links_approved":0,
        "full_BAFU_native_2026_stationary_incremental_GWP100_or_NPV_calculated":False,
        "independent_original_licensed_provider_redistributed":False,
    }

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--public-v1-crosswalk",required=True)
    p.add_argument("--original-BAFU-v11-zolca",required=True)
    p.add_argument("--private-native-reference-tsv",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args(argv)
    output=Path(a.output)
    need(not output.exists(),"do not overwrite native original source review")
    result=reconcile(a.public_v1_crosswalk,a.original_BAFU_v11_zolca,
                     a.private_native_reference_tsv)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print("Original BAFU v1.1 native reference identities checked:",
          result["source_native_process_identity_and_reference_unit_candidates_verified"],
          "verified-only /",result["source_candidates_changed_unit_name_or_revision"],
          "changed /",result["source_candidates_absent"],"missing.")
    print("Supplier maps approved=0; GWP and LCOH NOT computed.")

if __name__=="__main__":
    main()
