"""L3-D independent hermetic DCF mathematics, source gates, money-year scope.

These tests use SYNTHETIC cases only. Real 2022/2024 PtXFlex source hash
is checked at runtime by the L3-D CLI, never replaced by these fixtures.
"""
import copy
import hashlib
import math
import pytest

from ptxlens import l3d_historical_source_dcf as m


def synthetic_year_blob():
    d={
        "schema_version":m.SCHEMA,
        "2023_CDS_to_ARCO_full_year_original_source_calibration_passed":True,
        "2023_CDS_to_ARCO_8760_hour_1W_source_reference_SHA256":m.ORIGINAL_WIND_SHA,
        "scientific_v1_0_release_allowed":False,
        "installed_plant_investment_DCF_certified":False,
        "manufacturer_storage_incremental_CAPEX_OPEX_verified":False,
        "native_BAFU_2026_whole_plant_LCIA_verified":False,
        "independent_solver_dual_certificates_recomputed":False,
        "real_industrial_site_H2_validation_completed":False,
        "source_original_hourly_arrays_released":False,
        "private_hourly_primal_witnesses_released":False,
        "independent_financial_metadata_four_case_review_passed":True,
        "independent_year_mode_full_hourly_primal_E_EplusS_and_EOS_replay_passed":True,
        "cases":[],
    }
    for year in (2022,2024):
        for mode in m.MODES:
            service=m.YEARS[year]*50000/24*.6
            d["cases"].append({
                "year":year,"storage_capacity_semantics":mode,
                "year_utc_hours":m.YEARS[year],
                "independent_full_hourly_E_and_EplusS_primal_replay_passed":True,
                "independent_full_hourly_type_I_20_to_200bar_EOS_replay_passed":True,
                "source_original_hash_and_calendar_gate_passed":True,
                "independent_solver_dual_certificates_recomputed":False,
                "source_year_price_f64_sha256":"a"*64,
                "source_year_wind_f64_sha256":"b"*64,
                "price_neutral_E_uniform_hydrogen_service":{
                    "fraction_of_nominal_50_tonnes_per_day":.6,
                    "modelled_delivered_h2_kg_per_year":service,
                    "solver_reported_relative_optimality_gap":1e-8,
                },
                "matched_service_annual_operational_savings_nominal_eur":100.,
                "solver_reported_savings_lower_eur":99.999,
                "solver_reported_savings_upper_eur":100.001,
                "savings_modelled_nominal_eur_per_kg_of_same_h2_service":100/service,
                "E":{"modelled_h2_delivered_kg":service,
                     "modelled_nominal_eur_wholesale_cost":200.,
                     "solver_reported_cost_dual_lower_bound_eur":199.999,
                     "solver_reported_relative_mip_gap":2e-7},
                "E_plus_S":{"modelled_h2_delivered_kg":service,
                     "modelled_nominal_eur_wholesale_cost":100.,
                     "solver_reported_cost_dual_lower_bound_eur":99.999,
                     "solver_reported_relative_mip_gap":2e-7},
            })
    return d


def test_all_four_synthetic_metadata_source_integrity_and_mode_separation():
    cases=m.check_four_cases(synthetic_year_blob())
    assert len(cases)==4
    assert cases[2024,"usable_service"]["year_utc_hours"]==8784
    assert len(m.build(cases,"0"*64)["analyst_324_case_deterministic_sensitivity_matrix"])==324


def test_duplicate_year_or_missing_leap_hour_rejected():
    d=synthetic_year_blob()
    d["cases"][3]["year_utc_hours"]=8760
    with pytest.raises(m.HistoricalSourceDCFError):
        m.check_four_cases(d)
    d=synthetic_year_blob()
    d["cases"][3]["storage_capacity_semantics"]="max_inventory"
    with pytest.raises(m.HistoricalSourceDCFError):
        m.check_four_cases(d)


def test_mismatched_original_price_hash_or_H2_product_refused():
    for key,value in [("source_year_price_f64_sha256","f"*64),
                      ("source_year_wind_f64_sha256","e"*64)]:
        d=synthetic_year_blob()
        d["cases"][1][key]=value
        with pytest.raises(m.HistoricalSourceDCFError):
            m.check_four_cases(d)
    d=synthetic_year_blob()
    d["cases"][2]["E_plus_S"]["modelled_h2_delivered_kg"]+=100
    with pytest.raises(m.HistoricalSourceDCFError):
        m.check_four_cases(d)


def test_invalid_optimality_gap_faked_independent_dual_and_v1_forbidden():
    d=synthetic_year_blob()
    d["cases"][0]["E"]["solver_reported_relative_mip_gap"]=1e-3
    with pytest.raises(m.HistoricalSourceDCFError):
        m.check_four_cases(d)
    for field in ("independent_solver_dual_certificates_recomputed",
                  "manufacturer_storage_incremental_CAPEX_OPEX_verified",
                  "native_BAFU_2026_whole_plant_LCIA_verified",
                  "scientific_v1_0_release_allowed"):
        d=synthetic_year_blob()
        d[field]=True
        with pytest.raises(m.HistoricalSourceDCFError):
            m.check_four_cases(d)


@pytest.mark.parametrize("r,N,expected",[
    (0.,20,2000.),
    (.08,20,100.*(1-(1.08)**-20)/.08),
    (.10,10,100.*(1-(1.10)**-10)/.10),
])
def test_independent_closed_form_annuity_and_capex_ceiling(r,N,expected):
    a=m.Scenario(years=N,discount_real=r)
    x=m.dcf(100.,a)
    assert x["zero_NPV_extra_all_in_CAPEX_ceiling_source_year_eur"]==pytest.approx(expected,abs=1e-8)
    assert x["hypothetical_incremental_NPV_source_year_eur"]==pytest.approx(expected,abs=1e-8)


def test_t0_capex_EOY_replacement_terminal_salvage_decommission_timing():
    a=m.Scenario(years=3,discount_real=.1,capex=80.,opex=5.,
                 replacement_year=2,replacement_cost=20.,
                 salvage=10.,decommission=4.)
    f=m.cashflows(100.,a)
    assert f==pytest.approx([-80.,95.,75.,101.])
    expected=-80+95/1.1+75/1.1**2+101/1.1**3
    x=m.dcf(100.,a)
    assert x["hypothetical_incremental_NPV_source_year_eur"]==pytest.approx(expected)
    assert x["zero_NPV_extra_all_in_CAPEX_ceiling_source_year_eur"]==pytest.approx(expected+80)


def test_cashflow_degradation_and_an_unprofitable_sensitivity():
    a=m.Scenario(years=3,discount_real=0,annual_degradation=.5,
                 repeat_factor=2.,opex=100.,capex=1000.)
    assert m.cashflows(100.,a)==pytest.approx([-1000.,100.,0.,-50.])
    r=m.dcf(100.,a)
    assert r["hypothetical_incremental_NPV_source_year_eur"]==-950.
    assert r["discounted_first_recovery_year_only_if_final_NPV_nonnegative"] is None


def test_zero_NPV_capex_and_opex_equivalence_and_negative_threshold():
    a=m.Scenario(years=5,discount_real=.05,opex=100.)
    result=m.dcf(40.,a)
    assert result["negative_capex_ceiling_means_no_nonnegative_CAPEX_feasible"] is True
    assert result["negative_opex_ceiling_means_no_nonnegative_OPEX_feasible"] is False
    b=m.Scenario(years=5,discount_real=.05,capex=100.)
    baseline=m.dcf(40.,b)
    opex_star=baseline["break_even_extra_annual_OPEX_at_selected_CAPEX_source_year_eur"]
    assert opex_star>0
    solved=m.dcf(40.,m.Scenario(years=5,discount_real=.05,
                                 capex=100.,opex=opex_star))
    assert solved["hypothetical_incremental_NPV_source_year_eur"]==pytest.approx(0,abs=1e-7)


def test_reported_cost_solver_interval_propagated_not_statistical_confidence():
    d=synthetic_year_blob()
    case=m.check_four_cases(d)[2024,"usable_service"]
    v=m.case_dcf(case,m.Scenario(years=20))
    lo,hi=v["solver_reported_bound_propagated_NPV_interval_eur"]
    point=v["modelled_central_economic_result"]["hypothetical_incremental_NPV_source_year_eur"]
    assert lo<=point<=hi
    assert not v["statistical_confidence_band"]
    assert not v["independent_HiGHS_cost_dual_proof"]
    assert not v["manufacturer_CAPEX_OPEX_verification"]


@pytest.mark.parametrize("bad",[
    dict(replacement_year=None,replacement_cost=10.),
    dict(replacement_year=0,replacement_cost=10.),
    dict(years=0),dict(discount_real=-.1),
    dict(discount_real=1.),dict(annual_degradation=1.2),
    dict(opex=-1.),dict(capex=-1.),
])
def test_invalid_hypothetical_assumptions_fail_closed(bad):
    with pytest.raises(m.HistoricalSourceDCFError):
        m.Scenario(**bad)


def test_github_blob_hash_checks_true_raw_content_and_CRLF_conversion(tmp_path):
    content=b'{"value": 1}\n'
    expected=hashlib.sha1(b"blob "+str(len(content)).encode()+b"\x00"+content).hexdigest()
    assert m.git_blob_hash(content)==expected
    assert m.git_blob_hash(content.replace(b"\n",b"\r\n"))==expected
    with pytest.raises(m.HistoricalSourceDCFError):
        m.git_blob_hash(b"bad\rraw")
    fake=tmp_path/"synthetic.json"
    fake.write_text('{"schema_version": "altered"}')
    with pytest.raises(m.HistoricalSourceDCFError,match="Git blob"):
        m.load_pinned_source(fake)


def test_report_and_four_case_matrix_have_explicit_NO_V1_release():
    cases=m.check_four_cases(synthetic_year_blob())
    result=m.build(cases,"0"*64)
    report=m.markdown_report(result)
    assert "324" in report
    assert "2022" in report and "2024" in report
    assert "NOT" in report or "not" in report
    assert result["scientific_v1_0_release_allowed"] is False
    assert result["no_manufacturer_CAPEX_quote"] is True
