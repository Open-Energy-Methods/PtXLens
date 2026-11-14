"""L3-A DCF science tests: exact source F3-C 2023 cost, 2023-real EUR timing,
independent analytical annuity/DCF, 1e-6 MIP propagation, no vendor costs.

Hypothetical parameters are not source-based price forecasts or actual site.
"""
import dataclasses
import json
import math
from pathlib import Path

import pytest

import ptxlens.l3a_source_wholesale_dcf as m


def test_verified_source_requires_original_f3c_sha_and_2023_service_mode():
    manifest,cases=m.read_verified_inputs()
    assert manifest["schema_version"]==m.MANIFEST_SCHEMA
    assert manifest["source_research_release_full_v1_allowed"] is False
    assert set(cases)=={"max_inventory","usable_service"}
    for mode,ref in cases.items():
        assert ref["frozen_8760hour_H2_service_float64_sha256"]==m.SOURCE_H2_HASHES[mode]
        assert ref["source_2023_annual_equal_hour_modelled_H2_kg"]<18250000
        assert ref["original_full_2023_contract_unserved_H2_kg"]>1914720
        assert ref["existing_vendor_all_in_incremental_installed_capex_eur"] is None
        assert ref["actual_opex_replacement_disposal_schedules_eur"] is None
        assert ref["source_full_LCOH_or_2026_native_BAFU_GWP"] is None
        assert ref["reference_incremental_empty_vessel_equipment_mass_kg"]>1e6


def test_known_2023_wholesale_savings_and_source_mip_interval_not_physical_uncertainty():
    _,v=m.read_verified_inputs()
    gross=v["max_inventory"]
    usable=v["usable_service"]
    assert gross["source_2023_net_grid_wholesale_annual_saving_eur"]==pytest.approx(1124332.2692838833,abs=.01)
    assert usable["source_2023_net_grid_wholesale_annual_saving_eur"]==pytest.approx(1103463.7287309095,abs=.01)
    assert gross["source_2023_annual_equal_hour_modelled_H2_kg"]==pytest.approx(16268755.000838026,abs=.002)
    assert usable["source_2023_annual_equal_hour_modelled_H2_kg"]==pytest.approx(16331558.946374645,abs=.002)
    assert gross["source_2023_net_grid_wholesale_solver_saving_interval_eur"][0]>1124318-1
    assert usable["source_2023_net_grid_wholesale_solver_saving_interval_eur"][1]<1103475
    assert gross["frozen_8760hour_H2_service_float64_sha256"]!=usable["frozen_8760hour_H2_service_float64_sha256"]


@pytest.mark.parametrize("years,real_r,reference_annuity",[
    (1,0.,1.),
    (5,0.,5.),
    (20,0.,20.),
    (10,.1,(1-(1.1)**-10)/.1),
    (20,.08,(1-(1.08)**-20)/.08),
])
def test_independent_annuity_reference(years,real_r,reference_annuity):
    s=m.constant_scenario(100.,years=years,r=real_r)
    pv=m.pv_components(s)
    assert pv["sum_end_of_year_discount_factors_annuity"]==pytest.approx(reference_annuity,abs=1e-11)
    assert pv["max_initial_all_in_incremental_capex_at_zero_NPV_eur"]==pytest.approx(
        100.*reference_annuity,abs=1e-10)


def test_t0_initial_CAPEX_and_eoy_replacement_and_terminal_salvage_decommission():
    s=m.constant_scenario(100.,years=3,r=.10,annual_opex_eur=10.,
                          replacements=((2,40.),),terminal_salvage_eur=50.,
                          terminal_decommission_eur=12.)
    # Independent hand arithmetic: 90/1.1 + 50/(1.1^2) + 128/(1.1^3).
    expected=90./1.1+50./1.1**2+128./1.1**3
    result=m.pv_components(s)
    assert result["max_initial_all_in_incremental_capex_at_zero_NPV_eur"]==pytest.approx(expected,abs=1e-10)
    assert m.npv_at_assumed_installed_capex(s,expected)==pytest.approx(0,abs=1e-10)
    assert m.npv_at_assumed_installed_capex(s,expected+1)==pytest.approx(-1,abs=1e-10)
    assert result["cashflow_years"][1]["analyst_hypothetical_replacement_eur"]==40.
    assert result["cashflow_years"][2]["analyst_hypothetical_terminal_salvage_eur"]==50.
    assert result["cashflow_years"][2]["analyst_hypothetical_decommission_eur"]==12.


def test_one_year_unit_end_year_is_not_y0():
    s=m.constant_scenario(100.,years=1,r=.25,annual_opex_eur=20.)
    assert m.pv_components(s)["max_initial_all_in_incremental_capex_at_zero_NPV_eur"]==pytest.approx(64.,abs=1e-12)


def test_nonstationary_year_factors_annual_opex_still_discount_independently():
    s=m.CashflowScenario(3,.05,100.,(1.,2.,0.),(0.,40.,10.))
    expected=100/1.05+160/1.05**2-10/1.05**3
    assert m.pv_components(s)["max_initial_all_in_incremental_capex_at_zero_NPV_eur"]==pytest.approx(expected,abs=1e-9)
    assert m.pv_components(s)["cashflow_years"][2]["conditional_replayed_wholesale_saving_eur"]==0.


def test_uniform_opex_ceiling_at_any_capex_exactly_zero_NPV_even_with_nonzero_initial_OPEX():
    s=m.constant_scenario(100.,years=3,r=.10,annual_opex_eur=15.,
                          replacements=((2,20.),),terminal_salvage_eur=30.)
    capex=125.
    max_opex=m.break_even_uniform_annual_opex(s,capex)
    t=m.constant_scenario(100.,years=3,r=.10,annual_opex_eur=max_opex,
                          replacements=((2,20.),),terminal_salvage_eur=30.)
    assert m.npv_at_assumed_installed_capex(t,capex)==pytest.approx(0,abs=1e-10)
    assert m.break_even_uniform_annual_opex(s,0)>m.break_even_uniform_annual_opex(s,100)


def test_high_hypothetical_annual_cost_yields_negative_CAPEX_ceiling_not_false_benefit():
    s=m.constant_scenario(100.,years=10,r=.05,annual_opex_eur=200.)
    x=m.pv_components(s)
    assert x["max_initial_all_in_incremental_capex_at_zero_NPV_eur"]<0
    assert not x["nonnegative_initial_capex_feasible_if_all_scenario_cashflows_realised"]
    assert m.break_even_uniform_annual_opex(s,0)==pytest.approx(100.,abs=1e-9)
    assert m.npv_at_assumed_installed_capex(s,0)<0


def test_real_discount_and_nominal_cashflows_conversion_identical_IF_consistent():
    real=m.constant_scenario(100.,years=20,r=.08)
    nominal=math.expm1(math.log1p(.08)+math.log1p(.025))
    nominal_cashflows=tuple(100*(1.025)**year for year in range(1,21))
    direct_nominal=sum(y/(1+nominal)**i for i,y in enumerate(nominal_cashflows,start=1))
    assert direct_nominal==pytest.approx(m.pv_components(real)["max_initial_all_in_incremental_capex_at_zero_NPV_eur"],rel=1e-12)


def test_solver_bounds_propagate_analytically_and_only_solver_uncertainty():
    s=m.constant_scenario(100.,years=20,r=.08,repeat_factor=.5,annual_opex_eur=7.)
    lo,hi=m.source_bound_capex_interval(s,(99.,101.))
    ref=m.pv_components(s)["max_initial_all_in_incremental_capex_at_zero_NPV_eur"]
    df=.5*sum((1.08)**-t for t in range(1,21))
    assert hi-lo==pytest.approx((101-99)*df,abs=1e-8)
    assert lo<ref<hi
    with pytest.raises(m.InvalidIncrementalCashflow):
        m.source_bound_capex_interval(s,(101.,99.))
    with pytest.raises(m.InvalidIncrementalCashflow):
        m.source_bound_capex_interval(s,(99.,110.))


def test_scenario_outputs_use_an_optimistic_zero_opex_upper_envelope_NOT_vendor_cost():
    d=m.make_all()
    assert d["schema_version"]==m.SCHEMA
    assert d["scientific_L3_full_release_PASSED"] is False
    assert d["actual_installed_incremental_capex"] is None
    assert d["actual_incremental_lifetime_NPV"] is None
    assert d["complete_hydrogen_whole_plant_LCOH"] is None
    assert d["native_full_2026_BAFU_stationary_typeI_GWP"] is None
    assert d["2023_source_annual_electricity_difference_not_forecast_future_power_prices"]
    assert d["two_modes_different_hourly_H2_functional_units_not_a_single_cost_comparison"]
    for mode in m.MODES:
        x=d["per_distinct_capacity_semantics"][mode]
        theoretical=x["conditional_20yr_8pct_zero_extra_cost_theoretical_capex_ceiling"]
        hypothetical=x["conditional_20yr_8pct_cost_and_replacement_sensitivity"]
        assert len(x["discount_lifetime_zero_extra_COST_OPTIMISTIC_upper_envelope"])==30
        assert len(x["source_2023_wholesale_persistence_factor_and_opex_sensitivity"])==18
        assert len(x["annual_opex_vs_installed_capex_20yr_8pct_break_even_frontier"])==8
        assert len(theoretical["year_1_to_20_cashflow_ledger"])==20
        assert theoretical["conditional_capex_ceiling_eur"]>hypothetical["conditional_capex_ceiling_eur"]
        assert theoretical["conditional_capex_ceiling_solver_bound_eur"][0]<theoretical["conditional_capex_ceiling_eur"]<theoretical["conditional_capex_ceiling_solver_bound_eur"][1]
        assert theoretical["conditional_wholesale_difference_eur_per_kg_matched_hourly_H2"]>0
        assert theoretical["hardware_reference_ceiling_per_kg_is_NOT_market_steel_PRICE"]
        assert theoretical["conditional_assumed_installed_capex_eur"] is None
        assert hypothetical["conditional_assumed_installed_capex_eur"] is None
        assert x["source_actual_manufacturer_capex_and_opex"] is None
        assert x["gwp_LCOH_and_true_investment_NPV"] is None
        assert not x["complete_economic_release_allowed"]


@pytest.mark.parametrize("years,rate,factor,opex,repl",[
  (0,.08,1.,0.,()),
  (61,.08,1.,0.,()),
  (20,-.08,1.,0.,()),
  (20,1.,1.,0.,()),
  (20,.08,-1.,0.,()),
  (20,.08,float("nan"),0.,()),
  (20,.08,1.,-1.,()),
  (20,.08,1.,0.,((0,10.),)),
  (20,.08,1.,0.,((21,10.),)),
  (20,.08,1.,0.,((4,10.),(4,20.))),
])
def test_bad_time_money_discount_or_negative_unlicensed_price_assumptions_fail(
        years,rate,factor,opex,repl):
    with pytest.raises(m.InvalidIncrementalCashflow):
        m.constant_scenario(100.,years=years,r=rate,repeat_factor=factor,
                            annual_opex_eur=opex,replacements=repl)


@pytest.mark.parametrize("corruption",[
  ("f3c_sha256","0"*64),
  ("f2_typeI_bom_sha256","0"*64),
  ("source_research_release_full_v1_allowed",True),
  ("money_basis","unknown USD"),
  ("strict_modes",["max_inventory"]),
])
def test_unlicensed_or_modified_source_manifest_rejected(tmp_path,monkeypatch,corruption):
    key,value=corruption
    register=json.loads(m.MANIFEST.read_text())
    register[key]=value
    altered=tmp_path/"altered.json"
    altered.write_text(json.dumps(register))
    monkeypatch.setattr(m,"MANIFEST",altered)
    with pytest.raises(m.InvalidIncrementalCashflow):
        m.read_verified_inputs()


def test_cross_repo_handoff_frozen_primary_sources_reject_physically_unfunded_2023_steel_cost(
        tmp_path,monkeypatch):
    m0=json.loads(m.MANIFEST.read_text())
    m0["not_qualified_claims"]["actual_vendor_capex_known"]=True
    mfile=tmp_path/"bad_manifest.json"
    mfile.write_text(json.dumps(m0))
    monkeypatch.setattr(m,"MANIFEST",mfile)
    with pytest.raises(m.InvalidIncrementalCashflow,match="falsely claims"):
        m.read_verified_inputs()
