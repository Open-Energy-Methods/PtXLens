"""L3-E exogenous H30/W090 incremental source-locked DCF science tests.

No supplier price, site evidence or native BAFU provider is invented by the
synthetic scenarios. Real fixture is the already-public Git-blob-pinned
independently reviewed 2022/2024 two-year source report, never hourly data.
"""
from dataclasses import replace
import json
import math

import pytest

from ptxlens import l3e_exogenous_incremental_dcf as m


def test_actual_published_exogenous_2022_2024_source_loaded_and_cost_matched():
    cases=m.load_admitted_source()
    assert set(cases)=={2022,2024}
    assert cases[2022]["annual_h2_kg"]==10950000.
    assert cases[2024]["annual_h2_kg"]==10980000.
    assert cases[2022]["source_annual_saving_eur"]==pytest.approx(
        3281613.054066889)
    assert cases[2024]["source_annual_saving_eur"]==pytest.approx(
        1931675.8526294443)
    for case in cases.values():
        assert case["source_solver_only_lower_eur"]<=case[
            "source_annual_saving_eur"]<=case["source_solver_only_upper_eur"]
        assert case["observed_cost_inputs_are_year_specific"] is True


def test_zero_discount_annual_cashflows_and_t0_incremental_capex():
    s=m.Scenario(horizon_years=10,real_discount_rate=0.,
                 historical_saving_repeat_fraction=1.,
                 added_annual_opex_year_eur=100.,
                 hypothetical_initial_capex_year_eur=500.)
    p=m.discount_stream(1000.,s)
    assert p["PV_repeated_modelled_wholesale_savings_year_eur"]==pytest.approx(10000.)
    assert p["PV_hypothetical_incremental_opex_year_eur"]==pytest.approx(1000.)
    z=m.frontier(1000.,1000.,1000.,s)
    assert z["hypothetical_extra_all_in_installed_CAPEX_zero_NPV_ceiling_year_eur"]==pytest.approx(9000.)
    assert z["at_assumed_CAPEX_hypothetical_incremental_NPV_year_eur"]==pytest.approx(8500.)
    assert z["hypothetical_annual_incremental_OPEX_zero_NPV_ceiling_at_assumed_CAPEX_year_eur"]==pytest.approx(950.)


def test_explicit_end_of_year_replacement_decreases_capex_by_discounted_cost():
    plain=m.Scenario(horizon_years=20,real_discount_rate=.08,
                     added_annual_opex_year_eur=250000.)
    change=replace(plain,replacements=((10,1000000.),))
    a=m.frontier(1931675.8526294443,1931675.5750419751,1931676.453831147,plain)
    b=m.frontier(1931675.8526294443,1931675.5750419751,1931676.453831147,change)
    delta=1000000./1.08**10
    key="hypothetical_extra_all_in_installed_CAPEX_zero_NPV_ceiling_year_eur"
    assert a[key]-b[key]==pytest.approx(delta)
    assert b["PV_hypothetical_replacements_year_eur"]==pytest.approx(delta)


def test_independent_20year_8pct_benchmark_follows_annuity_formula():
    sc=m.Scenario(horizon_years=20,real_discount_rate=.08,
                  added_annual_opex_year_eur=250000.)
    annuity=(1-1/1.08**20)/.08
    for benefit in (3281613.054066889,1931675.8526294443):
        z=m.frontier(benefit,benefit-.1,benefit+.1,sc)
        assert z["annuity_present_value_factor_years"]==pytest.approx(annuity)
        expected=(benefit-250000)*annuity
        assert z["hypothetical_extra_all_in_installed_CAPEX_zero_NPV_ceiling_year_eur"]==pytest.approx(expected)
        assert z["at_assumed_CAPEX_hypothetical_incremental_NPV_year_eur"]==pytest.approx(
            expected-10000000)
        assert z["hypothetical_annual_incremental_OPEX_zero_NPV_ceiling_at_assumed_CAPEX_year_eur"]==pytest.approx(
            benefit-10000000/annuity)


def test_source_bound_propagation_is_solver_numerics_not_weather_uncertainty():
    s=m.Scenario(horizon_years=10,real_discount_rate=.03,
                 annual_saving_fade_fraction=.02,
                 historical_saving_repeat_fraction=.75)
    r=m.frontier(300.,299.,302.,s)
    lo,hi=r["hypothetical_extra_all_in_CAPEX_solver_numerical_lower_upper_year_eur"]
    assert lo<=r["hypothetical_extra_all_in_installed_CAPEX_zero_NPV_ceiling_year_eur"]<=hi
    assert r["original_solver_error_bound_only_NOT_future_saving_uncertainty"] is True
    assert r["project_actually_profitable_with_verified_vendor_costs"] is None
    with pytest.raises(m.MatchedStorageDCFError):
        m.frontier(300.,301.,302.,s)


@pytest.mark.parametrize("field,value",[
    ("horizon_years",0),("horizon_years",61),
    ("horizon_years",20.),
    ("real_discount_rate",-0.1),("real_discount_rate",1.),
    ("historical_saving_repeat_fraction",float("nan")),
    ("historical_saving_repeat_fraction",-1.),
    ("annual_saving_fade_fraction",1.),
    ("annual_saving_fade_fraction",-0.001),
    ("added_annual_opex_year_eur",-1.),
    ("hypothetical_initial_capex_year_eur",True),
    ("end_salvage_year_eur",float("inf")),
    ("end_decommission_year_eur",-5.),
    ("replacements",((22,1000.),)),
    ("replacements",((2,1000.),(2,2000.))),
])
def test_invalid_discount_replacement_and_false_cost_inputs_fail_closed(field,value):
    from dataclasses import asdict
    data=asdict(m.Scenario())
    data[field]=value
    if field!="replacements":
        data["replacements"]=()
    with pytest.raises(m.MatchedStorageDCFError):
        m.Scenario(**data)


def test_repeated_source_year_cashflow_fades_not_increases():
    flat=m.Scenario(horizon_years=10,real_discount_rate=.08,
                    annual_saving_fade_fraction=0.)
    fading=replace(flat,annual_saving_fade_fraction=.02)
    assert m.discount_stream(1000.,fading)[
        "PV_repeated_modelled_wholesale_savings_year_eur"]<m.discount_stream(
        1000.,flat)["PV_repeated_modelled_wholesale_savings_year_eur"]


def test_grid_complete_and_independent_historical_year_currency_domains():
    x=m.build(m.load_admitted_source())
    scenarios=x["two_year_assumption_scenario_grid"]
    assert len(scenarios)==324
    assert sum(row["source_year"]==2022 for row in scenarios)==162
    assert sum(row["source_year"]==2024 for row in scenarios)==162
    assert all(row["real_installed_all_in_incremental_CAPEX_supplier_verified"] is None
               for row in scenarios)
    assert all(row["scenario_2022_and_2024_EUR_units_are_NOT_exchangeable"] is True
               for row in scenarios)
    assert x["manufacturer_supplier_verified_incremental_all_in_CAPEX_eur"] is None
    assert x["scientific_v1_0_economic_gate_passed"] is False
    assert x["BAFU_native_v11_incremental_inventory_and_LCIA_verified"] is False
    assert "vendor costs" in m.markdown(x).lower()
    assert "NOT" in m.markdown(x)


def test_pinned_published_source_rejects_even_a_harmless_price_drift(tmp_path):
    raw=m.SOURCE.read_bytes()
    d=json.loads(raw)
    d["source_year_results"][0]["source_year_wholesale_E_minus_EplusS_saving_eur"]+=1.
    p=tmp_path/"source_tampered.json"
    p.write_text(json.dumps(d),encoding="utf-8")
    with pytest.raises(m.MatchedStorageDCFError,match="Git blob"):
        m.load_admitted_source(p)


def test_2022_2024_hypothetical_cashflow_not_averaged_or_projected():
    x=m.build(m.load_admitted_source())
    assert x["no_source_years_averaged_or_future_expected_savings_implied"] is True
    assert x["projected_future_electricity_price_distribution_supplied"] is False
    assert set(x["explicit_replacement_sensitivity_at_20_years_real_8pct_250k_annual_OPEX"])=={
        "2022","2024"
    }
