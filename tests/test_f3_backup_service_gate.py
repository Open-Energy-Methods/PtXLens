"""Source-hash registered PtXLens backup load gate; no plant/supply validation."""
import json
import pytest

from ptxlens.f3_backup_service_gate import (
    InvalidBackstopSource, verify_source_backup_load, service_equivalence_barrier,
    ROOT,EXPECTED_BACKUP_SHA256,
)


def test_both_original_historical_source_backup_load_envelopes_verified():
    x=service_equivalence_barrier()
    assert x["original_source_hourly_shortage_proof_f3_imported"]
    assert not x["comparative_LCA_TEA_allowed"]
    a=x["scenarios"]["max_inventory"]
    b=x["scenarios"]["usable_service"]
    assert a["backup_annual_topup_for_one_source_feasible_incumbent_kg"]>65000
    assert b["backup_annual_topup_for_one_source_feasible_incumbent_kg"]>3700
    assert a["backup_peak_hourly_requirement_for_that_incumbent_kg_h"]>1000
    assert b["backup_peak_hourly_requirement_for_that_incumbent_kg_h"]>180
    assert a["backup_peak_24h_requirement_for_that_incumbent_kg"]>a["backup_peak_hourly_requirement_for_that_incumbent_kg_h"]
    assert not a["eligible_for_matched_service_native_BAFU_and_DCF"]
    assert not b["eligible_for_matched_service_native_BAFU_and_DCF"]


@pytest.mark.parametrize("mode",["max_inventory","usable_service"])
def test_original_source_missing_backup_impact_and_cost_cannot_be_interpreted_as_zero(mode):
    a=verify_source_backup_load(mode)
    assert a["incremental_backup_H2_kgCO2e_per_kg"] is None
    assert a["incremental_backup_cost_EUR_per_kg"] is None
    assert a["external_H2_supplier_physically_specified"] is False
    assert a["backup_full_lca_or_tea_complete"] is False


@pytest.mark.parametrize("mutation",[
    lambda x:x.update(incremental_backup_H2_kgCO2e_per_kg=0),
    lambda x:x.update(incremental_backup_cost_EUR_per_kg=0),
    lambda x:x.update(external_H2_supplier_physically_specified=True),
    lambda x:x.update(hourly_shortage_magnitude_is_a_modelled_feasible_incumbent_not_global_optimum=False),
    lambda x:x.update(single_incumbent_hypothetical_topup_max_kg_per_hour=0),
    lambda x:x.update(single_incumbent_hypothetical_topup_annual_kg=200000),
    lambda x:x.update(source_2023_original_E_reference_delivered_kg=0),
])
def test_unauthorized_or_physically_overclaiming_evidence_is_rejected(tmp_path,mutation):
    obj=json.loads((ROOT/"F3_2023_original_E_source_hypothetical_backup_max_inventory.json").read_text())
    mutation(obj)
    p=tmp_path/"fake.json";p.write_text(json.dumps(obj))
    with pytest.raises(InvalidBackstopSource,match="SHA256"):
        verify_source_backup_load("max_inventory",path=p)
