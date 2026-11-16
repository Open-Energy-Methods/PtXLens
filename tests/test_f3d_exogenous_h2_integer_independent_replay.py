"""F3-D independent exogenous service original MILP paired review acceptance.

These are synthetic proof-contract regression tests only, NOT a real original
2022 8,760h private-provider annual solver run.
"""
import copy
import json

import numpy as np
import pytest

from ptxlens import f3d_exogenous_h2_integer_independent_replay as m
from ptxlens.f3d_exogenous_service_lp_screen import (
    SCHEMA as SCREEN_SCHEMA,DAY_TONNES,WIND_POWER_FACTORS
)
from ptxlens.f3d_wind_reduction_independent_feasibility import source_f64_vector_hash
from ptxlens.f3d_external_year_independent_review import ExternalYearReviewError


def synthetic_screen():
    hours=8760
    price=[10.]*hours
    wind=[70.]*hours
    selected=[1270.]*hours
    fixed=np.full(hours,1250.,dtype=float)
    sha=lambda values:source_f64_vector_hash(values)
    rows=[]
    for service in DAY_TONNES:
        for factor in WIND_POWER_FACTORS:
            target=np.full(hours,service*1000./24,dtype=float)
            rows.append({
                "exogenous_H2_tonnes_per_day":service,
                "source_wind_power_multiplier":factor,
                "exogenous_H2_original_same_hourly_SHA256":sha(target),
                "exogenous_same_product_annual_H2_kg":float(np.sum(target)),
                "matched_source_annual_E_minus_EplusS_cost_saving_eur":None,
                "E_and_ES_original_integer_dispatch_both_certified":False,
                "cases":{name:{
                    "HiGHS_LP_status_code":0,
                    "source_E_or_EplusS_original_model_LP_status":
                        "SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED",
                    "source_stress_wind_electric_power_multiplier":factor,
                    "original_integer_MILP_feasible":None,
                    "source_matched_service_annual_cost_saving_eur":None,
                } for name in m.CASES},
            })
    data={
        "schema_version":SCREEN_SCHEMA,
        "source_year":2022,"capacity_semantics":"max_inventory",
        "source_original_4_case_public_Git_blob_sha1":m.ORIGINAL_REFERENCE_SOURCE_GIT_BLOB,
        "source_calendar_UTC_hours":hours,
        "source_original_price_float64_SHA256":sha(price),
        "source_original_wind_power_float64_SHA256":sha(wind),
        "source_original_E_max_selected_hourly_H2_float64_SHA256":sha(selected),
        "source_price_year_input_unchanged":True,
        "same_H2_target_hourly_for_E_and_ES_at_every_wind_factor":True,
        "exogenous_delivery_schedules_selected_without_looking_at_stressed_wind_outcomes":True,
        "original_integer_dispatch_or_matched_wholesale_savings_certified":False,
        "real_site_or_manufacturer_or_native_BAFU_or_scientific_v1_0":False,
        "prespecified_exogenous_delivery_tonnes_day":list(DAY_TONNES),
        "source_wind_electric_power_multipliers":list(WIND_POWER_FACTORS),
        "nine_service_factor_pairs_two_architectures_LP_cells":rows,
    }
    return data,price,wind,selected,fixed


def test_exogenous_screen_accepts_locked_same_hourly_30t_90pct_pair_only():
    data,p,w,s,t=synthetic_screen()
    assert m.check_screen(data,2022,"max_inventory",None,p,w,s,t) is None
    assert m.H2_TPD==30.
    assert m.WIND_FACTOR==.9


@pytest.mark.parametrize("mutate",[
    lambda j:j.update(source_original_4_case_public_Git_blob_sha1="fake"),
    lambda j:j.update(source_original_price_float64_SHA256="fake"),
    lambda j:j.update(same_H2_target_hourly_for_E_and_ES_at_every_wind_factor=False),
    lambda j:j.update(original_integer_dispatch_or_matched_wholesale_savings_certified=True),
    lambda j:j["nine_service_factor_pairs_two_architectures_LP_cells"][6]["cases"]["E"].update(
        HiGHS_LP_status_code=2),
    lambda j:j["nine_service_factor_pairs_two_architectures_LP_cells"][6].update(
        exogenous_H2_original_same_hourly_SHA256="fake"),
    lambda j:j["nine_service_factor_pairs_two_architectures_LP_cells"][6].update(
        matched_source_annual_E_minus_EplusS_cost_saving_eur=100.),
])
def test_external_screen_fingerprint_and_false_integer_or_cost_claim_rejected(mutate):
    data,p,w,s,t=synthetic_screen()
    mutate(data)
    with pytest.raises(ExternalYearReviewError):
        m.check_screen(data,2022,"max_inventory",None,p,w,s,t)


def test_unreviewed_private_E_witness_never_accepted_as_independent_physical_result():
    # A source result that lacks full hourly witness must be rejected, no
    # automatic fallback to cost-only source summary.
    metadata={"exogenous_H2_hourly_SHA256":"fake"}
    with pytest.raises(ExternalYearReviewError):
        m.check_private_case({},metadata,"E",[70.,70.],[20.,20.],
                             [1250.,1250.],{},{})


def test_original_source_unavailable_does_not_fabricate_paired_savings(tmp_path):
    with pytest.raises((FileNotFoundError,ExternalYearReviewError)):
        m.independent_review(2022,"max_inventory",
                             tmp_path/"PtX_PRIVATE_RESEARCH",
                             tmp_path/"nonexistent_original.json",
                             tmp_path/"screen.json")


def test_real_annual_H2_target_remains_not_50t_per_day():
    t=m.fixed_service(8760,30.)
    assert float(t[0])==1250.
    assert float(np.sum(t))==10_950_000
    assert float(t[0])<50000./24
    assert m.SCHEMA.endswith("independently_replayed.v1")
    assert "PRIVATE" in m.__doc__


def test_private_witness_replay_accepts_numpy_float64_exogenous_target_and_preserves_sha(monkeypatch):
    """Regression reproduces the original crash INSIDE check_private_case.

    Synthetic physically consistent 2h E primal. Mock only the independent
    real-gas EOS which is separately tested on the actual private 2022 data;
    do not certify a synthetic pressure vessel as source-verified hardware.
    """
    from ptxlens.f3d_external_year_private_witness_replay import (
        expected_params, replay_equations
    )
    p=expected_params(20000)
    duty={
        "capacity_semantics":"max_inventory",
        "gas_heel_kg":2000.,
        "compressor_electrical_kwh_per_kg_charged":1.,
    }
    target=np.asarray([1250.,1250.],dtype=np.float64)
    original_wind=[70.,70.]
    price=[20.,20.]
    power=(1250.+1.)/p["h2_coefficient_kg_mwh"]
    grid=power+.001-70.*.9
    states=[[power,1.,grid,0.,10000.,1.,0.,1.] for _ in range(2)]
    source_SHA=source_f64_vector_hash(np.asarray(states,dtype=np.float64).reshape(-1))
    meta={
        "exogenous_H2_hourly_SHA256":source_f64_vector_hash(target),
        "source_original_price_SHA256":source_f64_vector_hash(price),
        "source_stressed_wind_SHA256":
            source_f64_vector_hash(np.asarray(original_wind,dtype=float)*m.WIND_FACTOR),
    }
    # This replay uses only genuine original-physics arithmetic and native
    # Python numeric vectors; it is *not* a mocked hourly equation.
    check=replay_equations(
        states,target.tolist(),
        [x*m.WIND_FACTOR for x in original_wind],price,p,duty)
    assert check["hourly_service_sha256"]==meta["exogenous_H2_hourly_SHA256"]
    assert check["hourly_states_sha256"]==source_SHA
    assert max(check["maxima"].values())<2e-4
    # EOS is separately checked in live source experiments with CoolProp.
    monkeypatch.setattr(m,"verify_eos",lambda *args,**kwargs:{
        "independent_313K_CoolProp_Hydrogen_EOS_recomputed":True,
        "min_bar_absolute":90.,"max_bar_absolute":90.,
    })
    record={
        "schema_version":m.PRODUCER_SCHEMA,
        "metadata":meta,"scenario":"E",
        "outcome":"SOURCE_MILP_SOLVER_REPORTED_COST_BOUND_NOT_INDEPENDENTLY_REPLAYED",
        "hourly_witness_private_not_for_git":True,
        "original_provider_price_wind_arrays_not_duplicated":True,
        "independent_full_year_hourly_physical_replay_complete":False,
        "independent_original_cost_dual_proof_complete":False,
        "matched_service_E_minus_ES_cost_saving_eur":None,
        "real_site_or_manufacturer_or_BAFU_v1_certified":False,
        "original_full_hourly_states_8var_PRIVATE":states,
        "original_full_hourly_states_SHA256":source_SHA,
        "source_solver_cost_eur":check["independent_source_year_signed_grid_cost_eur"],
        "source_solver_reported_cost_lower_bound_eur":
            check["independent_source_year_signed_grid_cost_eur"],
        "source_solver_reported_relative_MIP_gap":0.,
        "source_solver_reported_annual_h2_kg":float(np.sum(target)),
        "original_source_solver_audit":{
            "source_hourly_dispatch_float64_sha256":source_SHA
        },
    }
    result=m.check_private_case(record,meta,"E",original_wind,price,target,p,duty)
    assert result["status"]==(
        "INDEPENDENT_ORIGINAL_FULL_YEAR_INTEGER_PRIMAL_H2_ELECTRIC_EOS_REPLAY_PASSED")
    assert result["independent_hourly_primal_SHA256"]==source_SHA
    assert result["source_modelled_nominal_original_year_wholesale_eur"]==pytest.approx(
        check["independent_source_year_signed_grid_cost_eur"])
    assert result["independent_source_max_physical_residual"]<2e-4


def test_private_witness_replay_rejects_numpy_target_source_sha_tamper(monkeypatch):
    """A type-fix may not relax the existing H2 source provenance gate."""
    from ptxlens.f3d_external_year_private_witness_replay import expected_params
    monkeypatch.setattr(m,"replay_equations",lambda *a,**k:
                        (_ for _ in ()).throw(AssertionError("unsafe replay")))
    target=np.asarray([1250.,1250.],dtype=np.float64)
    meta={"exogenous_H2_hourly_SHA256":"tampered"}
    record={
        "schema_version":m.PRODUCER_SCHEMA,"metadata":meta,
        "scenario":"E",
        "outcome":"SOURCE_MILP_SOLVER_REPORTED_COST_BOUND_NOT_INDEPENDENTLY_REPLAYED",
        "hourly_witness_private_not_for_git":True,
        "original_provider_price_wind_arrays_not_duplicated":True,
        "independent_full_year_hourly_physical_replay_complete":False,
        "independent_original_cost_dual_proof_complete":False,
        "matched_service_E_minus_ES_cost_saving_eur":None,
        "real_site_or_manufacturer_or_BAFU_v1_certified":False,
        "original_full_hourly_states_8var_PRIVATE":[[0.]*8,[0.]*8],
    }
    with pytest.raises(ExternalYearReviewError,match="target"):
        m.check_private_case(record,meta,"E",[70.,70.],[20.,20.],
                             target,expected_params(20000),{})
