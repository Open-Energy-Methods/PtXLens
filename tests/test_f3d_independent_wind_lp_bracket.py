"""F3-D controlled observed-year wind-factor E relaxed-LP bracket tests.

All sources synthetic and small. Exact original 2022 private provider arrays and
full-year LP solves are required separately on the user's Windows environment.
"""
import copy

import numpy as np
import pytest
from scipy.sparse import csr_matrix

from ptxlens import f3d_independent_wind_lp_bracket as m
from ptxlens.f3d_external_year_private_witness_replay import expected_params
from ptxlens.f3d_external_year_independent_review import ExternalYearReviewError


def toy():
    model=expected_params(20000)
    duty={
        "scenario_capacity_kg":20000,
        "capacity_semantics":"max_inventory",
        "gas_heel_kg":2000.,
        "compressor_electrical_kwh_per_kg_charged":1.,
    }
    return model,duty


def test_analytical_cut_lower_bracket_does_not_promote_to_integer_feasibility():
    """Simulated monotone LP feasibility classifier, no real source solver."""
    boundary=.992
    def check(factor):
        return {"factor":factor,
                "status":("SOURCE_MODEL_LP_INFEASIBLE_NO_FARKAS_RAY"
                          if factor<boundary else "LP_PRIMAL_FEASIBLE_NOT_INTEGER")}
    r=m.bisect_lp_with_explicit_statuses(.982860278,1.,check,steps=10)
    lower=r["largest_tested_independent_rebuilt_E_LP_infeasible_factor"]
    upper=r["smallest_tested_independent_rebuilt_E_LP_feasible_factor"]
    assert lower<boundary<=upper
    assert lower>=.982860278
    assert upper-lower<.00002
    assert r["actual_integer_E_feasible_factor_only_proven_at_1"]==1.
    assert r["LP_feasible_does_not_prove_original_integer_MILP_feasible"] is True
    assert r["independent_Farkas_ray_produced"] is False
    assert len(r["evaluated_factors_and_scalar_residuals_only"])==10
    assert all("hourly" not in x for x in r["evaluated_factors_and_scalar_residuals_only"])


def test_unknown_solver_status_cannot_be_treated_as_infeasible_or_feasible():
    for status in ("TIME_LIMIT", "NUMERICAL", "", None, "LP_PRIMAL_FEASIBLE"):
        with pytest.raises(ExternalYearReviewError):
            m.bisect_lp_with_explicit_statuses(
                .99,1.,lambda x:{"factor":x,"status":status},steps=1)
    with pytest.raises(ExternalYearReviewError):
        m.bisect_lp_with_explicit_statuses(
            .99,1.,lambda x:{"factor":x+.01,"status":"LP_PRIMAL_FEASIBLE_NOT_INTEGER"},
            steps=1)


@pytest.mark.parametrize("n", [0,13,-1,1.5,True])
def test_excessive_or_invalid_source_LP_count_rejected(n):
    with pytest.raises(ExternalYearReviewError):
        m.bisect_lp_with_explicit_statuses(
            .9829,1.,lambda x:{"factor":x,"status":"LP_PRIMAL_FEASIBLE_NOT_INTEGER"},
            steps=n)


def problem_fixture():
    return {
        "c":np.array([0.]),
        "A_eq":csr_matrix([[1.]]),"b_eq":np.array([.5]),
        "A_ub":csr_matrix([[1.]]),"b_ub":np.array([.8]),
        "lower":np.array([0.]),"upper":np.array([1.]),
    }


def test_independent_primal_feasibility_checks_all_three_types_of_constraints():
    p=problem_fixture()
    r=m.independently_validate_feasible_lp_witness(p,np.array([.5]))
    assert r["maximum_LP_primal_equality_residual"]==0.
    assert r["maximum_LP_primal_inequality_violation"]==0.
    assert r["maximum_LP_variable_bound_violation"]==0.
    assert r["actual_integer_E_dispatch_feasible"] is False
    for x in ([-.1],[.6],[1.1],[float("nan")],[.5,.6]):
        with pytest.raises(ExternalYearReviewError):
            m.independently_validate_feasible_lp_witness(p,np.asarray(x))


def test_small_independent_original_model_LP_feasible_and_infeasible_status():
    model,duty=toy()
    wind=np.full(50,60.,dtype=float)
    price=np.zeros(50,dtype=float)
    target=np.full(50,1000.,dtype=float)
    good=m.independent_relaxed_lp_feasible_at_factor(
        wind,price,target,model,duty,.95,time_limit_s=30)
    assert good["status"]=="LP_PRIMAL_FEASIBLE_NOT_INTEGER"
    assert good["HiGHS_status"]==0
    assert good["actual_integer_E_dispatch_feasible"] is False
    # Higher (but source delivery-limit-admissible) fixed service under no
    # wind cannot be supported by 50 MW grid and finite storage for 50h.
    wind=np.zeros(50)
    target[:]=2400.
    bad=m.independent_relaxed_lp_feasible_at_factor(
        wind,price,target,model,duty,.95,time_limit_s=30)
    assert bad["status"]=="SOURCE_MODEL_LP_INFEASIBLE_NO_FARKAS_RAY"
    assert bad["HiGHS_status"]==2
    assert bad["independent_LP_infeasibility_Farkas_dual_ray_computed"] is False


def test_malformed_input_factors_and_LP_limits_rejected():
    model,duty=toy()
    wind=np.full(3,50.);price=np.zeros(3);target=np.full(3,1000.)
    for factor in (-1.,.89,1.01):
        with pytest.raises(ExternalYearReviewError):
            m.independent_relaxed_lp_feasible_at_factor(
                wind,price,target,model,duty,factor,time_limit_s=30)
    for time in (0,7201,1.0,True):
        with pytest.raises(ExternalYearReviewError):
            m.independent_relaxed_lp_feasible_at_factor(
                wind,price,target,model,duty,.95,time_limit_s=time)


def test_complete_evidence_chain_rejects_changed_original_wind_SHA_and_unaudited_Wind_LP():
    original={
        "price_neutral_E_uniform_hydrogen_service":{
            "hourly_target_f64_sha256":"h"*64
        },"source_year_price_f64_sha256":"p"*64,
        "source_year_wind_f64_sha256":"w"*64
    }
    with pytest.raises(ExternalYearReviewError):
        m.validate_record_chain(
            2022,"max_inventory",
            [12.,13.],[1200.,1200.],original,{},{},{},b"no_private")
