"""F3-C PtXLens release: source 2023 pressure E/E+S hourly service and wholesale cost only.

Actual numerical source results are 4 separately independently source-verified
original 2023 CI MILPs; all source JSON bytes registered by exact SHA256.
Tampered cost, hourly checksum, pressure claims, physical CAPEX or source
full-annual demand claims are rejected BEFORE computing any paired comparison.
"""
import json
import math
from pathlib import Path

import pytest
import ptxlens.f3c_common_service_bridge as bridge


def test_2023_source_four_cases_are_immutable_and_matched_within_capacity_semantics():
    r=bridge.compare_all_modes()
    assert r["schema_version"]==bridge.BRIDGE_SCHEMA
    assert r["source_year"]==2023
    assert r["source_2023_weather_observations_and_NL_A44_original_matched"]
    assert r["service_is_original_E_source_feasible_stageA_incumbent_not_full_contract"]
    assert r["pressure_screened_TypeI_200bar_and_RVO_compression_electricity_included"]
    assert r["not_dynamic_compressor_or_plant_validated"]
    assert r["native_BAFU_complete_LCA_and_discounted_LCOH_missing"]
    assert not r["l1_l2_l3_v1_0_RELEASE_PASSED"]
    assert set(r["modes"])=={"max_inventory","usable_service"}
    for mode,z in r["modes"].items():
        a=bridge.source_one(mode,"E")
        b=bridge.source_one(mode,"E_plus_S")
        assert a["common_hourly_modelled_H2_service_float64_sha256"]==b["common_hourly_modelled_H2_service_float64_sha256"]
        assert a["source_StageA_E_hourly_json_sha256"]==b["source_StageA_E_hourly_json_sha256"]
        assert z["reference_common_annual_modelled_service_kg"]<bridge.REFERENCE
        assert z["remaining_unserved_original_full_contract_kg"]>1_914_720
        assert z["EplusS_saving_interval_mip_bounds_eur"][0]>0
        assert (z["EplusS_saving_interval_mip_bounds_eur"][0]
                <=z["EplusS_2023_wholesale_saving_eur"]
                <=z["EplusS_saving_interval_mip_bounds_eur"][1])
        assert z["original_source_initial_kg_differs_with_storage_capacity"]
        assert not z["actual_economic_preference_or_full_plant_LCA_claim_permitted"]
        assert z["native_BAFU_2026_v1_1_full_physical_plant_GWP_kgCO2e"] is None
        assert z["installed_40t_vs_20t_CAPEX_and_discounted_lifetime_cashflow_eur"] is None
        assert z["annual_compression_MWh_E"]>0
        assert z["annual_compression_MWh_EplusS"]>0


@pytest.mark.parametrize("mode,service,saving",[
   ("max_inventory",16268755.000838026,1124332.2692838833),
   ("usable_service",16331558.946374645,1103463.7287309095),
])
def test_original_source_modelled_2023_matched_service_specific_numerical_results(mode,service,saving):
    r=bridge.compare_one_mode(mode)
    assert math.isclose(r["reference_common_annual_modelled_service_kg"],service,abs_tol=.002)
    assert math.isclose(r["EplusS_2023_wholesale_saving_eur"],saving,abs_tol=.02)
    assert r["EplusS_saving_interval_mip_bounds_eur"][0]>0
    assert r["source_data_evidence_sha256"]["E"]==bridge.REGISTERED[mode]["E"]
    assert r["source_data_evidence_sha256"]["E_plus_S"]==bridge.REGISTERED[mode]["E_plus_S"]


@pytest.mark.parametrize("field,new",[
 ("native_full_BAFU_2026_v1_1_GWP",0.0),
 ("solver_optimality_certified_to_gap_1e_6",False),
 ("source_2023_wholesale_operating_cost_feasible_incumbent_eur",0.0),
 ("common_hourly_modelled_H2_service_float64_sha256","0"*64),
 ("original_full_2023_industrial_contract_kg",16335279.317376737),
 ("2023_plant_or_vendor_validated",True),
])
def test_bytes_modified_cannot_be_promoted_to_source_licensed_comparison(tmp_path,monkeypatch,field,new):
    root=tmp_path
    d=root/"data/results";d.mkdir(parents=True)
    raw=(bridge.ROOT/"data/results/F3_C_2023_source_pressure_matched_max_inventory_E.json").read_text()
    x=json.loads(raw);x[field]=new
    (d/"F3_C_2023_source_pressure_matched_max_inventory_E.json").write_text(json.dumps(x))
    monkeypatch.setattr(bridge,"ROOT",root)
    with pytest.raises(bridge.InvalidCommonServiceEvidence,match="hash mismatch"):
        bridge.source_one("max_inventory","E")


def test_mismatched_mode_hourly_profile_rejected_even_when_both_individual_files_pass_sha(monkeypatch):
    old=bridge.source_one
    def different(mode,case):
        x=old(mode,case)
        if case=="E_plus_S": x=dict(x,common_hourly_modelled_H2_service_float64_sha256="0"*64)
        return x
    monkeypatch.setattr(bridge,"source_one",different)
    with pytest.raises(bridge.InvalidCommonServiceEvidence,match="NOT serving the same byte-for-byte hourly profile"):
        bridge.compare_one_mode("usable_service")


def test_savings_cannot_be_claimed_without_source_mip_dual_consistency(monkeypatch):
    old=bridge.source_one
    def corrupted(mode,case):
        d=old(mode,case)
        if case=="E_plus_S":
            d=dict(d,solver_lower_bound_wholesale_eur=d["source_2023_wholesale_operating_cost_feasible_incumbent_eur"]+1e6)
        return d
    monkeypatch.setattr(bridge,"source_one",corrupted)
    with pytest.raises(bridge.InvalidCommonServiceEvidence,match="bound interval invalid"):
        bridge.compare_one_mode("max_inventory")
