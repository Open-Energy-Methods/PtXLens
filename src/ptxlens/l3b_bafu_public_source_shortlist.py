"""Independent check of the 16 source-verified BAFU v1 process shortlist.

Original Swiss OGD catalogue is regenerated from 16 GraphQL UUID-prefix
partitions, not from plausible-sounding database names. Only source v1
process identities and units may be verified by this module. Any native v1.1
LCI, equipment manufacturing or monetary claim must remain FALSE.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

from .l3b_bafu_ogd_native_crosswalk import (
    original_public_catalogue,FORBIDDEN_BAFU_VEHICLE_PROCESS,
    BafuCrosswalkEvidenceError,need,
)

ROOT=Path(__file__).resolve().parents[2]
REGISTER=ROOT/"research/L3B_BAFU2026v1_SOURCE_VERIFIED_PUBLIC_PROCESS_SHORTLIST_NOT_NATIVE_v11_2026-11-14.json"
SCHEMA="ptxlens.l3b_official_BAFU2026_v1_shortlisted_original_process_metadata_NOT_native_v11.v1"
OUTPUT="ptxlens.l3b_official_BAFU2026_v1_16_identifiers_exact_catalogue_match_v1"

def audit_shortlist(original_csv,manifest,registry=REGISTER):
    index,sha=original_public_catalogue(original_csv,manifest)
    r=json.loads(Path(registry).read_text(encoding="utf-8"))
    need(r.get("schema_version")==SCHEMA and
         r.get("original_BAFU_v1_public_process_csv_SHA256")==sha and
         r.get("source_catalogue_processes")==11947 and
         r.get("source_process_ID_and_unit_verified_from_original_public_v1") is True and
         r.get("source_GWP_factors_deliberately_excluded_from_mapping") is True and
         r.get("original_native_v11_technosphere_reference_flows_crosswalk_done") is False and
         r.get("source_GWP_factors_are_precharacterized_not_manufacturing_technosphere_exchanges") is True and
         r.get("source_manufacturer_specific_material_quantity_recorded") is False and
         r.get("source_BAFU_v1_and_native_v11_equivalence_NOT_inferred") is True and
         r.get("no_full_plant_GWP_or_supplier_CAPEX_or_LCOH_claim") is True,
         "claimed native-v11, forbidden manufacturing mass or source-v1 shortlist SHA drift")
    entries=r.get("entries")
    need(isinstance(entries,list) and len(entries)==16,
         "published original BAFU v1 scientific shortlist must retain 16 actual source identities")
    seen=set()
    for row in entries:
        uid=row["uuid"]
        need(uid not in seen and uid in index,"duplicate/unknown Swiss BAFU original source process")
        seen.add(uid)
        v=index[uid]
        need((row["processName"],row["location"],row["referenceUnit"])==
             (v["processName"],v["location"],v["referenceUnit"]),
             "original source verified UUID / name / location / quantitative reference unit mismatch: "+uid)
        need(row.get("native_v11_process_verified_in_current_crosswalk") is False and
             row.get("native_v11_reference_flow_uuid") is None and
             row.get("OEM_material_mass_kg") is None and
             row.get("OEM_technosphere_process_link_approved") is False and
             row.get("GWP100_incremental_kgCO2e") is None,
             "published source process UUID is not an OEM material LCI or site-verified native provider")
        if uid==FORBIDDEN_BAFU_VEHICLE_PROCESS:
            need(row.get("evidence_class")=="SOURCE_VERIFIED_AND_REJECTED_TECHNOLOGY_BASIS",
                 "vehicle composite tank cannot masquerade as raw alloy steel")
        else:
            need(row.get("evidence_class")=="SOURCE_VERIFIED_PUBLIC_V1_PROCESS_METADATA_ONLY",
                 "unqualified published process promoted to native supplier")
    need(FORBIDDEN_BAFU_VEHICLE_PROCESS in seen,
         "known composite tank basis trap silently removed")
    return {
        "schema_version":OUTPUT,
        "original_official_BAFU2026_v1_catalogue_SHA256":sha,
        "source_published_GWP100_process_count":len(index),
        "source_selected_UUID_name_geo_unit_exact_matches":len(seen),
        "source_rejected_vehicle_composite_tank_UUID":FORBIDDEN_BAFU_VEHICLE_PROCESS,
        "original_native_v11_zolca_or_technosphere_examined_by_this_validator":False,
        "source_stationary_TypeI_original_manufacturer_alloy_kg_known":False,
        "published_factor_not_used_to_build_native_foreground":True,
        "source_independent_native_LCIA_and_supplier_BOM_passed":False,
    }

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("--catalogue",required=True)
    ap.add_argument("--manifest",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args(argv)
    path=Path(a.output)
    need(not path.exists(),"do not overwrite reviewed BAFU source traceability")
    r=audit_shortlist(a.catalogue,a.manifest)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(r,sort_keys=True,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print("Official Swiss OGD 16 process UUIDs, units/geographies verified; native v1.1 and station GWP NOT computed")

if __name__=="__main__":
    main()
