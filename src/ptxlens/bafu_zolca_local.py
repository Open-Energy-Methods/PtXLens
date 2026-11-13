"""Inspect a BAFU:2026 .zolca file previously obtained through Nexus.

This program never downloads, logs into Nexus, or accepts third-party licence
terms on behalf of a user. Files stay local. It validates the archive's Derby
backup structure before GreenDelta's native Java .zolca restore is attempted.
"""
from __future__ import annotations
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
import stat
import zipfile

CITATION="Database of the Swiss Federal Administration, BAFU:2026, Federal Office for the Environment, 2026"
EXPECTED_EDITION="BAFU:2026 v1"
MAX_UNCOMPRESSED_BYTES=25*1024**3
MAX_MEMBERS=200_000


def inspect_zolca(filename):
    p=Path(filename)
    if p.suffix.lower()!=".zolca" or not p.is_file():
        raise ValueError("requires the legally obtained inner .zolca file, not the outer Nexus .zip")
    digest=hashlib.sha256()
    with p.open("rb") as stream:
        for block in iter(lambda:stream.read(1024*1024),b""):
            digest.update(block)
    if not zipfile.is_zipfile(p):
        raise ValueError("source .zolca is not a valid ZIP-compatible openLCA backup")
    count=0
    bytes_total=0
    has={"service.properties":False,"log":False,"seg0":False}
    with zipfile.ZipFile(p) as z:
        for info in z.infolist():
            count+=1
            if count>MAX_MEMBERS:
                raise ValueError("archive has excessive number of files")
            name=info.filename.replace("\\","/")
            parts=name.split("/")
            if (name.startswith("/") or any(part in ("","..") for part in parts if part != parts[-1])
                    or ".." in parts or "\x00" in name):
                raise ValueError("unsafe backup ZIP path")
            if info.is_dir():continue
            mode=(info.external_attr>>16)&0xffff
            if stat.S_ISLNK(mode):
                raise ValueError("symbolic link inside source .zolca not permitted")
            bytes_total+=info.file_size
            if bytes_total>MAX_UNCOMPRESSED_BYTES:
                raise ValueError("archive expansion exceeds local guardrail")
            if name=="service.properties":has["service.properties"]=True
            if name.startswith("log/"):has["log"]=True
            if name.startswith("seg0/"):has["seg0"]=True
    if not all(has.values()) or count<50:
        raise ValueError("source not a native Derby .zolca database; extract the inner file from Nexus package")
    return {
        "schema_version":"ptxlens.BAFU2026_user_supplied_native_archive_preflight.v0.1",
        "inspected_utc":datetime.now(timezone.utc).isoformat(),
        "expected_source_edition":EXPECTED_EDITION,
        "edition_verified_from_nexus_account":False,
        "publication_citation":CITATION,
        "original_archive_sha256":digest.hexdigest(),
        "archive_size_bytes":p.stat().st_size,
        "uncompressed_bytes":bytes_total,
        "member_count":count,
        "native_openlca_Derby_backup_structure_verified":True,
        "can_claim_provider_complete":False,
        "file_contents_not_copied_to_git_or_artifacts":True,
        "remaining_verification":"Run genuine openLCA 2.7 native Java import and check BAFU:2026 process UUIDs/flows, provider completeness and named IPCC method."
    }


def main(argv=None):
    import argparse
    a=argparse.ArgumentParser()
    a.add_argument("source",type=Path)
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args(argv)
    if args.output.exists():raise FileExistsError("refusing to overwrite source fingerprint")
    out=inspect_zolca(args.source)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
