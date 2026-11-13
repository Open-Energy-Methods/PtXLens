"""Inspect *actual* Commons Merged JSON-LD process/provider and LCIA method graph.

A process name match or defaultProvider identifier is NOT proof of provider
closure. This audits source byte-hash, explicit product flows, supplier UUIDs,
system boundary, and method presence without fabricating an impact score.
"""
from __future__ import annotations
from collections import Counter,deque
import hashlib
import json
from pathlib import Path
import zipfile

PEM_ID="f00a298a-295f-4fbc-b463-45f8e96f018b"
KNOWN_SHA="1ded185617d4de67f8ed6933c473a68d65c232dd738779179e8559a31dfd056d"


def refid(data):
    return data.get("@id") if isinstance(data,dict) else None


def load_models(path):
    path=Path(path)
    content=path.read_bytes()
    digest=hashlib.sha256(content).hexdigest()
    if digest!=KNOWN_SHA:
        raise ValueError(f"Commons source ZIP sha mismatch, unreviewed edition: {digest}")
    entities={}
    with zipfile.ZipFile(path) as archive:
        for item in archive.namelist():
            if not item.endswith(".json") or "/" not in item:continue
            kind=item.split("/",1)[0]
            if kind not in ("processes","flows","lcia_methods","lcia_categories","impact_methods","impact_categories"):
                continue
            data=json.loads(archive.read(item))
            if not isinstance(data,dict):
                raise ValueError("source JSON-LD item is not an object")
            key=data.get("@id")
            if key:
                entities.setdefault(kind,{})[key]=data
    if PEM_ID not in entities.get("processes",{}):
        raise ValueError("actual 1kg PEM reference process absent from downloaded archive")
    return entities,digest


def audit(archive_path):
    e,digest=load_models(archive_path)
    ps=e["processes"]
    flows=e.get("flows",{})
    methods=e.get("lcia_methods",{}) or e.get("impact_methods",{})
    categories=e.get("lcia_categories",{}) or e.get("impact_categories",{})
    suppliers={}
    for proc in ps.values():
        for exchange in proc.get("exchanges",[]):
            # Any output (including co-products) can supply a product flow.
            # Restricting to quantitative reference falsely rejects valid co-product suppliers.
            if exchange.get("isInput") is False:
                suppliers.setdefault(refid(exchange.get("flow")),[]).append(proc["@id"])
    source=ps[PEM_ID]
    q=deque([PEM_ID])
    visited=set()
    errors=[]
    examined=0
    while q and len(visited)<5000:
        uuid=q.popleft()
        if uuid in visited:continue
        visited.add(uuid)
        process=ps[uuid]
        for exchange in process.get("exchanges",[]):
            if not isinstance(exchange,dict):
                raise ValueError("invalid exchange")
            if exchange.get("isInput") is not True:continue
            flow=exchange.get("flow") or {}
            fid=refid(flow)
            ftype=flows.get(fid,{}).get("flowType")
            if ftype=="ELEMENTARY_FLOW":continue
            # For known PRODUCT_FLOWS and WASTE_FLOWS, validate explicit provider
            provider=refid(exchange.get("defaultProvider"))
            examined+=1
            label={"consumer":process.get("name"),"consumer_uuid":uuid,
                   "input_flow_name":flow.get("name"),"flow_uuid":fid,
                   "flow_type":ftype or "UNRESOLVED_FLOW_TYPE",
                   "default_provider_uuid":provider,
                   "possible_matching_output_provider_uuids":suppliers.get(fid,[])[:5]}
            if not provider:
                errors.append({**label,"issue":"NO_EXPLICIT_DEFAULT_PROVIDER"})
                continue
            if provider not in ps:
                errors.append({**label,"issue":"PROVIDER_UUID_ABSENT_FROM_ARCHIVE"})
                continue
            if provider not in suppliers.get(fid,[]):
                errors.append({**label,"issue":"PROVIDER_DOES_NOT_REFERENCE_OUTPUT_FLOW"})
                continue
            q.append(provider)
    if q:
        errors.append({"issue":"GRAPH_LIMIT_REACHED","count_unvisited":len(q)})
    repair_candidates={"no_same_flow_output_process":0,
                       "one_same_flow_output_process":0,
                       "multiple_same_flow_output_processes":0}
    for problem in errors:
        if problem.get("issue")!="NO_EXPLICIT_DEFAULT_PROVIDER":
            continue
        options=len(problem.get("possible_matching_output_provider_uuids") or [])
        if options==0:
            repair_candidates["no_same_flow_output_process"]+=1
        elif options==1:
            repair_candidates["one_same_flow_output_process"]+=1
        else:
            repair_candidates["multiple_same_flow_output_processes"]+=1
    # Record *all* native impact-method names, not an assumed IPCC label.
    method_names=[]
    method_categories=[]
    for uuid,m in methods.items():
        category_refs=m.get("impactCategories") or []
        entry={"id":uuid,"name":m.get("name"),
               "category_uuid_count":len(category_refs)}
        for category in category_refs:
            category_id=refid(category)
            actual=categories.get(category_id)
            factor_list=(actual or {}).get("impactFactors") or []
            referenced=sum(bool(refid(f.get("flow")) in flows) for f in factor_list if isinstance(f,dict))
            method_categories.append({
                "method_name":m.get("name"),
                "category_id":category_id,
                "category_name":(actual or {}).get("name") or category.get("name"),
                "number_characterization_factors":len(factor_list),
                "factors_referencing_available_elementary_flows":referenced,
                "in_archive":actual is not None,
            })
        method_names.append(entry)
    # Prevent an archive with a named method but missing characterization rows
    # from being described as ready for real LCIA.
    ipcc=methods.get("00feb6d9-9282-3bcf-9d18-7b040f516935")
    ar6=categories.get("a6206006-65bc-395c-8dc9-f12262f45a04")
    if ipcc is None or ar6 is None or ar6.get("name")!="AR6-100":
        raise ValueError("original version-pinned IPCC AR6-100 method/category missing")
    cf=ar6.get("impactFactors") or []
    if len(cf)!=134:
        raise ValueError("unexpected original AR6-100 number of published characterization factors")
    cf_types=Counter(
        (flows.get(refid(k.get("flow")),{}).get("flowType","UNKNOWN"))
        for k in cf if isinstance(k,dict)
    )
    if cf_types.get("ELEMENTARY_FLOW",0)!=134:
        raise ValueError("AR6-100 characterization factors do not all reference valid elementary flows")
    method_verification={"ipcc_method_uuid":ipcc["@id"],"ipcc_method_name":ipcc.get("name"),
                         "ar6_100_category_uuid":ar6["@id"],
                         "characterization_factor_count":len(cf),
                         "verified_elementary_flow_factors":cf_types["ELEMENTARY_FLOW"],
                         "impact_factors_are_native_lcia_results":False}
    first_inputs=[]
    for x in source.get("exchanges",[]):
        if x.get("isInput") is True:
            p=refid(x.get("defaultProvider"))
            first_inputs.append({"flow":(x.get("flow") or {}).get("name"),
                                 "flow_uuid":refid(x.get("flow")),
                                 "amount":x.get("amount"),
                                 "unit":(x.get("unit") or {}).get("name"),
                                 "provider_uuid":p,
                                 "provider_in_archive":p in ps if p else False,
                                 "matching_quantitative_output":p in suppliers.get(refid(x.get("flow")),[]) if p else False,
                                 "alternate_output_provider_uuids":suppliers.get(refid(x.get("flow")),[])[:10]})
    return {
        "schema_version":"ptxlens.commons_merged_actual_provider_graph.v0.1",
        "source_archive_sha256":digest,
        "source_repository":"Federal_LCA_Commons/commons_merged",
        "source_reference_process_uuid":PEM_ID,
        "source_reference_process_name":source.get("name"),
        "source_reference_process_location":(source.get("location") or {}).get("name"),
        "counts":{"processes":len(ps),"flows":len(flows),
                  "lcia_methods":len(methods),"lcia_categories":len(categories),
                  "reachable_upstream_processes":len(visited),
                  "upstream_technosphere_inputs_examined":examined,
                  "missing_or_incompatible_provider_links":len(errors)},
        "first_process_actual_source_inputs":first_inputs,
        "available_impact_methods":method_names,
        "ipcc_ar6_100_original_method_verification":method_verification,
        "impact_method_category_characterization_coverage":method_categories,
        "upstream_errors_by_type":dict(Counter(row["issue"] for row in errors)),
        "missing_provider_candidate_counts":repair_candidates,
        "first_five_nearest_unlinked_product_inputs":errors[:5],
        "upstream_error_samples":errors[:45],
        "upstream_unresolved_exchange_records":errors,
        "provider_graph_closed":len(errors)==0,
        "ready_for_cradle_to_gate_nl_lca":False,
        "assumptions_and_caveats":[
            "Full repository is open source/public but includes mixed contributed datasets and geographical limits.",
            "Source 2017 US PEM hydrogen at plant is not a 2023 NL plant and excludes anode drying/purification.",
            "A closed provider graph alone does not guarantee compatible LCIA characterization, flow coverage, allocation or completeness.",
            "Same-flow UUID candidate suppliers are only a repair shortlist; do not link without validating coproduct allocation, geography, units, year and library provenance.",
            "This is graph auditing, not an executed openLCA LCIA."
        ],
    }


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--archive",required=True)
    p.add_argument("--output",required=True)
    args=p.parse_args()
    result=audit(args.archive)
    out=Path(args.output)
    if out.exists():raise FileExistsError("refusing to overwrite provider audit")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ("source_archive_sha256","counts","upstream_errors_by_type","available_impact_methods","first_process_actual_source_inputs")},indent=2))
