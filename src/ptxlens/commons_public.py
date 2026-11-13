"""Download the truly public Commons Merged openLCA JSON-LD archive.

Uses the collaboration server's documented public webservice, rather than
USDA NAL API keys. No synthetic data and no licensed archive redistribution.
"""
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request,urlopen
import zipfile

BASE="https://lcacommons.gov/lca-collaboration/ws/public/download/json"
GROUP="Federal_LCA_Commons"
REPO="commons_merged"
MAX_BYTES=900_000_000


def download(output_zip):
    path=Path(output_zip)
    if path.exists():raise FileExistsError("do not overwrite verified source archive")
    prep=f"{BASE}/prepare/{GROUP}/{REPO}"
    headers={"User-Agent":"PtXLens/0.2 academic reproducibility",
             "Accept":"application/json,text/plain"}
    with urlopen(Request(prep,headers=headers),timeout=240) as resp:
        body=resp.read(1000)
    if len(body)>900:raise ValueError("unexpected long public archive token body")
    s=body.decode("utf-8-sig").strip()
    try:
        doc=json.loads(s)
        token=doc.get("token","") if isinstance(doc,dict) else doc
    except ValueError:
        token=s
    if not isinstance(token,str) or not (5<=len(token)<=300) or "/" in token or " " in token:
        raise ValueError("collaboration server did not return a valid opaque archive token")
    url=f"{BASE}/{quote(token,safe='')}"
    digest=hashlib.sha256()
    count=0
    path.parent.mkdir(parents=True,exist_ok=True)
    try:
        with urlopen(Request(url,headers={"User-Agent":headers["User-Agent"],"Accept":"application/zip"}),timeout=650) as resp, path.open("xb") as w:
            while True:
                block=resp.read(1024*1024)
                if not block:break
                count+=len(block)
                if count>MAX_BYTES:
                    raise ValueError("archive too large for runner (limit 900MB)")
                digest.update(block)
                w.write(block)
        if not zipfile.is_zipfile(path):
            raise ValueError("server response is not openLCA JSON-LD ZIP")
        with zipfile.ZipFile(path) as archive:
            infos=archive.infolist()
            if len(infos)<100:
                raise ValueError("Commons Merged archive unexpectedly small")
            dirs={}
            for info in infos:
                name=info.filename.split("/")[0]
                dirs[name]=dirs.get(name,0)+1
            result={
                "schema_version":"ptxlens.commons_public_full_archive.v0.1",
                "acquired_at_utc":datetime.now(timezone.utc).isoformat(),
                "download_provider":BASE,
                "group":GROUP,"repository":REPO,
                "download_sha256":digest.hexdigest(),"size_bytes":count,
                "member_count":len(infos),"top_level_member_counts":dirs,
                "first_paths":[x.filename for x in infos[:20]],
                "claim":"authentic public FLCAC JSON-LD; no provider completeness or native LCA yet",
                "archive_not_redistributed":True,
            }
        return result
    except BaseException:
        path.unlink(missing_ok=True)
        raise


def record(result, output_file):
    out=Path(output_file)
    if out.exists():raise FileExistsError("refusing to overwrite")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--archive",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    args=p.parse_args()
    result=download(args.archive)
    record(result,args.manifest)
    print(json.dumps(result,indent=2,sort_keys=True))
