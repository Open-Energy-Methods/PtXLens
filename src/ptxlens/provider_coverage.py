"""Generate a real-source provider coverage CSV from Federal LCA Commons API.

Only the actual observed HTTP responses may populate candidate process IDs.
A keyword hit is NOT an LCA provider link. No inputs are silently given zero
impact. The matrix can be regenerated from archived API evidence.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path

TARGET_REPO="Federal_LCA_Commons/commons_merged"
EXPECTATIONS = (
    ("titanium","titanium metal, 528 kg/1 MW", "exclude titanium dioxide"),
    ("aluminium","primary aluminium, 27 kg/1 MW","exclude aluminium sulphate"),
    ("stainless steel","18/8 steel, 100 kg/1 MW","evaluate 304 grade and North American geography"),
    ("copper","copper metal, 4.5 kg/1 MW","bridge is not a process provider"),
    ("nafion","Nafion membrane precursor, 16 kg/1 MW","specialty chemistry product and mass unit"),
    ("activated carbon","activated carbon, 9 kg/1 MW","proxy production may need region and technology validation"),
    ("iridium","iridium metal or PGM precursor, 0.75 kg/1 MW","precursor versus iridium metal mass needs careful mapping"),
    ("platinum","platinum metal, 0.075 kg/1 MW","precious metal extraction/smelting provider"),
    ("water treatment","deionized water, at hydrogen plant","drinking water is not deionized water"),
    ("hydrogen compression","H2 compression, conditioning and delivery","a PEM production unit process is NOT a compressor"),
    ("electricity offshore wind","wind offshore electricity process","no US onshore or generic electricity provider accepted as NL offshore"),
)


def classifications(term, process_name):
    name=process_name.lower()
    bridge="bridge" in name
    if term=="titanium":
        return ("irrelevant_titanium_oxide_or_bridge" if "dioxide" in name or bridge
                else "unreviewed_titanium_candidate")
    if term=="aluminium":
        return ("irrelevant_aluminium_salt_or_bridge" if "sulphate" in name or "sulfate" in name or bridge
                else "unreviewed_aluminium_candidate")
    if term=="stainless steel":
        return "candidate_US_stainless_304_grade_proxy" if "stainless 304" in name else "other_steel_not_approved"
    if term=="copper":
        return "bridge_without_confirmed_production_provider" if bridge else (
            "unrelated_copper_chemical" if "sulfate" in name or "sulphate" in name else "unreviewed_copper_candidate")
    if term=="activated carbon":
        return "candidate_US_activated_carbon_proxy" if "carbon production" in name else "not_activated_carbon_supply"
    if term=="water treatment":
        return "drinking_water_not_deionized" if "drinking water" in name else "unreviewed_water_process"
    if term=="hydrogen compression":
        return "PEM_hydrogen_reference_process_not_compressor" if "proton exchange membrane water electrolysis" in name else "not_verified_hydrogen_compression"
    return "name_candidate_not_approved"


def build_coverage(record, *, target=TARGET_REPO):
    if record.get("schema_version")!="ptxlens.federal_lca_api_probe.v0.1":
        raise ValueError("must use original source API observation record")
    queries = {row["query"]:row for row in record.get("queries",[])}
    rows=[]
    for term,desired,warning in EXPECTATIONS:
        entry=queries.get(term)
        if not entry:
            rows.append(dict(search_term=term,desired_product=desired,search_state="NOT_QUERIED",
                             candidate_name="",candidate_process_uuid="",candidate_assessment="",
                             source_release_tag="",reference_region="",repo=target,
                             reviewed_and_linked=False,coverage_warning=warning))
            continue
        if not entry.get("ok"):
            rows.append(dict(search_term=term,desired_product=desired,search_state="API_ERROR_"+str(entry.get("http_status")),
                             candidate_name="",candidate_process_uuid="",candidate_assessment="",
                             source_release_tag="",reference_region="",repo=target,
                             reviewed_and_linked=False,coverage_warning=warning))
            continue
        response=entry["response"]
        hits=response.get("data")
        info=response.get("resultInfo")
        if not isinstance(hits,list) or not isinstance(info,dict):
            raise ValueError("unexpected real API search schema; cannot classify")
        total=info.get("totalCount")
        # Search term can span different repos; require an exact source repo match.
        matches=[]
        for item in hits:
            if not isinstance(item,dict):
                raise ValueError("non-object record")
            for version in item.get("versions",[]):
                if not isinstance(version,dict):
                    continue
                for rep in version.get("repos",[]):
                    if rep.get("path")==target:
                        matches.append({
                            "uuid":item.get("refId",""),"name":version.get("name",""),
                            "tags":version.get("tags",[]),"location":version.get("location",""),
                            "process_type":version.get("processType",""),
                        })
                        break
        seen=set()
        if not matches:
            rows.append(dict(search_term=term,desired_product=desired,
                             search_state=("ZERO_PROCESS_NAME_MATCH_IN_SEARCH" if total==0 else "NO_TARGET_REPO_HIT_IN_RETRIEVED_PAGE"),
                             candidate_name="",candidate_process_uuid="",candidate_assessment="",
                             source_release_tag="",reference_region="",repo=target,
                             reviewed_and_linked=False,coverage_warning=warning))
        for match in matches:
            key=(match["uuid"],match["name"])
            if key in seen:continue
            seen.add(key)
            status=("SEARCH_PAGE_INCOMPLETE" if isinstance(total,int) and total>len(hits)
                    else "SEARCH_PAGE_COMPLETE")
            rows.append(dict(
                search_term=term,desired_product=desired,search_state=status,
                candidate_name=match["name"],candidate_process_uuid=match["uuid"],
                candidate_assessment=classifications(term,match["name"]),
                source_release_tag="|".join(match["tags"]),
                reference_region=match["location"] or "UNSPECIFIED_IN_SEARCH",
                repo=target,reviewed_and_linked=False,coverage_warning=warning))
    return rows


def generate(source,output_csv,manifest):
    source=Path(source);output_csv=Path(output_csv);manifest=Path(manifest)
    if output_csv.exists() or manifest.exists():
        raise FileExistsError("refusing to overwrite real-source audit")
    raw=source.read_bytes()
    data=json.loads(raw)
    rows=build_coverage(data)
    output_csv.parent.mkdir(parents=True,exist_ok=True)
    keys=list(rows[0].keys())
    with output_csv.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=keys)
        writer.writeheader();writer.writerows(rows)
    status={term:[] for term,_,_ in EXPECTATIONS}
    for row in rows:
        status[row["search_term"]].append(row["candidate_assessment"] or row["search_state"])
    evidence={
       "schema_version":"ptxlens.provider_search_coverage.v0.1",
       "raw_source_sha256":hashlib.sha256(raw).hexdigest(),
       "source_provider":"US Federal LCA Commons live API (Commons Merged)",
       "target_repository":TARGET_REPO,
       "term_summary":status,
       "source_queries_made":len(data["queries"]),
       "number_of_unreviewed_candidate_rows":sum(bool(r["candidate_process_uuid"]) for r in rows),
       "number_of_verified_usable_provider_links":0,
       "confirmed_cradle_to_gate_model_ready":False,
       "caveats":[
           "These are TEXT search matches for PROCESS objects, not verified output flows or actual provider links.",
           "Search pagination may truncate responses; a zero search result does not prove the product never exists in another repository.",
           "Method compatibility and US vs NL geography have not been validated.",
           "Exact provider/unit IDs, sub-process and elementary flow coverage must be checked after importing complete JSON-LD.",
           "A bridge process to USEEIO is not a standalone material production process.",
       ]
    }
    manifest.write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return evidence


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--csv",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(generate(args.source,args.csv,args.manifest),indent=2))
