"""Original 2023 full-hour wind-10 PtXFlex E+S LP model feasibility independent QA.

The LP result is mathematical feasibility evidence ONLY for the identical
2023 source 200bar(a) TypeI model; not site evidence nor a priced asset.
"""
import json
import pytest
import ptxlens.f3d_weakwind_lp_independent_review as m


@pytest.mark.parametrize("mode",["max_inventory","usable_service"])
def test_exact_2023_source_hour_E_ES_lp_relaxed_original_H2_constraints_status2(mode):
    d=m.verify_one(mode)
    assert d["schema_version"]==m.EXPECTED
    assert d["mode"]==mode
    assert d["source_year"]==2023
    assert d["both_original_source_E_and_ES_relaxed_LPs_reported_infeasible"]
    assert d["source_2023_common_h2_hourly_SHA256"]==m.MODE_SHAS[mode]
    assert d["paired_economic_preference_OR_certified_wholesale_savings_eur"] is None
    assert not d["full_LCA_LCOH_and_v1_release_passed"]
    for item in (d["E"],d["E_plus_S"]):
        assert item["solver_status_code"]==2
        assert "infeasible" in item["solver_status_message"].lower()
        assert item["all_original_hourly_electricity_H2_storage_pressure_compressor_constraints_preserved"]
        assert item["LP_feasibility_objective_zero_ignores_2023_wholesale_cost"]
        assert not item["LP_model_has_accepted_feasible_vector"]
        assert item["MILP_infeasibility_supported_if_LP_status_2"]
        assert item["actual_site_operational_infeasibility_certified"] is False


def test_two_modes_mathematical_superset_proof_NEVER_overwrites_source_economic_status():
    d=m.review_both()
    assert d["schema_version"]==m.SCHEMA
    assert d["source_original_ERA5_2023_and_ENTSOE_price2023_only"]
    assert d["counterfactual_wind_available_MW_multiplier"]==.9
    assert d["both_capacity_modes_and_both_E_and_EplusS_HiGHS_LP_status2"]
    assert d["solver_infeasible_LP_is_superset_of_original_binary_MILP"]
    assert d["modelled_source_hourly_target_unattainable_in_E_and_ES_under_wind_090"]
    assert d["full_real_site_hydrogen_unattainable_proven"] is False
    assert d["new_observed_2022_2024_data_retrieved"] is False
    assert d["relative_annual_wholesale_cost_under_stress_eur"] is None
    assert d["hypothetical_financial_capex_break_even_at_wind_090_eur"] is None
    assert d["native_full_BAFU_storage_manufacturing_GWP_kgCO2e"] is None
    assert not d["real_full_LCOH_and_industrial_plant_certified"]
    assert set(d["mode_original_source_LP_SHA256"])=={"max_inventory","usable_service"}


@pytest.mark.parametrize("mode",["max_inventory","usable_service"])
def test_scientific_original_source_weak_wind_lp_record_tampering_is_detected(
        tmp_path,monkeypatch,mode):
    source=m.ROOT/"data/results"/f"F3_D_2023_{mode}_wind090_original_source_LP_relaxation_NOT_plant_proof.json"
    fake=json.loads(source.read_text())
    fake["E"]["solver_status_code"]=0
    target=tmp_path/"data/results"
    target.mkdir(parents=True)
    (target/source.name).write_text(json.dumps(fake))
    monkeypatch.setattr(m,"ROOT",tmp_path)
    with pytest.raises(m.BadWeakWindProof,match="tampered"):
        m.verify_one(mode)
