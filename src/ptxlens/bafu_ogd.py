"""Official Swiss FOEN / BAFU open-government-data GraphQL discovery.

The API exposes PRECALCULATED LCIA per process, not a linked foreground LCI.
Never replace actual openLCA product-system calculations with these values.
No authentication and no private/nonpublic Nexus download.
"""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError, URLError
import hashlib,json

ENDPOINT="https://data.bafu.admin.ch/api"
DOCUMENTATION="https://data.bafu.admin.ch/en/dataproduct-economy-consumption-lca"
EXPECTED_VERSION="BAFU:2026 v1"

QUERY_ROOT="""query DataType {
  __schema { queryType { name fields {
    name
    type { kind name ofType { kind name ofType { kind name } } }
  } } }
}"""
QUERY_NAMED="""query NamedType($name: String!) {
  __type(name: $name) {
    name kind
    fields {
      name
      type { kind name ofType { kind name ofType {kind name} } }
      args { name type {kind name ofType {kind name ofType {kind name}}} }
    }
  }
}"""


def request(query,variables=None,*,opener=urlopen):
    payload=json.dumps({"query":query,"variables":variables or {}},separators=(",",":")).encode()
    req=Request(ENDPOINT,data=payload,method="POST",headers={
        "Content-Type":"application/json","Accept":"application/json",
        "User-Agent":"Open-Energy-Methods/PtXLens-source-audit-0.2"})
    with opener(req,timeout=70) as resp:
        raw=resp.read(4_000_001)
        http=getattr(resp,"status",200)
    if len(raw)>4_000_000:
        raise ValueError("BAFU OGD response exceeds 4MB; use pagination")
    body=json.loads(raw)
    if not isinstance(body,dict) or body.get("errors"):
        raise ValueError("BAFU GraphQL error: "+str(body.get("errors"))[:1500])
    if not isinstance(body.get("data"),dict):
        raise ValueError("BAFU GraphQL response missing data")
    return {"http_status":http,"raw_sha256":hashlib.sha256(raw).hexdigest(),
            "data":body["data"],"size_bytes":len(raw)}


def unwrapped(t):
    for _ in range(4):
        if not isinstance(t,dict):break
        if t.get("name"):return t["name"]
        t=t.get("ofType")
    return None


def discover_schema():
    root=request(QUERY_ROOT)
    query_type=root["data"]["__schema"]["queryType"]
    if not query_type or not isinstance(query_type.get("fields"),list):
        raise ValueError("official Swiss GraphQL query schema not available")
    matching=[f for f in query_type["fields"] if "econom" in f["name"].lower() or "consump" in f["name"].lower()]
    # Nested introspection is performed from REAL returned type names, never fabricated schema assumptions
    introspected=[]
    for f in matching:
        type_name=unwrapped(f["type"])
        if not type_name:continue
        detail=request(QUERY_NAMED,{"name":type_name})
        d=detail["data"]["__type"]
        introspected.append({"name":f["name"],"type":type_name,
                             "type_details":d,
                             "raw_response_sha256":detail["raw_sha256"]})
        if isinstance(d,dict):
            for sub in (d.get("fields") or []):
                if "lca" in sub["name"].lower() or "life" in sub["name"].lower() or "impact" in sub["name"].lower():
                    typ=unwrapped(sub["type"])
                    if typ:
                        obj=request(QUERY_NAMED,{"name":typ})
                        introspected.append({"parent_field":f["name"],"name":sub["name"],
                           "type":typ,"type_details":obj["data"]["__type"],
                           "raw_response_sha256":obj["raw_sha256"]})
    return {
        "schema_version":"ptxlens.bafu_official_graphql_schema.v0.1",
        "discovery_utc":datetime.now(timezone.utc).isoformat(),
        "provider":"Swiss Federal Office for the Environment (BAFU/FOEN)",
        "source":ENDPOINT,
        "documentation":DOCUMENTATION,
        "expected_database_version":EXPECTED_VERSION,
        "expected_method":"IPCC 2021 / GWP 100",
        "request_status":root["http_status"],
        "original_root_response_sha256":root["raw_sha256"],
        "root_fields":[{"name":f["name"],"return_type":unwrapped(f["type"])} for f in query_type["fields"]],
        "economy_or_consumption_namespaces":introspected,
        "is_authentic_linked_native_openlca":False,
        "source_license_note":"Official Swiss OGD: open use, must attribute original BAFU data; specific Nexus inventory licence separate",
    }


def save_json(doc, path):
    p=Path(path)
    if p.exists():raise FileExistsError("refuse to overwrite registered source evidence")
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(doc,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=discover_schema()
    save_json(result,args.output)
    print(json.dumps({"root_fields":result["root_fields"],
          "target_schema":result["economy_or_consumption_namespaces"],
          "provider":result["provider"],"status":"source introspection only"},
          indent=2,ensure_ascii=False)[:12000])
