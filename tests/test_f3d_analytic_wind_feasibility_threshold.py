"""Scientific tests of analytical source-wind feasibility threshold only.

Synthetic original-physics hourly electricity availability and fixed hydrogen
profile. No private 2022 weather, no original-year MILP/LP reoptimization.
"""
import copy
from datetime import datetime,timezone,timedelta

import numpy as np
import pytest

from ptxlens import f3d_analytic_wind_feasibility_threshold as m
from ptxlens.f3d_external_year_private_witness_replay import (
    expected_params,f64_hash,
)
from ptxlens.f3d_external_year_independent_review import ExternalYearReviewError


def hardware():
    return expected_params(20000),{
        "scenario_capacity_kg":20000,
        "capacity_semantics":"max_inventory",
        "gas_heel_kg":2000.,
        "compressor_electrical_kwh_per_kg_charged":1.,
    }


def synthetic_source():
    # Original factor 1.0 makes PEM max power 50+21.5MW sufficient for
    # 1,490kg/h H2; 0.90 is insufficient over 1000 consecutive hours
    # even under the generous 18,000kg storage swing.
    power=np.full(1000,21.5,dtype=np.float64)
    hydrogen=np.full(1000,1490.,dtype=np.float64)
    model,duty=hardware()
    return power,hydrogen,model,duty


def test_analytic_lower_wind_factor_monotonicity_and_original_feasibility_bracket():
    args=synthetic_source()
    lo=m.scan_interval_factor(*args,factor=.9)
    hi=m.scan_interval_factor(*args,factor=1.)
    assert lo["simple_energy_interval_necessary_condition_violated"] is True
    assert hi["simple_energy_interval_necessary_condition_violated"] is False
    result=m.necessary_cut_threshold(*args,low=.9,high=1.,steps=30)
    low=result["lower_factor_at_which_energy_storage_inequality_still_PROVES_infeasible"]
    high=result["first_higher_factor_at_which_inequality_NO_LONGER_PROVES_infeasible"]
    assert .9<low<high<1.
    assert high-low<1e-9
    assert result["actual_E_MILP_feasibility_transition_factor_verified"] is None
    assert not result["independent_new_full_year_MILP_or_dual_solved"]
    assert m.scan_interval_factor(*args,factor=low)[
        "simple_energy_interval_necessary_condition_violated"] is True
    assert m.scan_interval_factor(*args,factor=high)[
        "simple_energy_interval_necessary_condition_violated"] is False


def test_no_violation_at_90pct_must_not_infer_new_wind_threshold():
    power,hydrogen,model,duty=synthetic_source()
    hydrogen=hydrogen*.5
    with pytest.raises(ExternalYearReviewError):
        m.necessary_cut_threshold(power,hydrogen,model,duty)


def test_100pct_wind_necessary_violation_rejected_as_inconsistent_with_original():
    power,hydrogen,model,duty=synthetic_source()
    hydrogen=np.full_like(hydrogen,2000.)
    with pytest.raises(ExternalYearReviewError):
        m.necessary_cut_threshold(power,hydrogen,model,duty)


def test_invalid_factor_or_steps_fail_closed():
    data=synthetic_source()
    for x in (-.01,1.01,float("nan")):
        with pytest.raises(ExternalYearReviewError):
            m.scan_interval_factor(*data,factor=x)
    for n in (0,49,2.5):
        with pytest.raises(ExternalYearReviewError):
            m.necessary_cut_threshold(*data,steps=n)


def test_original_independent_90pct_review_acceptance_and_source_SHA():
    wind,target,model,duty=synthetic_source()
    measured=m.scan_interval_factor(wind,target,model,duty,factor=.9)
    correct={
        "schema_version":m.INDEPENDENT_FEASIBILITY_SCHEMA,
        "year":2022,"capacity_semantics":"max_inventory",
        "original_4_case_public_Git_blob_sha1":m.SOURCE_PUBLISHED_GIT_BLOB,
        "independent_reconstruction_reports_E_LP_infeasible":True,
        "independent_EplusS_feasible_full_year_original_primal_replay_passed":True,
        "paired_E_minus_EplusS_cost_saving_eur":None,
        "original_source_model_E_infeasible_EplusS_feasible_under_fixed_hourly_H2":True,
        "real_site_physical_infeasibility_certified":False,
        "original_observed_wind_float64_SHA256":f64_hash(wind.tolist()),
        "same_frozen_hourly_hydrogen_service_float64_SHA256":f64_hash(target.tolist()),
        "counterfactual_wind_model_electric_power_float64_SHA256":
            f64_hash((wind*.9).tolist()),
        "analytical_energy_storage_interval":measured,
    }
    assert m.validate_original_review(2022,"max_inventory",correct,wind,target)==measured
    for change in [
        ("paired_E_minus_EplusS_cost_saving_eur",0.),
        ("independent_reconstruction_reports_E_LP_infeasible",False),
        ("original_observed_wind_float64_SHA256","tampered"),
        ("real_site_physical_infeasibility_certified",True),
    ]:
        altered=copy.deepcopy(correct)
        altered[change[0]]=change[1]
        with pytest.raises(ExternalYearReviewError):
            m.validate_original_review(2022,"max_inventory",altered,wind,target)


def test_exact_UTC_hour_index_to_timestamp_and_no_hourly_source_vectors():
    # Summarize requires 2022/2024 complete source calendars; use 8760
    # synthetic observations where 90% wind violates the necessary bound,
    # and at 100% the bound holds.
    wind=np.full(8760,21.5,dtype=float)
    h2=np.full(8760,1490.,dtype=float)
    model,duty=hardware()
    # For this test every hour is a deficit at .90, violation end=8760.
    observed=m.scan_interval_factor(wind,h2,model,duty,factor=.9)
    review={
        "schema_version":m.INDEPENDENT_FEASIBILITY_SCHEMA,
        "year":2022,"capacity_semantics":"max_inventory",
        "original_4_case_public_Git_blob_sha1":m.SOURCE_PUBLISHED_GIT_BLOB,
        "independent_reconstruction_reports_E_LP_infeasible":True,
        "independent_EplusS_feasible_full_year_original_primal_replay_passed":True,
        "paired_E_minus_EplusS_cost_saving_eur":None,
        "original_source_model_E_infeasible_EplusS_feasible_under_fixed_hourly_H2":True,
        "real_site_physical_infeasibility_certified":False,
        "original_observed_wind_float64_SHA256":f64_hash(wind.tolist()),
        "same_frozen_hourly_hydrogen_service_float64_SHA256":f64_hash(h2.tolist()),
        "counterfactual_wind_model_electric_power_float64_SHA256":
            f64_hash((wind*.9).tolist()),
        "analytical_energy_storage_interval":observed,
    }
    out=m.summarize(2022,"max_inventory",wind,h2,model,duty,review)
    assert out["90pct_proof_interval_hours"]==8760
    assert out["90pct_proof_interval_start_UTC_inclusive"]=="2022-01-01T00:00:00Z"
    assert out["90pct_proof_interval_end_UTC_exclusive"]=="2023-01-01T00:00:00Z"
    assert out["90pct_paired_wholesale_cost_saving_eur"] is None
    assert out["scientific_v1_0_release_allowed"] is False
    assert "E MILP" in m.markdown(out)
    assert "Hourly" not in str(out) or "source" in str(out)
