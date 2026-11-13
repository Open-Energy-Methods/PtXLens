"""Fail-closed intake for PtXFlex full-year Stage A adequacy certificates.

This is a provenance and matched-delivery decision gate, NOT a hydrogen LCA
or TEA calculation. The approved hash must be obtained independently from
an actual upstream GitHub Actions artifact; supplying a self-chosen hash
does not establish independent source provenance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

SCHEMA = "ptxflex.f3_stage_a_adequacy_certificates.v1"
SOURCE_E = "069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051"
SOURCE_ES = "cd4101fe62c3f1b8aa2d7508d3651d2fee40d2bafe6d5b87e40d5f4d055070f9"
TARGET_KG = 16335279.317376737


class UnacceptableAdequacyEvidence(ValueError):
    pass


def _quantity(value, key):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise UnacceptableAdequacyEvidence("nonfinite/unregistered numerical bound: " + key)
    return float(value)


def assess_certificate_for_lca(data, *, upstream_sha256, original_bytes):
    """Require source-locked evidence and refuse incompatible environmental claims."""
    if (not isinstance(upstream_sha256, str) or len(upstream_sha256) != 64
            or any(c not in "0123456789abcdef" for c in upstream_sha256)):
        raise UnacceptableAdequacyEvidence("external source artifact SHA256 required")
    if hashlib.sha256(original_bytes).hexdigest() != upstream_sha256:
        raise UnacceptableAdequacyEvidence("source artifact bytes changed")
    if data.get("schema_version") != SCHEMA:
        raise UnacceptableAdequacyEvidence("not a Stage A executable-MILP shortage certificate")
    if (data.get("original_source_E_sha256") != SOURCE_E
            or data.get("original_source_EplusS_sha256") != SOURCE_ES):
        raise UnacceptableAdequacyEvidence("original source input mismatch")
    target = _quantity(data.get("reference_service_kg"), "reference_service_kg")
    full = _quantity(data.get("full_original_demand_kg"), "full_original_demand_kg")
    original_gap = _quantity(data.get("preexisting_source_E_shortfall_kg"), "preexisting_source_E_shortfall_kg")
    if abs(target - TARGET_KG) > 0.002 or abs(full - 18250000) > 0.002 or abs(full - target - original_gap) > .002:
        raise UnacceptableAdequacyEvidence("source target / original shortfall changed")
    if (data.get("model_assumptions_not_vendor_validated") is not True
            or data.get("not_a_matched_service_cost_or_environmental_comparison") is not True
            or data.get("physical_installation_BOM_LCIA_TEA_complete") is not False):
        raise UnacceptableAdequacyEvidence("unverified plant or complete comparison claim")
    modes = data.get("cases")
    if not isinstance(modes, dict) or not modes:
        raise UnacceptableAdequacyEvidence("no historical scenarios to assess")
    output = {
        "schema": "ptxlens.stage_a_source_adequacy_intake.v1",
        "upstream_sha256": upstream_sha256,
        "reference_modelled_H2_service_kg": target,
        "full_original_H2_demand_kg": full,
        "native_storage_LCIA_completed": False,
        "system_TEA_completed": False,
        "environmental_or_financial_superiority_claim_allowed": False,
        "scenario_modes": {},
    }
    for mode, rows in modes.items():
        if mode not in ("max_inventory", "usable_service") or not isinstance(rows, dict) or not rows:
            raise UnacceptableAdequacyEvidence("invalid capacity semantics or missing cases")
        accepted = {}
        for case, r in rows.items():
            if case not in ("E", "E_plus_S") or not isinstance(r, dict):
                raise UnacceptableAdequacyEvidence("unexpected historical H2 scenario")
            if "annual_operating_cost_eur" in r and r["annual_operating_cost_eur"] is not None:
                raise UnacceptableAdequacyEvidence("invalid annual cost inference from adequacy stage")
            if "native_full_system_GWP_kgCO2e" in r and r["native_full_system_GWP_kgCO2e"] is not None:
                raise UnacceptableAdequacyEvidence("invalid complete native GWP inference")
            status = r.get("status")
            if status == "NOT_CERTIFIED":
                if r.get("shortfall_lower_bound_kg") is not None or r.get("shortfall_upper_bound_kg") is not None:
                    raise UnacceptableAdequacyEvidence("uncertified result carries an invented bound")
                accepted[case] = {"source_status": status, "verified_zero_shortfall": False,
                                  "minimum_positive_shortfall_proven": False}
                continue
            if status not in ("PROVEN_MINIMUM", "BOUNDED_INCUMBENT_MINIMUM_UNPROVEN"):
                raise UnacceptableAdequacyEvidence("unrecognized F3 physical shortage certification")
            lo = _quantity(r.get("shortfall_lower_bound_kg"), "shortfall_lower_bound_kg")
            hi = _quantity(r.get("shortfall_upper_bound_kg"), "shortfall_upper_bound_kg")
            if lo < 0 or hi < 0 or lo > hi + .01 or hi > target + .01:
                raise UnacceptableAdequacyEvidence("mathematically invalid minimization interval")
            if abs(_quantity(r.get("full_original_demand_shortfall_lower_bound_kg"), "full gap lower")-(original_gap+lo)) > .002:
                raise UnacceptableAdequacyEvidence("original full-contract shortfall lower bound is inconsistent")
            if abs(_quantity(r.get("full_original_demand_shortfall_upper_bound_kg"), "full gap upper")-(original_gap+hi)) > .002:
                raise UnacceptableAdequacyEvidence("original full-contract shortfall upper bound is inconsistent")
            if r.get("minimum_shortfall_certified") is not (status == "PROVEN_MINIMUM"):
                raise UnacceptableAdequacyEvidence("false solver optimality classification")
            if r.get("positive_minimum_shortfall_proven") is not (lo > .01):
                raise UnacceptableAdequacyEvidence("false proved positive inadequacy claim")
            accepted[case] = {
                "source_status": status, "minimum_positive_shortfall_proven": lo > .01,
                "verified_zero_shortfall": hi <= 1e-7,
                "additional_shortfall_lower_bound_kg": lo,
                "additional_shortfall_upper_bound_kg": hi,
            }
        # A paired modelled full-delivery witness is necessary, not sufficient,
        # for an actual system/environmental functional-unit comparison.
        paired_zero = all(c in accepted and accepted[c]["verified_zero_shortfall"]
                          for c in ("E", "E_plus_S"))
        output["scenario_modes"][mode] = {
            "modelled_equal_hourly_service_adequacy_demonstrated": paired_zero,
            "full_life_cycle_comparison_eligible": False,
            "cases": accepted,
            "remaining_gates": ["complete_source_matched_hourly_dispatch_evidence",
                                "vessel_manufacturing_material_provider_compatibility",
                                "compressor_and_cooler_BOM_and_operating_losses",
                                "complete_native_BAFU_v1.1_LCIA",
                                "harmonized_full_system_discounted_cash_flow",
                                "independent_physical_and_scientific_review"],
        }
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--expected-sha256", required=True, help="independently registered upstream artifact SHA")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    dest = Path(args.output)
    if dest.exists():
        raise FileExistsError("never overwrite previously ingested source study evidence")
    original = Path(args.input).read_bytes()
    report = assess_certificate_for_lca(json.loads(original), upstream_sha256=args.expected_sha256, original_bytes=original)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, sort_keys=True, indent=2, allow_nan=False)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
