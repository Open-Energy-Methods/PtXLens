"""F3-D source 2023 original ZIP pair > 8 authenticated E+S pressure studies.

Only six of eight original source-derived price/wind stress comparisons have
both E and E+S certified to HiGHS 1e-6 MIP gap and independently equal-hour H2.
Ten percent weaker wind produced NO ACCEPTED INCUMBENT, not a mathematical
infeasibility proof. Null means unknown, not negative benefit or zero.
"""
import json
from pathlib import Path
import pytest
import ptxlens.f3d_independent_2023_stress_finance_bridge as m


@pytest.mark.parametrize("mode",["max_inventory","usable_service"])
@pytest.mark.parametrize("scenario",m.SCENARIOS)
def test_all_eight_original_f3d_source_results_immutable_without_new_historical_year_claim(mode,scenario):
    d=m.source_one(mode,scenario)
    assert d["schema_version"]==m.F3D_SCHEMA
    assert d["source_observed_year"]==2023
    assert d["actual_new_2022_or_2024_observed_pairing"] is False
    assert d["counterfactual_not_an_independently_verified_historical_weather_or_market_year"]
    assert d["source_stageA_shortage_constructive_not_globally_minimal"]
    assert d["original_2023_hourly_E_feasible_common_H2_target_SHA256"]==m.MODE_SHAS[mode]
    assert d["source_full_original_2023_industrial_contract_kg"]==18250000
    assert d["original_full_contract_H2_still_unserved_kg"]>1900000
    assert d["manufacturer_fully_installed_20t_incremental_storage_CAPEX_eur"] is None
    assert d["matched_native_BAFU_GWP_per_kg_H2"] is None
    assert d["whole_plant_economic_GWP_and_v1_0_release_PASSED"] is False
    if scenario=="wind_090_multiplier":
        assert d["paired_modelled_incremental_EplusS_wholesale_saving_eur2023_COUNTERFACTUAL_not_forecast"] is None
        assert d["paired_modelled_source_HiGHS_error_saving_bounds_eur2023"] is None
        assert not d["both_H2_source_cases_certified_MIP_gap_le_1e6"]
        assert d["E"]["solver_outcome"]=="NO_ACCEPTED_INCUMBENT_OR_FAILED_UNKNOWN"
        assert d["E_plus_S"]["solver_outcome"]=="NO_ACCEPTED_INCUMBENT_OR_FAILED_UNKNOWN"
    else:
        assert d["both_H2_source_cases_certified_MIP_gap_le_1e6"]
        a=d["paired_modelled_incremental_EplusS_wholesale_saving_eur2023_COUNTERFACTUAL_not_forecast"]
        lo,hi=d["paired_modelled_source_HiGHS_error_saving_bounds_eur2023"]
        assert lo<=a<=hi
        assert hi-lo<100
        assert a>0.
        assert d["E"]["source_TypeI_screened_200bar_pressure_OK"]
        assert d["E_plus_S"]["source_TypeI_screened_200bar_pressure_OK"]


@pytest.mark.parametrize("mode,expected",[
  ("max_inventory",{
   "price_circular_168h":726848.434048567,
   "price_centered_spread_150":1709869.7413428687,
   "wind_110_multiplier":1028799.9265977517
  }),
  ("usable_service",{
   "price_circular_168h":720619.0668690689,
   "price_centered_spread_150":1681102.6950972378,
   "wind_110_multiplier":994497.9194853678
  })
])
def test_source_2023_six_certified_robustness_price_sensitivity_is_not_universal_annual_saving(mode,expected):
    import math
    for stress,euro in expected.items():
        row=m.source_one(mode,stress)
        assert row["paired_modelled_incremental_EplusS_wholesale_saving_eur2023_COUNTERFACTUAL_not_forecast"]==pytest.approx(euro,abs=.005)


def test_all_eight_source_rows_are_properly_typed_six_certified_and_two_unknown():
    d=m.synthesize_independent_comparison()
    assert d["schema_version"]==m.SCHEMA
    assert d["original_observed_weather_and_market_year"]==2023
    assert d["zero_independently_observed_new_2022_2024_price_wind_pairs_retrieved"]
    assert d["price_wind_counterfactuals_NOT_observed_new_years"]
    assert d["source_wind_multiplier_090_110_does_not_physically_recalculate_ERA5_turbine_powers"]
    assert d["certified_matched_source_year_scenarios_count"]==6
    assert d["unknown_result_short_wind_source_scenarios_count"]==2
    assert d["market_robustness_therefore_NOT_a_predictive_confidence_interval"]
    assert d["manufacturer_installed_extra_20t_typeI_storage_cost_eur"] is None
    assert d["native_BAFU2026_v11_exact_matched_source_LCIA_kgCO2e"] is None
    assert d["full_true_hydrogen_LCOH_and_plant_preference"] is None
    assert not d["scientific_v1_full_release_passed"]
    assert len(d["rows"])==8
    unknown=[a for a in d["rows"] if not a["both_cases_solver_optimality_certified_to_1e6"]]
    assert len(unknown)==2
    assert {a["source_2023_counterfactual_stress_id"] for a in unknown}=={"wind_090_multiplier"}
    for r in unknown:
        assert r["source_2023_counterfactual_wholesale_EplusS_saving_eur"] is None
        assert r["conditional_20y_8pct_no_extra_cost_C0_max_eur_2023_basis"] is None
        assert r["undetermined_is_not_mathematical_infeasibility"]
    certified=[a for a in d["rows"] if a["both_cases_solver_optimality_certified_to_1e6"]]
    assert len(certified)==6
    for a in certified:
        assert a["source_2023_counterfactual_wholesale_EplusS_saving_eur"]>0
        assert a["conditional_20y_8pct_no_extra_cost_C0_max_eur_2023_basis"]>0
        assert a["conditional_20y_8pct_no_extra_cost_C0_minmax_due_ONLY_to_solver_gap_eur"][0]<a["conditional_20y_8pct_no_extra_cost_C0_max_eur_2023_basis"]+1e-3
        assert a["manufacturer_CAPEX_EUR_or_site_LCOH_GWP"] is None
        assert a["future_2023_model_difference_repeats_each_year_NOT_forecast"]


@pytest.mark.parametrize("mode,scenario",[
    ("max_inventory","price_circular_168h"),
    ("usable_service","wind_090_multiplier"),
])
def test_modified_original_source_2023_json_is_rejected_before_2023_cashflow(monkeypatch,tmp_path,mode,scenario):
    src=m.ROOT/"data/results"/f"F3_D_2023_{mode}_{scenario}_COUNTERFACTUAL_NOT_other_observed_year.json"
    d=json.loads(src.read_text(encoding="utf-8"))
    d["manufacturer_fully_installed_20t_incremental_storage_CAPEX_eur"]=0.
    path=tmp_path/"data/results";path.mkdir(parents=True)
    (path/src.name).write_text(json.dumps(d))
    monkeypatch.setattr(m,"ROOT",tmp_path)
    with pytest.raises(m.UnqualifiedCounterfactualEconomicFinding,match="source SHA changed"):
        m.source_one(mode,scenario)
