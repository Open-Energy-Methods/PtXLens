"""Download a *real*, public Commons Merged JSON-LD repo with immutable evidence.

No synthetic/fake database. Never commits or uploads raw LCI archive.
Uses user API key from environment, demo key only for exploratory testing.
"""
from __future__ import annotations
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request,urlopen
import zipfile

BASE="https://api.nal.usda.gov/FederalLCACommonsapi"
GROUP="Federal_LCA_Commons"
REPO="commons_merged"
MAX_BYTES=850_000_000


def get_url(path):
    key=os.environ.get("LCA_COMMONS_API_KEY","DEMO_KEY")
    if not key or not key.strip():
        raise RuntimeError("FLCAC API key is missing")
    return f"{BASE}{path}?"+urlencode({"api_key":key})


def retrieve_json(path,*,opener=urlopen):
    url=get_url(path)
    req=Request(url,headers={"Accept":"application/json","User-Agent":"PtXLens/0.2 academic database coverage"})
    with opener(req,timeout=240) as resp:
        raw=resp.read(80_001)
        status=getattr(resp,"status",200)
        kind=resp.headers.get("Content-Type","")
        location=resp.headers.get("Location","")
    if len(raw)>80_000:
        raise ValueError("unexpectedly large prepare response; refusing")
    if not raw.strip():
        raise RuntimeError(f"FLCAC prepare returned empty body (HTTP {status}, type={kind}, location_present={bool(location)}); no archive created")
    try:
        return json.loads(raw)
    except (ValueError, UnicodeError) as ex:
        # Some API versions return a plain-text token; never log it.
        text=raw.decode("utf-8",errors="replace").strip()
        if (5<=len(text)<=200 and all(c.isalnum() or c in "-_." for c in text)
                and "html" not in kind.lower()):
            return {"token":text}
        marker=("HTML" if "<html" in text.lower() or "<!doctype" in text.lower()
                else "unrecognized body")
        raise RuntimeError(f"FLCAC prepare HTTP {status}, Content-Type {kind}, {len(raw)} bytes ({marker}); no archive") from ex


def retrieve_zip(target_path,*,opener=urlopen):
    """Full repository download; return exact SHA, never upload raw file."""
    target_path=Path(target_path)
    if target_path.exists():
        raise FileExistsError("never overwrite database download")
    prepare=retrieve_json(f"/download/json/prepare/{GROUP}/{REPO}",opener=opener)
    token=prepare.get("token") if isinstance(prepare,dict) else None
    if not isinstance(token,str) or len(token)<5:
        raise ValueError("No valid download token returned by Commons API; not downloaded")
    # Official API guide documents GET /download/json/{token}.
    url=get_url("/download/json/"+token)
    req=Request(url,headers={"Accept":"application/zip,application/octet-stream","User-Agent":"PtXLens/0.2 academic database coverage"})
    digest=hashlib.sha256()
    count=0
    target_path.parent.mkdir(parents=True,exist_ok=True)
    try:
        with opener(req,timeout=500) as response, target_path.open("xb") as stream:
            content_type=response.headers.get("Content-Type","")
            while True:
                b=response.read(1024*1024)
                if not b:break
                count+=len(b)
                if count>MAX_BYTES:
                    raise ValueError("Commons archive > maximum 850MB; abort")
                digest.update(b)
                stream.write(b)
        if not zipfile.is_zipfile(target_path):
            raise ValueError("repository response is not a JSON-LD ZIP; inspect server response but do not invent a dataset")
    except Exception:
        target_path.unlink(missing_ok=True)
        raise
    with zipfile.ZipFile(target_path) as f:
        members=f.infolist()
        by_dir={}
        for member in members:
            if member.is_dir():continue
            prefix=member.filename.split("/",1)[0]
            by_dir[prefix]=by_dir.get(prefix,0)+1
        # Large archive may contain thousands of JSON records.
        if len(members)<20:
            raise ValueError("repo ZIP contains suspiciously few entries")
        sample=[x.filename for x in members[:25]]
    return {
       "schema_version":"ptxlens.commons_real_download.v0.1",
       "retrieved_utc":datetime.now(timezone.utc).isoformat(),
       "provider":"US Federal LCA Commons (NAL) data.gov API",
       "group":GROUP,"repository":REPO,
       "api_prepare_url_without_key":f"{BASE}/download/json/prepare/{GROUP}/{REPO}",
       "source_archive_sha256":digest.hexdigest(),"archive_bytes":count,
       "file_count":len(members),"top_level_entry_counts":by_dir,
       "sample_paths":sample,
       "original_archive_retained_only_on_CI_runner":True,
       "note":"Raw archive never committed, may include mixed industry datasets with distinct source licences",
    }


def write_report(out, report):
    out=Path(out)
    if out.exists():raise FileExistsError("refuse overwrite")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--archive",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    args=p.parse_args()
    doc=retrieve_zip(args.archive)
    write_report(args.manifest,doc)
    print(json.dumps(doc,indent=2,sort_keys=True))
