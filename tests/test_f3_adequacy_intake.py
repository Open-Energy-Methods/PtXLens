"""Contract-only synthetic tests; not source 2023 calculations."""
import copy
import hashlib
import json
import pytest

from ptxlens.f3_adequacy_intake import (
    assess_certificate_for_lca, UnacceptableAdequacyEvidence, SOURCE_E, SOURCE_ES,
    TARGET_KG,
)


def sample():
    target = TARGET_KG
    e = {
        "status": "BOUNDED_INCUMBENT_MINIMUM_UNPROVEN",
        "shortfall_lower_bound_kg": 1000.0,
        "shortfall_upper_bound_kg": 2000.0,
        "minimum_shortfall_certified": False,
        "positive_minimum_shortfall_proven": True,
        "full_original_demand_shortfall_lower_bound_kg": 18250000.0-target+1000,
        "full_original_demand_shortfall_upper_bound_kg": 18250000.0-target+2000,
        "annual_operating_cost_eur": None, "native_full_system_GWP_kgCO2e": None,
    }
    es = copy.deepcopy(e)
    es.update(status="PROVEN_MINIMUM", shortfall_lower_bound_kg=0.0,
              shortfall_upper_bound_kg=0.0, minimum_shortfall_certified=True,
              positive_minimum_shortfall_proven=False,
              full_original_demand_shortfall_lower_bound_kg=18250000-target,
              full_original_demand_shortfall_upper_bound_kg=18250000-target)
    return {
        "schema_version": "ptxflex.f3_stage_a_adequacy_certificates.v1",
        "original_source_E_sha256": SOURCE_E, "original_source_EplusS_sha256": SOURCE_ES,
        "reference_service_kg": target, "full_original_demand_kg": 18250000.0,
        "preexisting_source_E_shortfall_kg": 18250000.0-target,
        "model_assumptions_not_vendor_validated": True,
        "not_a_matched_service_cost_or_environmental_comparison": True,
        "physical_installation_BOM_LCIA_TEA_complete": False,
        "cases": {"max_inventory": {"E":e,"E_plus_S":es}}
    }


def ingest(data, *, replace_bytes=None, replace_sha=None):
    raw = json.dumps(data, sort_keys=True).encode() if replace_bytes is None else replace_bytes
    sha = hashlib.sha256(raw).hexdigest() if replace_sha is None else replace_sha
    return assess_certificate_for_lca(data, upstream_sha256=sha, original_bytes=raw)


def test_physically_unmatched_adequacy_is_not_comparative_lca():
    d=ingest(sample())
    mode=d["scenario_modes"]["max_inventory"]
    assert not mode["modelled_equal_hourly_service_adequacy_demonstrated"]
    assert not mode["full_life_cycle_comparison_eligible"]
    assert not d["environmental_or_financial_superiority_claim_allowed"]
    assert mode["cases"]["E_plus_S"]["verified_zero_shortfall"]
    assert mode["cases"]["E"]["minimum_positive_shortfall_proven"]


def test_even_two_zero_shortfall_cases_still_require_actual_native_LCIA_and_BOM():
    x=sample()
    r=x["cases"]["max_inventory"]["E"]
    r.update(status="PROVEN_MINIMUM",shortfall_lower_bound_kg=0.,shortfall_upper_bound_kg=0.,
             minimum_shortfall_certified=True,positive_minimum_shortfall_proven=False,
             full_original_demand_shortfall_lower_bound_kg=18250000-TARGET_KG,
             full_original_demand_shortfall_upper_bound_kg=18250000-TARGET_KG)
    mode=ingest(x)["scenario_modes"]["max_inventory"]
    assert mode["modelled_equal_hourly_service_adequacy_demonstrated"]
    assert not mode["full_life_cycle_comparison_eligible"]


@pytest.mark.parametrize("mutator",[
    lambda x: x.update(original_source_E_sha256="0"*64),
    lambda x: x.update(physical_installation_BOM_LCIA_TEA_complete=True),
    lambda x: x["cases"]["max_inventory"]["E"].update(shortfall_lower_bound_kg=3000),
    lambda x: x["cases"]["max_inventory"]["E"].update(full_original_demand_shortfall_upper_bound_kg=12),
    lambda x: x["cases"]["max_inventory"]["E"].update(annual_operating_cost_eur=1),
    lambda x: x["cases"]["max_inventory"]["E"].update(native_full_system_GWP_kgCO2e=0),
    lambda x: x["cases"]["max_inventory"]["E"].update(minimum_shortfall_certified=True),
    lambda x: x["cases"]["max_inventory"]["E"].update(positive_minimum_shortfall_proven=False),
    lambda x: x["cases"]["max_inventory"]["E"].update(shortfall_lower_bound_kg=float("nan")),
])
def test_cannot_accept_corrupted_or_overclaiming_F3_evidence(mutator):
    x=sample();mutator(x)
    with pytest.raises(UnacceptableAdequacyEvidence):
        ingest(x)


def test_source_artifact_sha_must_match_real_bytes():
    x=sample()
    with pytest.raises(UnacceptableAdequacyEvidence,match="source artifact bytes changed"):
        ingest(x, replace_sha="0"*64)
