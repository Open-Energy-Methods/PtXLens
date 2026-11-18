"""RC1 paired PtXFlex/PtXLens scientific release-candidate evidence audit.

This is a structural and immutable-evidence quality gate, NOT approval of
scientific v1.0, the site, the pressure system, the installed NPV or native
BAFU manufacture/replacement/end-of-life LCIA. Runs without private data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from . import l3g_release_qualification as l3g

SCHEMA = "ptxlens.rc1_paired_repo_release_evidence_audit.v1"
PACKAGE_IDS = {"P0", "P1", "F1", "F2", "L1", "F3", "L2", "L3", "F4", "L4", "X1", "X2"}
GOVERNANCE = (
    "contracts/ptx-exchange-v1.schema.json",
    "research/gates-v1.0.json",
    "docs/PROGRAMME_MASTER_PLAN_v1.0.md",
    "docs/DECISION_REGISTER_v1.0.md",
)
DENIED_SUFFIXES = {".zolca", ".spold", ".ecospold", ".zip", ".pem", ".key",
                   ".p12", ".pfx", ".nc", ".parquet", ".sqlite", ".db"}
SENSITIVE_BASENAMES = {".env", "credentials.json", "id_rsa", "id_ed25519"}
SECRET_PATTERNS = (
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"github_pat_[A-Za-z0-9_]{15,}"),
    re.compile(rb"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(rb"sk-[A-Za-z0-9]{24,}"),
    re.compile(rb"[A-Za-z]:\\Users\\", re.I),
)
LF_PAIRS = (
    "data/results/L3F_*.json text eol=lf",
    "data/results/L3F_*.md text eol=lf",
)
L3G_LF_PAIRS = (
    "data/results/L3G_*.json text eol=lf",
    "data/results/L3G_*.md text eol=lf",
)


class RC1AuditError(ValueError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RC1AuditError("RC1 paired release audit: " + message)


def safe_read(root: Path, relpath: str) -> bytes:
    need(type(relpath) is str and not relpath.startswith(("/", "\\")) and
         ".." not in Path(relpath).parts, "unsafe relative research path")
    f = root / relpath
    need(f.is_file() and not f.is_symlink(), "missing or symlink research path: " + relpath)
    return f.read_bytes()


def validate_gate_document(gates: dict) -> dict:
    """Validation is dependency-aware and prevents gate self-certification."""
    need(type(gates) is dict and
         gates.get("schema_version") == "oem.ptx.science-gates.v1.0",
         "programme research gate schema changed")
    rows = gates.get("work_packages")
    need(type(rows) is list and len(rows) == len(PACKAGE_IDS),
         "12 expected work packages missing/duplicated")
    by_id = {x.get("id"): x for x in rows}
    need(set(by_id) == PACKAGE_IDS, "work package IDs diverged")
    for row in rows:
        uid = row["id"]
        need(row.get("gate_result") in {"PASSED", "NOT_PASSED"} and
             row.get("status") in {"blocked", "in_progress", "verified", "not_started"},
             "missing accepted gate decision: " + uid)
        need(type(row.get("depends_on")) is list and
             set(row["depends_on"]).issubset(PACKAGE_IDS - {uid}) and
             len(row["depends_on"]) == len(set(row["depends_on"])),
             "invalid gate dependency: " + uid)
        if row["gate_result"] == "PASSED":
            need(row["status"] == "verified" and
                 row.get("acceptance_evidence") and
                 row.get("last_scientific_review"),
                 "unreviewed gate falsely marked PASSED: " + uid)
            need(all(by_id[p]["gate_result"] == "PASSED" for p in row["depends_on"]),
                 "scientific gate passed with blocked dependency: " + uid)
    visited: set[str] = set()
    visiting: set[str] = set()

    def visit(uid: str) -> None:
        need(uid not in visiting, "cycle in programme scientific gates")
        if uid in visited:
            return
        visiting.add(uid)
        for upstream in by_id[uid]["depends_on"]:
            visit(upstream)
        visiting.remove(uid)
        visited.add(uid)

    for uid in sorted(PACKAGE_IDS):
        visit(uid)

    flags = gates.get("release_readiness")
    need(type(flags) is dict, "scientific programme release flags absent")
    core = all(row["gate_result"] == "PASSED" for row in rows
               if row.get("required_for_hydrogen_core_v1") is True)
    full = all(row["gate_result"] == "PASSED" for row in rows
               if row.get("required_for_full_methanol_v1") is True)
    need(flags.get("hydrogen_core_v1_allowed") is core and
         flags.get("full_methanol_v1_allowed") is full,
         "science release flags contradict required evidence gates")
    source = gates.get("source_and_licensing_guardrails", {})
    expiry = source.get("original_source_archive_expiry_date")
    need(type(expiry) is str and re.fullmatch(r"\d{4}-\d{2}-\d{2}", expiry),
         "original model input evidence preservation date absent")
    return {
        "all_work_packages": len(rows),
        "not_passed_work_packages": sorted(
            x["id"] for x in rows if x["gate_result"] != "PASSED"),
        "hydrogen_core_v1_allowed": core,
        "full_methanol_v1_allowed": full,
        "original_source_archive_documented_expiry_date_NOT_LIVE_CHECK": expiry,
        "verified_independent_external_scientific_review":
            flags.get("independent_scientific_peer_review_passed") is True,
    }


def tracked_paths(root: Path) -> list[str]:
    try:
        p = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=20, check=False)
    except (OSError, subprocess.TimeoutExpired) as ex:
        raise RC1AuditError("git repository listing unavailable") from ex
    need(p.returncode == 0, "git ls-files failed; cannot evaluate tracked paths")
    return [x.decode("utf-8") for x in p.stdout.split(b"\0") if x]


def inspect_public_tree(root: Path, repo: str) -> dict:
    paths = tracked_paths(root)
    need(paths, "tracked public file listing empty: " + repo)
    bad_paths = [
        s for s in paths
        if Path(s).suffix.lower() in DENIED_SUFFIXES or
        Path(s).name.lower() in SENSITIVE_BASENAMES or
        s.startswith(("private-lci/", "private-source-escrow/",
                      "bafu-licensed-databases/", "PtX_PRIVATE_RESEARCH/"))
    ]
    need(not bad_paths,
         "licensed/private/raw input paths tracked in " + repo + ": " + ", ".join(bad_paths[:5]))
    attrs = safe_read(root, ".gitattributes").decode("utf-8")
    for rule in LF_PAIRS + (L3G_LF_PAIRS if repo == "PtXLens" else ()):
        need(rule in attrs.splitlines(),
             "source SHA audit lacks canonical Git LF rule: " + repo + "/" + rule)
    return {
        "repo": repo,
        "tracked_file_count": len(paths),
        "denylisted_original_provider_archive_file_paths": len(bad_paths),
        "canonical_windows_LF_result_rules": len(LF_PAIRS) +
            (len(L3G_LF_PAIRS) if repo == "PtXLens" else 0),
        "raw_provider_file_contents_secret_scanned": False,
    }


def verify_evidence_bytes(lens: Path, flex: Path, l3g_result: dict) -> dict:
    """E2E source reconstruction is delegated to L3-G. Screen its 10 outputs."""
    l3g.publish_local(l3g_result, output_dir=lens / "data/results", verify_only=True)
    rows = l3g_result["public_artifact_fingerprints_only"]
    need(len(rows) == 8, "L3-G source fingerprint count differs")
    outputs: list[tuple[str, bytes]] = []
    for row in rows:
        repo, relpath = row["repo"], row["relative_path"]
        data = safe_read(lens if repo == "PtXLens" else flex, relpath)
        need(hashlib.sha256(data).hexdigest() ==
             row["SHA256_exact_original_source_rebuilt"],
             "published source hash mismatch: " + repo + "/" + relpath)
        outputs.append((repo + "/" + relpath, data))
    for name in (l3g.OUT_JSON, l3g.OUT_MD):
        relpath = "data/results/" + name
        outputs.append(("PtXLens/" + relpath, safe_read(lens, relpath)))
    for path, data in outputs:
        need(data and b"\x00" not in data and b"\r" not in data,
             "non-canonical public output or binary: " + path)
        need(all(not expr.search(data) for expr in SECRET_PATTERNS),
             "sensitive credential/local path resembles token in: " + path)
    return {
        "exact_public_reconstructed_L3F_files": 8,
        "exact_public_L3G_manifest_files": 2,
        "public_scope_safety_checks_only": True,
        "full_repository_secret_scan_performed": False,
        "original_private_archives_read": False,
    }


def audit(lens_root: Path, flex_root: Path) -> dict:
    lens, flex = Path(lens_root).resolve(), Path(flex_root).resolve()
    need(lens != flex and lens.is_dir() and flex.is_dir(),
         "distinct paired PtXLens and PtXFlex local checkouts required")
    state = {}
    for name, root in (("PtXLens", lens), ("PtXFlex", flex)):
        state[name] = {
            "tree": inspect_public_tree(root, name),
            "gates": validate_gate_document(json.loads(
                safe_read(root, "research/gates-v1.0.json"))),
        }
    shared = {}
    for relpath in GOVERNANCE:
        x = safe_read(lens, relpath)
        y = safe_read(flex, relpath)
        need(x == y, "paired source-controlled scientific governance drift: " + relpath)
        shared[relpath] = hashlib.sha256(x).hexdigest()
    need(state["PtXLens"]["gates"] == state["PtXFlex"]["gates"],
         "same programme has two release-gate interpretations")
    evidence = l3g.audit(lens_results=lens / "data/results",
                         flex_results=flex / "data/results")
    qualified = verify_evidence_bytes(lens, flex, evidence)
    release = state["PtXLens"]["gates"]
    need(not release["hydrogen_core_v1_allowed"] and
         not release["full_methanol_v1_allowed"],
         "RC1 must be reevaluated if programme science v1 gates become passed")
    return {
        "schema_version": SCHEMA,
        "decision": "RC1_STRUCTURAL_SOURCE_EVIDENCE_PASS_FULL_SCIENTIFIC_V1_BLOCKED",
        "source_locked_research_claims_passed": True,
        "audited_scoped_public_evidence": qualified,
        "paired_repository_state": state,
        "paired_governance_SHA256": shared,
        "scientific_and_industrial_release_blocked": True,
        "external_OEM_PED_site_qualification_performed": False,
        "actual_project_NPV_or_native_BAFU_LCIA_reproduced": False,
        "original_annual_modelled_MILPs_rerun_by_RC1": False,
        "main_branch_mergeability_verified_by_RC1": False,
        "original_source_escrow_redundancy_verified": False,
        "software_supply_chain_fully_locked_or_audited": False,
        "unqualified_v1_0_release_approved": False,
    }


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--lens-root", required=True, type=Path)
    p.add_argument("--flex-root", required=True, type=Path)
    p.add_argument("--output", type=Path, help="Optional local JSON report; not committed automatically")
    p.add_argument("--require-full-v1", action="store_true",
                   help="Fail if complete scientific programme v1.0 is not approved")
    args = p.parse_args(argv)
    report = audit(args.lens_root, args.flex_root)
    if args.output is not None:
        path = args.output
        need(path.parent.is_dir() and not path.is_symlink() and
             not path.exists(), "report output must be a new ordinary path")
        with path.open("x", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, sort_keys=True, indent=2, allow_nan=False)
            f.write("\n")
    print(report["decision"])
    blocked = len(report["paired_repository_state"]["PtXLens"]["gates"]["not_passed_work_packages"])
    print("10 exact public reports, 4 matching scientific governance inputs, "
          f"{blocked}/12 full-programme gates NOT PASSED; no native LCIA/OEM/NPV")
    if args.require_full_v1:
        raise SystemExit("Scientific v1.0 blocked: RC1 structural evidence is not physical/scientific approval")


if __name__ == "__main__":
    main()
