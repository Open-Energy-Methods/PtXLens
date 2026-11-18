"""RC2 source receipt and scientific scope regressions (no private inputs)."""
import copy
import json
from pathlib import Path

import pytest

from ptxlens import rc2_provenance_governance as m

ROOT = Path(__file__).resolve().parents[1]


def peer_root():
    sibling = ROOT.parent / "PtXFlex"
    checkout = ROOT / "_external_ptxflex_source"
    for peer in (sibling, checkout):
        if (peer / m.RECEIPT).is_file():
            return peer
    pytest.skip("matching RC2 PtXFlex checkout not available")


def inputs():
    peer = peer_root()
    read = lambda root, p: json.loads((root / p).read_text(encoding="utf-8"))
    return (read(ROOT, m.RECEIPT), read(peer, m.ORIGINAL_STATUS),
            read(peer, m.SOURCE), read(ROOT, m.IR),
            read(ROOT, "research/gates-v1.0.json"))


def test_actual_paired_source_registry_reconciliation():
    result = m.audit(ROOT, peer_root())
    assert result["decision"] == "RC2_SOURCE_RECEIPT_AND_GOVERNANCE_AUDIT_PASS_P0_AND_SCIENTIFIC_V1_BLOCKED"
    assert result["historical_private_archive_readback_receipts_checked"] == 3
    assert result["prior_admitted_source_years"] == [2022, 2024]
    assert result["prior_selected_service_year_mode_pairs"] == 4
    assert result["prior_fixed_H30_W090_max_inventory_year_pairs"] == 2
    assert result["full_programme_gates_NOT_PASSED"] == 12
    assert not result["private_raw_archives_reread_by_this_public_audit"]
    assert not result["independent_permanent_backup_verified"]
    assert not result["full_scientific_v1_approved"]


@pytest.mark.parametrize("case", [
    "fake_permanent_backup", "false_crc", "archive_changed", "wrong_leap_hours",
    "wrong_source_receipt", "duplicate_mode", "selected_confused_with_H30",
    "fake_full_solver_dual", "fake_fresh_readback", "stale_source_count",
    "fabricated_full_v1", "fake_licence",
])
def test_unadmitted_source_and_scope_claims_rejected(case):
    receipt, status, source, h30, gates = copy.deepcopy(inputs())
    owner = receipt["original_2023_pynexus"]
    alt = receipt["alternate_year_source_evidence"]
    if case == "fake_permanent_backup":
        owner["permanent_independent_physical_backup_and_full_restore_verified"] = True
    elif case == "false_crc":
        owner["original_artifacts"][0]["existing_private_owner_copy_readback_zip_crc_passed"] = False
    elif case == "archive_changed":
        owner["original_artifacts"][0]["verified_source_archive_sha256"] = "0" * 64
    elif case == "wrong_leap_hours":
        alt["source_pairs"][1]["calendar_utc_hours"] = 8760
    elif case == "wrong_source_receipt":
        alt["source_pairs"][1]["source_provider_pair_receipt_sha256"] = "f" * 64
    elif case == "duplicate_mode":
        rows = alt["source_pairs"][0]["separate_price_neutral_E_selected_service_cases"]
        rows[1]["storage_capacity_semantics"] = rows[0]["storage_capacity_semantics"]
    elif case == "selected_confused_with_H30":
        alt["separately_prespecified_fixed_H30_W090_max_inventory_cases"][0]["prespecified_h2_tonnes_per_day"] = 30.480648653278504
    elif case == "fake_full_solver_dual":
        alt["source_pairs"][0]["separate_price_neutral_E_selected_service_cases"][0]["integer_search_dual_independently_reconstructed"] = True
    elif case == "fake_fresh_readback":
        alt["all_private_alternate_year_raw_archives_freshly_read_by_RC2"] = True
    elif case == "stale_source_count":
        gates["release_readiness"]["f3d_real_2022_2024_A44_and_ERA5_authenticated_pair_count"] = 0
    elif case == "fabricated_full_v1":
        gates["release_readiness"]["hydrogen_core_v1_allowed"] = True
    elif case == "fake_licence":
        owner["original_source_provider_licensing_independently_reviewed"] = True
    with pytest.raises(ValueError):
        m.reconcile(receipt, status, source, h30, gates)
