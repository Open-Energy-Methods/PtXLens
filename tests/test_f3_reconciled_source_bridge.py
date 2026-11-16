"""Real, source-hash-pinned F3 modelled adequacy verification and falsification."""
import json
import pytest
from ptxlens.f3_reconciled_source_bridge import (
    F3_PATH,F3_DERIVED_SHA256,ReconciledF3EvidenceError,
    read_verified_f3_evidence,comparative_lca_gate,
)


def test_source_derived_evidence_sha_and_critical_original_shortage_values():
    x=read_verified_f3_evidence()
    assert x["schema_version"]=="ptxflex.f3_2023_pressure_adequacy_reconciled.v1"
    assert F3_DERIVED_SHA256=="5dead18cfa0c3fecf15562f423e01044bcc6ad4ba4f5212dfb44a010b0d1a0d3"
    for mode in ("max_inventory","usable_service"):
        e=x["modes"][mode]["cases"]["E"]
        es=x["modes"][mode]["cases"]["E_plus_S"]
        assert e["minimum_additional_modelled_H2_shortfall_lower_bound_kg"]>0
        assert e["minimum_additional_modelled_H2_shortfall_upper_bound_kg"]>=e["minimum_additional_modelled_H2_shortfall_lower_bound_kg"]
        assert es["minimum_additional_modelled_H2_shortfall_upper_bound_kg"]==0
    assert x["modes"]["max_inventory"]["cases"]["E"]["minimum_additional_modelled_H2_shortfall_lower_bound_kg"]>65000
    assert x["modes"]["usable_service"]["cases"]["E"]["minimum_additional_modelled_H2_shortfall_lower_bound_kg"]>3700


def test_full_native_LCA_and_full_cost_not_inferred_from_source_pressure_shortage():
    gate=comparative_lca_gate()
    assert not gate["same_hourly_delivered_service_achieved_in_both"]
    assert gate["system_native_manufacturing_GWP_kgCO2e"] is None
    assert gate["full_system_LCOH_EUR_kg"] is None
    assert not gate["direct_comparative_environmental_or_financial_claim_allowed"]


def test_tampered_source_JSON_fails_even_if_new_document_is_internally_consistent(tmp_path):
    x=json.loads(F3_PATH.read_text())
    x["modes"]["max_inventory"]["cases"]["E"]["minimum_additional_modelled_H2_shortfall_lower_bound_kg"]=0
    path=tmp_path/"f3_tampered.json"
    path.write_text(json.dumps(x))
    with pytest.raises(ReconciledF3EvidenceError,match="SHA-256 changed"):
        read_verified_f3_evidence(path)
