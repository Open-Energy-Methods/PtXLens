"""A byte-for-byte integrity gate, not a silent source column mapper."""
import csv
import hashlib
import json
from pathlib import Path

def inspect_verified_artifact(dispatch_csv, manifest_json):
    dispatch, manifest = Path(dispatch_csv), Path(manifest_json)
    meta = json.loads(manifest.read_text(encoding="utf-8"))
    digest = hashlib.sha256(dispatch.read_bytes()).hexdigest()
    if meta.get("verified") is not True or digest != meta.get("dispatch_sha256"):
        raise ValueError("PyNEXUS artifact is unverified or has changed")
    with dispatch.open(encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream)
        columns = next(reader, None)
        count = sum(1 for _ in reader)
    if not columns or len(set(columns)) != len(columns) or count != meta.get("snapshots"):
        raise ValueError("PyNEXUS row count/columns mismatch")
    return {"verified": True, "dispatch_sha256": digest,
            "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
            "rows": count, "source_columns": columns,
            "original_source_kind": meta.get("input_source", {}).get("kind"),
            "source_commit": meta.get("git_sha")}
