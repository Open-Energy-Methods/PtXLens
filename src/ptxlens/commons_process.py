"""Inspect authentic 2026 Commons Merged PEM H2 process from FLCAC JSON-LD API.

Only actual source JSON-LD exchanges and provider UUIDs are recorded.
Do not equate a pre-existing process's inputs with confirmed closed upstream
provider graph or call a unit-process inventory a completed LCIA.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen

BASE="https://api.nal.usda.gov/FederalLCACommonsapi"
PROCESS_ID="f00a298a-295f-4fbc-b463-45f8e96f018b"
GROUP="Federal_LCA_Commons"
REPO="commons_merged"
PROCESS_URL="https://lcacommons.gov/lca-collaboration/National_Renewable_Energy_Laboratory/USLCI_Database_Public/dataset/PROCESS/"+PROCESS_ID


def ref(x):
    if isinstance(x,dict):
        return {"id":x.get("@id") or x.get("id"),
                "name":x.get("name"),"type":x.get("@type")}
    return None


def read_public_process(*,opener=urlopen):
    key=os.environ.get("LCA_COMMONS_API_KEY","DEMO_KEY")
    if not key:raise RuntimeError("missing API credential")
    path=f"/browse/{GROUP}/{REPO}/PROCESS/{PROCESS_ID}"
    url=f"{BASE}{path}?"+urlencode({"api_key":key})
    request=Request(url,headers={"Accept":"application/json","User-Agent":"PtXLens/0.2 published-reference LCI audit"})
    with opener(request,timeout=80) as response:
        raw=response.read(5_000_001)
    if len(raw)>5_000_000:raise ValueError("unexpected oversized single-process API object")
    doc=json.loads(raw)
    # The public gateway normally returns a JSON-LD process. Do not
    # substitute guessed data if the gateway returns a search wrapper.
    if not isinstance(doc,dict):
        raise ValueError("unexpected non-object single process")
    if doc.get("@id")!=PROCESS_ID:
        raise ValueError("returned JSON-LD process ID mismatch")
    if doc.get("@type") not in ("Process","PROCESS"):
        raise ValueError("expected openLCA Process JSON-LD object")
    exchanges=doc.get("exchanges")
    if not isinstance(exchanges,list) or not exchanges:
        raise ValueError("published process unexpectedly has no exchanges")
    rows=[]
    for e in exchanges:
        if not isinstance(e,dict):raise ValueError("invalid source exchange")
        if "isInput" not in e or not isinstance(e["isInput"],bool):
            raise ValueError("openLCA JSON-LD exchange isInput flag missing or nonboolean")
        rows.append({
            "flow":ref(e.get("flow")),"input":e["isInput"],
            "amount":e.get("amount"),"unit":ref(e.get("unit")),
            "flow_property":ref(e.get("flowProperty")),
            "default_provider":ref(e.get("defaultProvider")),
            "is_quantitative_reference":e.get("isQuantitativeReference"),
            "description":(e.get("description") or "")[:450],
        })
    useful=[r for r in rows if r["input"] and r["flow"]]
    missing=[r["flow"]["name"] for r in useful if not (r["default_provider"] and r["default_provider"]["id"])]
    if not useful:
        raise ValueError("no identified inputs; invalid or incomplete JSON-LD parsing")
    from .lca_source_quality import inventory_stoichiometry_check
    physical_quality=inventory_stoichiometry_check(rows)
    return {
        "schema_version":"ptxlens.actual_uslci_pem_process_audit.v0.1",
        "mass_and_stoichiometry_source_check":physical_quality,
        "source_repo":"Federal_LCA_Commons/commons_merged",
        "original_source_record":PROCESS_URL,
        "process_uuid":PROCESS_ID,
        "process_name":doc.get("name"),
        "source_jsonld_sha256":hashlib.sha256(raw).hexdigest(),
        "process_type":doc.get("processType"),
        "source_location":ref(doc.get("location")),
        "number_exchanges":len(rows),
        "number_input_exchanges":len(useful),
        "unlinked_input_flow_names":missing,
        "all_exchange_source_metadata":rows,
        "result_status":"PROCESS_INPUT_INSPECTION_ONLY; no native openLCA LCIA or complete provider graph",
        "geographic_warning":"2017 US-representative PEM process adapted from German work, not NL 2023",
    }


def write_result(path):
    p=Path(path)
    if p.exists():raise FileExistsError("do not overwrite actual source proof")
    result=read_public_process()
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    args=p.parse_args()
    x=write_result(args.output)
    print(json.dumps({"process":x["process_name"],"uuid":x["process_uuid"],
                      "exchange_count":x["number_exchanges"],
                      "unlinked_inputs":x["unlinked_input_flow_names"],
                      "source_sha256":x["source_jsonld_sha256"]},indent=2))
