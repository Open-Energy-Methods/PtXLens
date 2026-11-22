"""RC2-A/B audit of public provenance receipts and reconciled science gates.

The recorded 2023 owner-controlled private archive SHA/ZIP CRC inspection is
historical audit evidence, not recreated by this offline public-only runner.
Original raw files and temporary/owner storage locators never enter this audit.
The existing F3D publication admission is repeated on public source summaries;
no private hourly input, MILP tree, native BAFU LCIA or industrial proof reruns.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from . import f3d_2024_crossyear_publication as crossyear
from . import rc1_release_audit as rc1

RECEIPT = "research/RC2_SOURCE_PROVENANCE_AND_YEAR_EVIDENCE_2026-11-18.json"
ORIGINAL_STATUS = "research/P0_2023_PyNEXUS_original_actions_artifacts_live_status_2026-11-14.json"
SOURCE = "research/F3D_ARCO_2022_2024_PUBLIC_VERIFIED_AGGREGATES_v1.json"
IR = "data/results/" + crossyear.STEM + ".json"
IDS = {"E": 12612294862, "E_plus_S": 12613045475,
       "A44_original_market_provider_XML": 12610917985}


def need(ok, reason):
    if not ok:
        raise ValueError("RC2 source/governance audit: " + reason)


def git_blob(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def reconcile(receipt, old_status, source, h30, gates):
    need(receipt.get("schema_version") == "oem.ptx.rc2_source_provenance_and_calendar_scope.v1",
         "unknown provenance receipt")
    p = receipt["original_2023_pynexus"]
    original = {x["case"]: x for x in old_status["source_artifacts"]}
    actual = {x["case"]: x for x in p["original_artifacts"]}
    need(len(p["original_artifacts"]) == 3 and set(actual) == set(original) == set(IDS),
         "three immutable original archives required")
    for k in IDS:
        a, o = actual[k], original[k]
        need(a["artifact_id"] == o["artifact_id"] == IDS[k] and
             all(a[key] == o[key] for key in ("size_bytes", "expires_at_UTC",
                                              "verified_source_archive_sha256")) and
             a["expired"] is False and
             all(a[key] is True for key in (
                 "api_sha256_digest_matches_frozen_registry",
                 "existing_private_owner_copy_readback_sha256_matches_registry",
                 "existing_private_owner_copy_readback_zip_crc_passed",
                 "existing_private_owner_copy_byte_length_matches_registry")),
             "original archive receipt differs from registry: " + k)
    need(p["earliest_observed_retention_expiry_utc"] ==
         min(x["expires_at_UTC"] for x in actual.values()), "wrong earliest source expiry")
    need(p["existing_owner_controlled_private_archive_readback_all_three_sha256_crc_verified"] is True and
         p["readback_temporary_analysis_is_NOT_second_permanent_independent_backup"] is True and
         all(p[k] is False for k in (
             "permanent_independent_physical_backup_and_full_restore_verified",
             "original_source_provider_licensing_independently_reviewed",
             "external_scientific_review_verified", "P0_full_release_gate_passed",
             "private_storage_locators_credentials_or_raw_source_bytes_in_report")),
         "private readback receipt promoted beyond verified scope")
    evidence = receipt["alternate_year_source_evidence"]
    need(evidence["original_2023_CDS_ARCO_full_year_calibration_passed_in_prior_source_evidence"] is True and
         source["2023_CDS_to_ARCO_full_year_original_source_calibration_passed"] is True and
         evidence["original_2023_CDS_ARCO_full_year_1W_reference_sha256"] ==
         source["2023_CDS_to_ARCO_8760_hour_1W_source_reference_SHA256"],
         "original 2023 calibration scope changed")
    pairs = evidence["source_pairs"]
    fixed = evidence["separately_prespecified_fixed_H30_W090_max_inventory_cases"]
    need([x["year"] for x in pairs] == [2022, 2024] and [x["year"] for x in fixed] == [2022, 2024],
         "two distinct source-calendar pairs required")
    need(len(source["cases"]) == 4 and len(h30["source_year_results"]) == 2,
         "selected-service vs prespecified-service case count changed")
    for row, expected_hours in zip(pairs, (8760, 8784)):
        year = row["year"]
        cases = [x for x in source["cases"] if x["year"] == year]
        need(len(cases) == 2 and
             {x["storage_capacity_semantics"] for x in cases} == {"max_inventory", "usable_service"},
             "missing paired capacity mode")
        need(row["calendar_utc_hours"] == expected_hours and row["original_source_hash_and_calendar_admitted"] is True,
             "wrong calendar or source admission")
        rows = row["separate_price_neutral_E_selected_service_cases"]
        need(len(rows) == 2 and len({x["storage_capacity_semantics"] for x in rows}) == 2,
             "selected-service capacity modes merged/repeated")
        for x in cases:
            need(x["year_utc_hours"] == expected_hours and
                 x["source_original_provider_pair_receipt_sha256"] == row["source_provider_pair_receipt_sha256"] and
                 x["source_year_price_f64_sha256"] == row["source_price_f64_sha256"] and
                 x["source_year_wind_f64_sha256"] == row["source_wind_electric_power_f64_sha256"] and
                 x["source_original_hash_and_calendar_gate_passed"] is True,
                 "year has stale/different original source receipt or vector hash")
            y = next(r for r in rows if r["storage_capacity_semantics"] == x["storage_capacity_semantics"])
            need(y["selected_tonnes_per_day"] == x["price_neutral_E_uniform_hydrogen_service"]["modelled_delivered_h2_tonnes_per_day"] and
                 y["paired_integer_primal_replayed"] is x["independent_full_hourly_E_and_EplusS_primal_replay_passed"] is True and
                 y["paired_eos_replayed"] is x["independent_full_hourly_type_I_20_to_200bar_EOS_replay_passed"] is True and
                 y["integer_search_dual_independently_reconstructed"] is x["independent_solver_dual_certificates_recomputed"] is False,
                 "selected-service numerical proof scope changed")
    for row, x, expected_hours in zip(fixed, h30["source_year_results"], (8760, 8784)):
        need(row["year"] == x["source_year"] and
             row["calendar_utc_hours"] == x["calendar_UTC_hours"] == expected_hours and
             row["annual_delivered_H2_kg"] == x["annual_delivered_H2_kg"] == 1250 * expected_hours and
             row["prespecified_h2_tonnes_per_day"] == x["exogenous_hydrogen_tonnes_per_day"] == 30. and
             row["wind_electric_power_factor"] == x["original_wind_electric_power_multiplier"] == .9 and
             row["source_year_nominal_wholesale_saving_eur"] == x["source_year_wholesale_E_minus_EplusS_saving_eur"] and
             row["paired_integer_primal_replayed"] is x["original_source_two_integer_primal_replays"] is True and
             row["integer_search_dual_independently_reconstructed"] is x["integer_search_tree_dual_independently_reconstructed"] is False,
             "H30 W090 fixed rather than selected service result differs")
    need(evidence["F3D_source_year_8784_hour_capable_for_these_verified_studies"] is True and
         evidence["original_2023_frozen_PyNEXUS_unchanged"] is True and
         all(evidence[key] is False for key in (
             "original_full_50t_day_contract_served_or_real_site_validated",
             "all_private_alternate_year_raw_archives_freshly_read_by_RC2",
             "native_BAFU_matched_storage_LCIA_or_real_OEM_cost_certified",
             "full_scientific_v1_allowed")),
         "prior narrowly scoped source validation overclaimed")
    state = rc1.validate_gate_document(gates)
    f = gates["release_readiness"]
    r = f["rc2_reconciliation"]
    need(len(state["not_passed_work_packages"]) == 12 and
         not state["hydrogen_core_v1_allowed"] and not state["full_methanol_v1_allowed"] and
         f["f3d_independently_observed_2022_2024_price_and_ERA5_pairs_admitted"] is True and
         f["f3d_real_2022_2024_A44_and_ERA5_authenticated_pair_count"] == 2 and
         f["f3d_2024_leap_year_8784_hour_milp_source_model_certified_compatible"] is True and
         f["f3d_original_2023_offshore_ERA5_100m_to_hub120_repro_SHA_certified_for_newyear_pipeline"] is True and
         r["public_provenance_receipt"] == RECEIPT and
         r["original_three_private_ZIPs_retrieved_SHA256_CRC_verified"] is True and
         r["admitted_distinct_2022_2024_source_year_pairs"] == 2 and
         r["prior_price_neutral_selected_service_year_mode_pairs"] == 4 and
         r["prior_exogenous_H30_W090_max_inventory_year_pairs"] == 2 and
         r["permanent_independent_physical_backup_and_restoration_verified"] is False and
         r["original_source_licensing_and_external_review_verified"] is False and
         r["fresh_RC2_readback_of_raw_alternate_year_source_arrays"] is False and
         r["full_scientific_v1_acceptance_criteria_unchanged"] is True,
         "reconciled gate flags silently promote full scientific readiness or use stale evidence")
    return {
        "historical_private_archive_readback_receipts_checked": 3,
        "prior_admitted_source_years": [2022, 2024],
        "prior_selected_service_year_mode_pairs": 4,
        "prior_fixed_H30_W090_max_inventory_year_pairs": 2,
        "full_programme_gates_NOT_PASSED": 12,
        "private_raw_archives_reread_by_this_public_audit": False,
        "independent_permanent_backup_verified": False,
        "full_scientific_v1_approved": False,
    }


def audit(lens_root, flex_root):
    lens, flex = Path(lens_root), Path(flex_root)
    l = rc1.safe_read(lens, RECEIPT)
    f = rc1.safe_read(flex, RECEIPT)
    need(l == f, "shared RC2 receipt differs between repositories")
    receipt = json.loads(l)
    a = rc1.safe_read(flex, SOURCE)
    b = rc1.safe_read(lens, IR)
    e = receipt["alternate_year_source_evidence"]
    need(git_blob(a) == e["public_flex_aggregate_git_blob_sha1"] and
         git_blob(b) == e["public_lens_h30_w090_crossyear_git_blob_sha1"],
         "source-pinned released report Git blob changed")
    old = json.loads(rc1.safe_read(flex, ORIGINAL_STATUS))
    gates = json.loads(rc1.safe_read(lens, "research/gates-v1.0.json"))
    need(rc1.safe_read(lens, "research/gates-v1.0.json") ==
         rc1.safe_read(flex, "research/gates-v1.0.json"),
         "shared reconciliation register differs")
    output = reconcile(receipt, old, json.loads(a), json.loads(b), gates)
    reconstructed = crossyear.audit(lens / "data/results", flex / SOURCE)
    need(reconstructed == json.loads(b), "original F3D cross-year admission did not reproduce")
    # Includes the ten original L3-F/L3-G result reports and original governance lock.
    rc1.audit(lens, flex)
    output["decision"] = "RC2_SOURCE_RECEIPT_AND_GOVERNANCE_AUDIT_PASS_P0_AND_SCIENTIFIC_V1_BLOCKED"
    return output


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--lens-root", required=True, type=Path)
    p.add_argument("--flex-root", required=True, type=Path)
    a = p.parse_args(argv)
    result = audit(a.lens_root, a.flex_root)
    print(result["decision"])
    print("2023 archived readback receipt: 3 originals; 2022/2024 admitted source pairs: 2; "
          "4 selected-service and 2 fixed-H30 cases; all 12 science gates NOT PASSED.")
    print("No private bytes reread by this public runner; independent backup and external review blocked.")


if __name__ == "__main__":
    main()
