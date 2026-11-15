"""Independent F3-D source-year LP lower-bound + KKT tests.

Synthetic tiny LPs only; no original 2022/2024 data, no raw provider files,
no actual 2022/2024 dual proof. The actual source-year tests need a private
local run, and may return a correct LP LOWER bound without full MILP closure.
"""
import copy
import math

import numpy as np
import pytest

from ptxlens import f3d_source_year_independent_cost_lp_dual as m
from ptxlens import f3d_external_year_counterfactual_independent_review as cf
from ptxlens.f3d_external_year_private_witness_replay import expected_params
from ptxlens.f3d_external_year_independent_review import ExternalYearReviewError


def inputs():
    params=expected_params(20000)
    duty={"capacity_semantics":"max_inventory",
          "scenario_capacity_kg":20000,
          "gas_heel_kg":400.,
          "compressor_electrical_kwh_per_kg_charged":1.}
    wind=np.asarray([60.,70.,50.,45.,65.])
    price=np.asarray([50.,30.,40.,60.,20.])
    target=np.asarray([1000.]*5)
    return wind,price,target,params,duty


def test_independent_LP_uses_original_8_state_model_and_three_hourly_equalities():
    prob=m.construct_lp(*inputs())
    assert prob["c"].shape==(5*8,)
    assert prob["A_eq"].shape==(16,40)  # 3 per hour and terminal equality
    assert prob["A_ub"].shape==(5*4+4*2,40)  # 4 hourly and 2 ramps per link
    assert prob["lower"].shape==(40,)
    assert prob["upper"].shape==(40,)
    assert np.count_nonzero(prob["c"])==5
    assert prob["lower"][2]==-50
    assert prob["upper"][2]==50
    assert prob["lower"][4]==400


def test_dual_sign_stationarity_complementarity_and_original_source_feasibility():
    prob=m.construct_lp(*inputs())
    evidence=m.solve_and_dual_audit(prob,time_limit=30)
    assert evidence["LP_optimally_solved"] is True
    assert evidence["HiGHS_LP_status"]==0
    assert evidence["independent_relaxed_LP_dual_KKT_passed"] is True
    assert evidence["source_cost_lower_bound_eur"] is not None
    assert evidence["LP_KKT_max_stationarity"]<1e-4
    assert abs(evidence["LP_primal_dual_difference_eur"])<.1
    assert evidence["original_source_MILP_optimality_confirmed"] is False


def test_infeasible_relaxation_not_promoted_to_MILP_cost_certificate():
    wind,price,target,params,duty=inputs()
    target[:]=4000. # source 125MW*21.086kg/MWh <=2636 kg/h
    p=m.construct_lp(wind,price,target,params,duty)
    result=m.solve_and_dual_audit(p,time_limit=30)
    assert result["LP_optimally_solved"] is False
    assert result["source_cost_lower_bound_eur"] is None
    assert result["original_source_MILP_optimality_confirmed"] is False


def test_tampered_source_params_and_capacity_semantics_rejected():
    inp=list(inputs())
    x=list(inp)
    x[3]=dict(x[3],rated_mw=250)
    with pytest.raises(ExternalYearReviewError):
        m.construct_lp(*x)
    x=list(inp)
    x[4]=dict(x[4],scenario_capacity_kg=40000)
    with pytest.raises(ExternalYearReviewError):
        m.construct_lp(*x)


def test_counterfactual_independent_transform_preserves_price_distribution_and_original_H2():
    p=[float(i) for i in range(240)]
    wind=[min(float(i),m.MODEL_FARM_POWER_CAP_MW) if hasattr(m,"MODEL_FARM_POWER_CAP_MW") else min(float(i),125.685) for i in range(240)]
    q,z=cf.transformed(p,wind,"price_roll_168h")
    assert q==p[-168:]+p[:-168]
    assert z==wind
    q,z=cf.transformed(p,wind,"price_spread_150pct")
    assert np.median(q)==np.median(p)
    q,z=cf.transformed(p,wind,"wind_power_090")
    assert q==p
    assert z==pytest.approx([.9*x for x in wind])
    q,z=cf.transformed(p,wind,"wind_power_110_capped")
    assert q==p
    assert max(z)==pytest.approx(125.685)


def test_counterfactual_private_pair_missing_original_market_source_is_rejected(tmp_path):
    with pytest.raises((FileNotFoundError,ExternalYearReviewError)):
        cf.independent_pair(
            2024,"max_inventory","price_roll_168h",
            tmp_path/"PtX_PRIVATE_RESEARCH",
            tmp_path/"missing_observed_F3D.json")


def test_no_unknown_year_mode_variant_release():
    with pytest.raises(ExternalYearReviewError):
        cf.independent_pair(2023,"max_inventory","price_roll_168h","no_private","no_public")
    with pytest.raises(ExternalYearReviewError):
        cf.independent_pair(2024,"other","price_roll_168h","no_private","no_public")
    with pytest.raises(ExternalYearReviewError):
        cf.independent_pair(2024,"max_inventory","unverified_future_market","no_private","no_public")
