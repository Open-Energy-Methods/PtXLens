"""Probe actual Federal LCA Commons API without guessing provider coverage.

The output is an API evidence record; it NEVER marks a material linked merely
because text search matched. Uses no synthetic record and no implicit fallbacks.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE="https://api.nal.usda.gov/FederalLCACommonsapi"
SEARCHES=("titanium","aluminium","stainless steel","copper","nafion","activated carbon","iridium","platinum","water treatment","hydrogen compression","electricity offshore wind")
GROUP="Federal_LCA_Commons"
REPO="commons_merged"


def request_json(path, params, *, opener=urlopen):
    key=os.environ.get("LCA_COMMONS_API_KEY","DEMO_KEY")
    if not key.strip():
        raise RuntimeError("empty API key; set LCA_COMMONS_API_KEY (or use low-rate DEMO_KEY)")
    query=urlencode({**params,"api_key":key})
    url=f"{BASE}{path}?{query}"
    safe_url=f"{BASE}{path}?"+urlencode({**params,"api_key":"[REDACTED]"})
    req=Request(url,headers={"Accept":"application/json","User-Agent":"PtXLens/0.2 scholarly non-commercial dataset quality audit"})
    try:
        with opener(req,timeout=55) as resp:
            payload=resp.read(5_000_001)
            status=getattr(resp,"status",200)
        if len(payload)>5_000_000:
            raise ValueError("LCA Commons JSON response > 5 MB; refusing unexpected payload")
        data=json.loads(payload)
        return {"ok":True,"http_status":status,"request_url_redacted":safe_url,
                "response_sha256":hashlib.sha256(payload).hexdigest(),
                "response_type":type(data).__name__,"response":data}
    except HTTPError as error:
        detail=error.read(600).decode("utf-8",errors="replace")
        return {"ok":False,"http_status":error.code,"request_url_redacted":safe_url,
                "error_excerpt":detail}
    except (URLError, TimeoutError) as error:
        return {"ok":False,"http_status":None,"request_url_redacted":safe_url,
                "error_excerpt":str(error)[:300]}


def run_probe(output:Path, *, terms=("titanium","platinum"), delay_seconds=2):
    output=Path(output)
    if output.exists():
        raise FileExistsError("refusing to overwrite prior API response evidence")
    logs=[]
    for term in terms:
        event=request_json("/search",{"query":term,"group":GROUP,"repo":REPO,
                                         "type":"PROCESS","pageSize":5})
        event["query"]=term
        # Keep a small but authentic sample of the response, no fake IDs/names.
        # For errors, report API response; don't present as no available process.
        logs.append(event)
        time.sleep(delay_seconds)
    out={
        "schema_version":"ptxlens.federal_lca_api_probe.v0.1",
        "timestamp_utc":datetime.now(timezone.utc).isoformat(),
        "source":"US Federal LCA Commons USDA NAL live data.gov gateway",
        "documentation":"https://www.lcacommons.gov/lca-commons-api-guide",
        "target_group":GROUP,"target_repo":REPO,
        "queries":logs,
        "interpretation":"Search matches are NOT provider validation. HTTP failure is NOT evidence of missing processes.",
    }
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
    return out


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--all",action="store_true")
    args=p.parse_args(argv)
    terms=SEARCHES if args.all else ("titanium","platinum")
    record=run_probe(args.output,terms=terms)
    for query in record["queries"]:
        response=query.get("response")
        shape=list(response)[:8] if isinstance(response,dict) else type(response).__name__
        print(json.dumps({"query":query["query"],"http":query["http_status"],
                          "ok":query["ok"],"response_keys":shape,
                          "result_type":query.get("response_type"),
                          "error":query.get("error_excerpt","")[:180]}))
    if not any(q["ok"] for q in record["queries"]):
        raise SystemExit("NO verified API results; blocked, see artifact diagnostics")


if __name__=="__main__":
    main()
