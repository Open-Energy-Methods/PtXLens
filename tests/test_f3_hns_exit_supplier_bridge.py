"""Source-verified E hourly H2 need; prospective TSO is NOT H2 purchaser/supplier."""
import json
import pytest
from ptxlens.f3_hns_exit_supplier_bridge import (
    CANDIDATE, RESULT_SHA256,
    IneligibleContractualH2Source,audited_H2_supplier_qualification_result,
    native_BAFU_full_LCA_and_DCF_gate,
)


def test_real_source_2023_8760_hour_inputs_and_prospective_2026_hns_split():
    a=audited_H2_supplier_qualification_result()
    assert a["model_year"]==2023
    assert a["source_2026_Hynetwork_operator_terms_are_not_actual_2023_gas_supply"]
    assert a["network_operator_does_not_guarantee_hydrogen_supply"]
    for mode,e in a["modes"].items():
        assert e["actual_connection_total_peak_HHV_kWh_h"] is None
        assert e["max_2023_incumbent_replacement_H2_kg_h"]>0
        assert e["incremental_topup_HNS_CSA_study_form_HHV_kWh_h"]>0
        assert e["mathematical_boundary_cases"]["EXACT_PEAK_FLOW_20BARA_PERFECT_UPTIME"]["unmet_h2_kg"]==0
        assert not e["mathematical_boundary_cases"]["EXACT_PEAK_FLOW_20BARA_PERFECT_UPTIME"]["physical_supplier_verified"]


def test_lca_and_DCF_must_remain_null_without_2023_site_and_two_distinct_contracts():
    d=native_BAFU_full_LCA_and_DCF_gate()
    assert d["upstream_source_json_sha256"]==RESULT_SHA256
    assert not d["user_original_pyNEXUS_hydrogen_customer_site_location_known"]
    assert not d["actual_customer_exit_CDS_pressure_to_20_bar_absolute_verified"]
    assert not d["supplier_separately_signed_purchase_shipper_nomination_verified"]
    assert not d["full_comparative_E_vs_ES_LCA_or_TEA_permitted"]
    assert d["matched_8760h_2023_modelled_h2_EOL_or_GWP"] is None
    assert d["source_backed_whole_plant_EUR_discounted_cashflow"] is None


@pytest.mark.parametrize("fake",[
 lambda d:d.update(network_operator_does_not_guarantee_hydrogen_supply=False),
 lambda d:d.update(supplier_contract_exit_connection_contract_both_missing=False),
 lambda d:d["modes"]["max_inventory"].update(actual_connection_total_peak_HHV_kWh_h=50000),
 lambda d:d["modes"]["max_inventory"]["mathematical_boundary_cases"]["EXACT_PEAK_FLOW_20BARA_PERFECT_UPTIME"].update(physical_supplier_verified=True),
 lambda d:d.update(native_BAFU_full_comparative_GWP=3.0),
])
def test_unapproved_changed_contract_or_GWP_cannot_pass_sha_and_lca(tmp_path,fake):
    obj=json.loads(CANDIDATE.read_text())
    fake(obj)
    p=tmp_path/"falsified.json";p.write_text(json.dumps(obj))
    with pytest.raises(IneligibleContractualH2Source,match="unregistered source"):
        audited_H2_supplier_qualification_result(p)
