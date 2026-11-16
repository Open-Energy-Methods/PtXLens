"""Aggregate actual Commons Merged unresolved provider exchanges for repair.

No imaginary provider matches or resolved=true claims. Each CSV row traces a
real source process/input flow UUID from original source ZIP. All 695
unresolved exchanges preserved without filtering, grouped by exact flow UUID.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import csv
import json
from pathlib import Path

def write_gap_tables(report_path, *, exchange_csv, flow_csv):
    data=json.loads(Path(report_path).read_text(encoding="utf-8"))
    if data.get("schema_version")!="ptxlens.commons_merged_actual_provider_graph.v0.1":
        raise ValueError("expected exact source-audited Commons graph report")
    problems=data.get("upstream_unresolved_exchange_records")
    if not isinstance(problems,list):
        raise ValueError("full unresolved source exchange list required, not just samples")
    n=data.get("counts",{}).get("missing_or_incompatible_provider_links")
    if len(problems)!=n:
        raise ValueError(f"missing provider count mismatch {len(problems)} vs {n}")
    for x in problems:
        if not isinstance(x,dict) or not x.get("issue") or not x.get("flow_uuid"):
            raise ValueError("invalid source supplier gap; no placeholder records")
    dests=[Path(exchange_csv),Path(flow_csv)]
    if any(p.exists() for p in dests):
        raise FileExistsError("refusing to overwrite source gap tables")
    for p in dests:p.parent.mkdir(parents=True,exist_ok=True)
    columns=[
        "issue", "consumer", "consumer_uuid", "input_flow_name","flow_uuid",
        "flow_type", "default_provider_uuid", "same_flow_output_provider_count",
        "same_flow_output_provider_first_5","verified_linked","repair_status"
    ]
    with dests[0].open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader()
        for p in problems:
            candidates=p.get("possible_matching_output_provider_uuids") or []
            w.writerow({
                "issue":p["issue"],"consumer":p.get("consumer",""),
                "consumer_uuid":p.get("consumer_uuid",""),
                "input_flow_name":p.get("input_flow_name",""),
                "flow_uuid":p.get("flow_uuid",""),"flow_type":p.get("flow_type",""),
                "default_provider_uuid":p.get("default_provider_uuid") or "",
                # Candidate list is truncated to five in upstream audit: avoid stating it is exhaustive!
                "same_flow_output_provider_count":(
                    ">=5" if len(candidates)>=5 else str(len(candidates))),
                "same_flow_output_provider_first_5":"|".join(candidates),
                "verified_linked":False,
                "repair_status":"REQUIRES_ACTUAL_UNIT_PROCESS_AND_METHOD_VALIDATION",
            })
    unique={}
    for p in problems:
        k=p["flow_uuid"]
        if k not in unique:
            unique[k]={"flow_name":p.get("input_flow_name",""),"flow_uuid":k,
                       "flow_type":p.get("flow_type",""),
                       "unresolved_input_exchanges":0,
                       "unique_consumers":set(),"same_flow_provider_candidates_first_5":p.get("possible_matching_output_provider_uuids") or []}
        unique[k]["unresolved_input_exchanges"]+=1
        unique[k]["unique_consumers"].add(p.get("consumer_uuid",""))
    flows=sorted(unique.values(),key=lambda x:(-x["unresolved_input_exchanges"],x["flow_uuid"]))
    with dests[1].open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["input_flow_name","flow_uuid","flow_type","unresolved_input_exchanges",
                                        "unique_consumer_count","same_flow_provider_candidates_first_5",
                                        "status"])
        w.writeheader()
        for item in flows:
            opts=item["same_flow_provider_candidates_first_5"]
            w.writerow({
                "input_flow_name":item["flow_name"],"flow_uuid":item["flow_uuid"],
                "flow_type":item["flow_type"],
                "unresolved_input_exchanges":item["unresolved_input_exchanges"],
                "unique_consumer_count":len(item["unique_consumers"]),
                "same_flow_provider_candidates_first_5":"|".join(opts),
                "status":"SAME_FLOW_PROVIDER_NOT_PRESENT" if not opts else "CANDIDATE_LINK_NOT_REVIEWED",
            })
    return {"source_archive_sha256":data["source_archive_sha256"],
            "total_unresolved_exchanges":len(problems),
            "distinct_unresolved_flow_uuids":len(flows),
            "counts_by_issue":dict(Counter(p["issue"] for p in problems)),
            "top_5_unresolved_flows":[{"name":x["flow_name"],"uuid":x["flow_uuid"],
                                       "references":x["unresolved_input_exchanges"]} for x in flows[:5]],
            "linked_provider_count":0,
            "claim":"supplier gap evidence only; no complete provider chain or LCIA execution"}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True)
    p.add_argument("--by-exchange",required=True)
    p.add_argument("--by-flow",required=True)
    args=p.parse_args()
    print(json.dumps(write_gap_tables(args.source,exchange_csv=args.by_exchange,flow_csv=args.by_flow),indent=2))
