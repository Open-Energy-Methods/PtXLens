"""RC1 science-gate and paired-public-release negative regression tests."""
import copy
import json
from pathlib import Path

import pytest

from ptxlens import rc1_release_audit as m


ROOT = Path(__file__).resolve().parents[1]
GATES = json.loads((ROOT / "research/gates-v1.0.json").read_text(encoding="utf-8"))


def test_pre_release_full_science_gates_fail_closed():
    result = m.validate_gate_document(copy.deepcopy(GATES))
    assert result["all_work_packages"] == 12
    assert len(result["not_passed_work_packages"]) == 12
    assert result["hydrogen_core_v1_allowed"] is False
    assert result["full_methanol_v1_allowed"] is False
    assert result["verified_independent_external_scientific_review"] is False


@pytest.mark.parametrize("case", [
    "fake_core_release", "fake_methanol_release",
    "unreviewed_pass", "passed_with_blocked_parent",
    "cycle", "missing_gate", "duplicate_gate",
    "blank_archive_preservation_date",
])
def test_false_scientific_release_statements_rejected(case):
    d = copy.deepcopy(GATES)
    rows = d["work_packages"]
    if case == "fake_core_release":
        d["release_readiness"]["hydrogen_core_v1_allowed"] = True
    elif case == "fake_methanol_release":
        d["release_readiness"]["full_methanol_v1_allowed"] = True
    elif case == "unreviewed_pass":
        rows[0]["gate_result"] = "PASSED"
        rows[0]["status"] = "verified"
    elif case == "passed_with_blocked_parent":
        by_id = {row["id"]: row for row in rows}
        p1 = by_id["P1"]
        p1["gate_result"] = "PASSED"
        p1["status"] = "verified"
        p1["acceptance_evidence"] = ["source review"]
        p1["last_scientific_review"] = "2026-11-18"
    elif case == "cycle":
        rows[0]["depends_on"].append("X2")
    elif case == "missing_gate":
        rows.pop()
    elif case == "duplicate_gate":
        rows[-1] = copy.deepcopy(rows[0])
    elif case == "blank_archive_preservation_date":
        d["source_and_licensing_guardrails"]["original_source_archive_expiry_date"] = None
    with pytest.raises(m.RC1AuditError):
        m.validate_gate_document(d)


def test_git_public_path_scanner_rejects_raw_data_and_broken_LF(tmp_path):
    src = ROOT / ".gitattributes"
    attrs = src.read_text(encoding="utf-8")
    assert all(x in attrs.splitlines() for x in m.LF_PAIRS + m.L3G_LF_PAIRS)
    assert ".zolca" in m.DENIED_SUFFIXES and ".zip" in m.DENIED_SUFFIXES
    assert m.SECRET_PATTERNS[0].search(
        b"-----BEGIN PRIVATE KEY-----") is not None
    assert m.SECRET_PATTERNS[1].search(
        b"github_pat_" + b"a" * 30) is not None
    with pytest.raises(m.RC1AuditError):
        m.safe_read(tmp_path, "../research/gates-v1.0.json")


def test_source_governance_cross_repo_byte_lock_when_peer_available():
    peer = ROOT.parent / "PtXFlex"
    if not peer.is_dir():
        peer = ROOT / "_external_ptxflex_source"
    if not peer.is_dir():
        pytest.skip("paired checkout not available on this host")
    result = m.audit(ROOT, peer)
    assert result["decision"] == (
        "RC1_STRUCTURAL_SOURCE_EVIDENCE_PASS_FULL_SCIENTIFIC_V1_BLOCKED")
    assert len(result["paired_governance_SHA256"]) == 4
    assert result["audited_scoped_public_evidence"][
        "exact_public_reconstructed_L3F_files"] == 8
    assert result["audited_scoped_public_evidence"][
        "exact_public_L3G_manifest_files"] == 2
    assert result["unqualified_v1_0_release_approved"] is False
    assert result["main_branch_mergeability_verified_by_RC1"] is False
    assert result["software_supply_chain_fully_locked_or_audited"] is False
