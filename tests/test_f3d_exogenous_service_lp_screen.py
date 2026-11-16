"""F3-D preregistered fixed-exogenous-H2 original-year paired source LP screening.

These are synthetic non-provider tests, NOT evidence of real 2022/2024
plant feasibility, whole-year integer dispatch or financial saving.
"""
import numpy as np
import pytest

from ptxlens import f3d_exogenous_service_lp_screen as m
from ptxlens.f3d_external_year_private_witness_replay import expected_params
from ptxlens.f3d_external_year_independent_review import ExternalYearReviewError


def duty(capacity=20000,mode="max_inventory"):
    return {
        "scenario_capacity_kg":capacity,
        "capacity_semantics":mode,
        "gas_heel_kg":2000.,
        "compressor_electrical_kwh_per_kg_charged":1.,
    }


def test_original_source_year_hydrogen_day_targets_are_prespecified_not_E_optimum():
    assert m.DAY_TONNES==(25.,27.5,30.)
    assert m.WIND_POWER_FACTORS==(.9,.95,1.)
    for hours in (8760,8784):
        for day in m.DAY_TONNES:
            q=m.fixed_service(hours,day)
            assert len(q)==hours
            assert np.max(q)==np.min(q)==pytest.approx(1000*day/24)
            assert float(np.sum(q))==pytest.approx(day*1000*hours/24)
            assert q.dtype==np.float64
        assert np.array_equal(m.fixed_service(hours,30.),
                              m.fixed_service(hours,30.))


def test_original_E_boundary_selected_h2_rejected_as_exogenous_contract():
    original=np.full(8760,30480.6486532785/24.,dtype=float)
    for day in m.DAY_TONNES:
        fixed=m.check_reference_below_original_service(original,day,8760)
        assert fixed[0]<original[0]
    with pytest.raises(ExternalYearReviewError):
        m.check_reference_below_original_service(original,31.,8760)
    with pytest.raises(ExternalYearReviewError):
        m.check_reference_below_original_service(original,float(original[0]*24/1000),8760)
    wrong=np.array(original)
    wrong[-1]*=.99
    with pytest.raises(ExternalYearReviewError):
        m.check_reference_below_original_service(wrong,30.,8760)


@pytest.mark.parametrize("bad", [20.,24.999,30.4806486,31.,50.,float("nan")])
def test_wrong_H2_service_grid_not_accepted(bad):
    with pytest.raises(ExternalYearReviewError):
        m.fixed_service(8760,bad)


@pytest.mark.parametrize("bad", [8761,8783,1,0])
def test_nonregistered_original_UTC_source_year_hour_count_rejected(bad):
    with pytest.raises(ExternalYearReviewError):
        m.fixed_service(bad,30.)


def test_zero_objective_LP_feasible_has_no_binary_or_cost_certificate():
    model=expected_params(20000)
    w=np.full(48,80.,dtype=float)
    price=np.full(48,-20.,dtype=float)
    q=np.full(48,1000.,dtype=float)
    good=m.screen_case(w,price,q,model,duty(),.9,time_limit_s=30)
    assert good["source_E_or_EplusS_original_model_LP_status"]==(
        "SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED")
    assert good["HiGHS_LP_status_code"]==0
    assert good["original_integer_MILP_feasible"] is None
    assert good["source_matched_service_annual_cost_saving_eur"] is None
    assert good["source_equation_reconstructed_LP_primal_residuals_if_feasible"][
        "actual_integer_E_dispatch_feasible"] is False


def test_zero_objective_LP_infeasible_direct_deficit_and_no_cost_saving():
    model=expected_params(20000)
    w=np.zeros(100,dtype=float)
    price=np.full(100,100.,dtype=float)
    q=np.full(100,2000.,dtype=float)
    bad=m.screen_case(w,price,q,model,duty(),.9,time_limit_s=30)
    assert bad["source_E_or_EplusS_original_model_LP_status"]==(
        "SOURCE_LP_INFEASIBLE_ORIGINAL_INTEGER_MODEL_IMPOSSIBLE")
    assert bad["HiGHS_LP_status_code"]==2
    assert bad["necessary_energy_inventory_cut_proved_infeasible"] is True
    assert bad["original_integer_MILP_feasible"] is False
    assert bad["source_matched_service_annual_cost_saving_eur"] is None


def test_source_hardware_and_stress_factor_fail_closed():
    model=expected_params(20000)
    w=np.full(4,70.);price=np.zeros(4);q=np.full(4,1000.)
    for k in (.89,.901,.97,1.01):
        with pytest.raises(ExternalYearReviewError):
            m.screen_case(w,price,q,model,duty(),k,time_limit_s=30)
    for time in (0,7201,True,20.):
        with pytest.raises(ExternalYearReviewError):
            m.screen_case(w,price,q,model,duty(),.9,time_limit_s=time)
    with pytest.raises(ExternalYearReviewError):
        m.screen_case(np.full(4,-1.),price,q,model,duty(),.9,time_limit_s=30)
    with pytest.raises(ExternalYearReviewError):
        m.screen_case(w,price,q,model,duty(capacity=40000),.9,time_limit_s=30)


def test_public_summary_h2_equality_and_no_vendor_or_real_site_claims():
    # A static self-check of admissible publication keys and normalised target
    # data, not an original source-year LP model execution.
    code=m.markdown({
        "source_year":2022,"capacity_semantics":"max_inventory",
        "nine_service_factor_pairs_two_architectures_LP_cells":[{
            "exogenous_H2_tonnes_per_day":25.,
            "source_wind_power_multiplier":.9,
            "cases":{
                "E":{"source_E_or_EplusS_original_model_LP_status":
                     "SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED"},
                "E_plus_S":{"source_E_or_EplusS_original_model_LP_status":
                            "SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED"},
            },
        }],
    })
    assert "25" in code
    assert "NULL" in code
    assert "integer" in code
    assert "not" in code.lower()
