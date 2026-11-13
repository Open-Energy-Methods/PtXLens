"""Complete, source-versioned BAFU:2026 IPCC GWP100 catalogue from Swiss FOEN OGD.

The official API has no offset pagination or substring filter. Partition by
the first hexadecimal character of each PROCESS UUID (16 disjoint windows).
Retrieve only source 2026 v1 / IPCC2021 / GWP100, validate every row, then
perform transparent local case-insensitive process-name discovery.

IMPORTANT: BAFU online responses are **pre-characterized per-process LCA
results**, NOT source foreground exchanges or a native openLCA product system.
A name match is a CANDIDATE, never a confirmed provider.
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import time

from .bafu_ogd import ENDPOINT, EXPECTED_VERSION, request, save_json

METHOD="IPCC 2021"
CATEGORY="GWP 100"
WINDOWS="0123456789abcdef"
LIMIT=10000
GRAPHQL="""query BafuGwp($where: EconomyConsumption_Lca_LciaResults_Filter, $limit:Int) {
  economy_consumption {
    lca {
      lcia_results(where:$where,limit:$limit) {
        version uuid processName location referenceUnit impactMethod
        impactCategory impactCategoryUnit value isSingleScore category
        lastDatasetUpdateYear sourceStudy sourceStudyAuthor
      }
    }
  }
}"""
UUID_RE=re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
FIELDS=("version","uuid","processName","location","referenceUnit",
        "impactMethod","impactCategory","impactCategoryUnit","value",
        "isSingleScore","category","lastDatasetUpdateYear","sourceStudy","sourceStudyAuthor")

# Search strings reflect source input classes, not assumed process IDs.
TARGETS={
  "stack.titanium":("titanium",),
  "stack.aluminium":("aluminium","aluminum"),
  "stack.stainless_steel":("stainless steel","chromium steel","steel, chromium"),
  "stack.copper":("copper",),
  "stack.membrane":("nafion","tetrafluoroethylene","polytetrafluoroethylene","ptfe"),
  "stack.activated_carbon":("activated carbon",),
  "stack.iridium":("iridium",),
  "stack.platinum":("platinum",),
  "water.deionized":("deionized","deionised","ion-exchange water","water, ultrapure"),
  "water.purification":("water purification","water treatment","reverse osmosis"),
  "electricity.offshore_wind":("offshore wind","wind power plant, offshore","wind turbine, offshore"),
  "electricity.market":("electricity, medium voltage","electricity, high voltage","electricity, low voltage"),
  "hydrogen.compress":("hydrogen compression","compressor, hydrogen"),
  "hydrogen.storage":("hydrogen storage","hydrogen tank","pressure vessel"),
  "equipment.electrolyser":("electrolyser","electrolyzer","electrolysis"),
  "bop.electronics":("electronics","electronic component"),
  "bop.silica":("silica gel",),
  "bop.heat_exchanger":("heat exchanger",),
}
CITATION="Database of the Swiss Federal Administration, BAFU:2026, Federal Office for the Environment, 2026"


def _validate(row):
    if not isinstance(row,dict):
        raise ValueError("unexpected non-object BAFU source record")
    if (row.get("version")!=EXPECTED_VERSION or row.get("impactMethod")!=METHOD
            or row.get("impactCategory")!=CATEGORY):
        raise ValueError("mixed source version or characterization method")
    uuid=row.get("uuid")
    if not isinstance(uuid,str) or not UUID_RE.fullmatch(uuid):
        raise ValueError("invalid source process UUID")
    name=row.get("processName")
    if not isinstance(name,str) or not name.strip():
        raise ValueError("source process name absent")
    score=row.get("value")
    if isinstance(score,bool) or not isinstance(score,(float,int)) or not math.isfinite(score):
        raise ValueError("source GWP factor absent/nonfinite")
    if row.get("isSingleScore") is True:
        raise ValueError("source unexpectedly flags IPCC GWP100 as weighted single-score")
    if not row.get("referenceUnit") or not row.get("impactCategoryUnit"):
        raise ValueError("source units absent")
    return uuid


def retrieve_catalogue(*, windows=WINDOWS, delay=.2, require_all_windows=True):
    """Partition by uuid startswith to obey BAFU max 10000 rows/query.

    Only source UUIDs validated as lowercase RFC format are included. Full
    catalogue asserts all 16 source UUID prefixes were queried once.
    """
    if not isinstance(windows,str) or len(set(windows))!=len(windows) or any(w not in WINDOWS for w in windows):
        raise ValueError("invalid UUID partition specification")
    if require_all_windows and windows!=WINDOWS:
        raise ValueError("partial windows must not be advertised as complete 2026 BAFU catalogue")
    by_uuid={}
    provenance=[]
    for prefix in windows:
        where={
            "version":{"_eq":EXPECTED_VERSION},
            "impactMethod":{"_eq":METHOD},
            "impactCategory":{"_eq":CATEGORY},
            "uuid":{"_startswith":prefix}
        }
        response=request(GRAPHQL,{"where":where,"limit":LIMIT})
        try:
            rows=response["data"]["economy_consumption"]["lca"]["lcia_results"]
        except (KeyError,TypeError) as exc:
            raise ValueError(f"BAFU source missing actual LCIA results for UUID prefix {prefix}") from exc
        if not isinstance(rows,list) or len(rows)>=LIMIT:
            raise ValueError("source response unexpectedly capped at 10000 records: finer split required")
        for row in rows:
            uuid=_validate(row)
            if not uuid.startswith(prefix):
                raise ValueError(f"source returned UUID outside filter partition {prefix}")
            if uuid in by_uuid:
                raise ValueError(f"duplicate source UUID/method GWP factor across official partitions: {uuid}")
            by_uuid[uuid]=row
        provenance.append({"uuid_prefix":prefix,"response_rows":len(rows),
                           "raw_json_response_sha256":response["raw_sha256"]})
        if delay:time.sleep(delay)
    if require_all_windows and len(by_uuid)<8000:
        raise ValueError("too few records for fully indexed 2026 database; possible missing API coverage")
    return by_uuid,provenance


def select_candidates(all_rows):
    out={}
    for group,needles in TARGETS.items():
        matches=[]
        for r in all_rows.values():
            name=r["processName"].casefold()
            if any(needle in name for needle in needles):
                matches.append({
                    **r,
                    "target_foreground_group":group,
                    "search_needle_used":[s for s in needles if s in name],
                    "is_candidate_name_match_only":True,
                    "verified_actual_provider_flow_id":None,
                    "verified_matching_unit_process_provider":False,
                    "verified_appropriate_2023_nl_geography":False,
                    "approved_for_hydrogen_lca":False,
                })
        out[group]=sorted(matches,key=lambda r:(r["processName"].casefold(),r["location"] or "",r["uuid"]))
    return out


def write_catalogue(csv_file, candidate_json, source_manifest, *,
                    windows=WINDOWS, delay=.2):
    paths=[Path(csv_file),Path(candidate_json),Path(source_manifest)]
    if any(p.exists() for p in paths):
        raise FileExistsError("never overwrite source result")
    full,source_provenance=retrieve_catalogue(windows=windows,delay=delay,
                                            require_all_windows=windows==WINDOWS)
    candidates=select_candidates(full)
    for p in paths:p.parent.mkdir(parents=True,exist_ok=True)
    with paths[0].open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=FIELDS)
        w.writeheader()
        w.writerows(full[k] for k in sorted(full))
    csv_hash=hashlib.sha256(paths[0].read_bytes()).hexdigest()
    cand={
        "schema_version":"ptxlens.bafu_2026_official_real_process_candidates.v0.2",
        "source":ENDPOINT,
        "version":EXPECTED_VERSION,"method":METHOD,"category":CATEGORY,
        "citation":CITATION,
        "is_native_linked_product_system":False,
        "approved_provider_count":0,
        "candidate_matches":candidates,
        "warnings":[
            "Names are not sufficient to identify production providers; check process reference flow, geography, upstream boundaries, units and licence.",
            "Supplier GWP100 results are already calculated for their original BAFU product system: do NOT combine with background-linked openLCA without avoiding double count.",
            "BAFU:2026 version uses updated published reference data, not actual 2023 Dutch electricity marginal intensities.",
            "No PEM stack input, water, compression or storage flow was assigned zero burden for lack of supplier."
        ]
    }
    save_json(cand,paths[1])
    manifest={
        "schema_version":"ptxlens.bafu_2026_complete_gwp100_source_manifest.v0.2",
        "verified_at_utc":datetime.now(timezone.utc).isoformat(),
        "endpoint":ENDPOINT,
        "documentation":"https://data.bafu.admin.ch/en/dataproduct-economy-consumption-lca",
        "citation":CITATION,
        "licence":"Swiss FOEN OGD: Open use. Must provide source.",
        "database_version":EXPECTED_VERSION,
        "impact_method":METHOD,"impact_category":CATEGORY,
        "uuid_partitions_attempted":windows,
        "all_16_hex_partitions_covered":windows==WINDOWS,
        "provider_records":len(full),
        "catalogue_sha256":csv_hash,
        "source_query_partition_hashes":source_provenance,
        "candidate_counts":{k:len(v) for k,v in candidates.items()},
        "confirmed_native_openlca_product_system_completeness":False,
        "bafu_zolca_database_imported":False,
    }
    save_json(manifest,paths[2])
    return manifest


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--csv",required=True,type=Path)
    p.add_argument("--candidates",required=True,type=Path)
    p.add_argument("--manifest",required=True,type=Path)
    p.add_argument("--pilot",action="store_true",
                   help="Query 2 UUID partitions only; cannot claim complete coverage")
    a=p.parse_args()
    m=write_catalogue(a.csv,a.candidates,a.manifest,
        windows="0a" if a.pilot else WINDOWS)
    print(json.dumps({"source":m["endpoint"],"version":m["database_version"],
                      "full_16_windows":m["all_16_hex_partitions_covered"],
                      "retrieved_real_process_records":m["provider_records"],
                      "candidate_counts":m["candidate_counts"],
                      "approved_provider_links":0},
                     sort_keys=True,ensure_ascii=False))
