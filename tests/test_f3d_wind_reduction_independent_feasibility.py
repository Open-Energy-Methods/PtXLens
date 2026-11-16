"""F3-D independently reconstructed wind-power infeasibility diagnostic tests.

No private hourly source or original-year witness needed for these hermetic
physical-inequality and LP-matrix tests. A positive deficit *proves* violation
of a necessary physical inequality; no violation proves nothing.
"""
import numpy as np
import pytest

from ptxlens import f3d_wind_reduction_independent_feasibility as m
from ptxlens.f3d_source_year_independent_cost_lp_dual import construct_lp
from ptxlens.f3d_external_year_private_witness_replay import expected_params
from ptxlens.f3d_external_year_independent_review import ExternalYearReviewError


def duty(cap=20000,mode="max_inventory"):
    return {
        "scenario_capacity_kg":cap,
        "capacity_semantics":mode,
        "gas_heel_kg":2000.0,
        "compressor_electrical_kwh_per_kg_charged":1.0,
    }


def test_long_low_wind_window_violates_original_E_inventory_necessary_condition():
    p=expected_params(20000)
    # No wind, 50 MW max imported, 200 consecutive 1500kg/h H2 demands.
    # Even if all PEM electrical input can be used with no losses and
    # perfectly unconstrained storage dispatch, 18t of bank working
    # inventory cannot cover this deficit.
    w=np.zeros(200,dtype=float)
    q=np.full(200,1500.)
    a=m.necessary_interval_deficit(w,q,p,duty())
    assert a["simple_energy_interval_necessary_condition_violated"] is True
    assert a["max_interval_deficit_minus_available_inventory_kg"]>60000
    assert a["violating_interval_start_UTC_hour_index"]==0
    assert a["violating_interval_end_exclusive_UTC_hour_index"]==200
    assert a["physical_bank_inventory_swing_upper_limit_kg"]==18000


def test_high_wind_nonviolation_never_claims_feasibility():
    p=expected_params(20000)
    w=np.full(200,110.,dtype=float)
    q=np.full(200,1500.)
    a=m.necessary_interval_deficit(w,q,p,duty())
    assert a["simple_energy_interval_necessary_condition_violated"] is False
    assert a["violating_interval_start_UTC_hour_index"] is None
    assert a["violating_interval_end_exclusive_UTC_hour_index"] is None
    assert a["max_contiguous_net_H2_deficit_kg_under_generous_PEM_power_upper_bound"]==0


def test_vessel_semantics_change_working_inventory_only_not_wind_power():
    p=expected_params(20000)
    w=np.full(100,0.,dtype=float)
    q=np.full(100,1500.)
    a=m.necessary_interval_deficit(w,q,p,duty(mode="max_inventory"))
    b=m.necessary_interval_deficit(w,q,p,duty(mode="usable_service"))
    assert a["physical_bank_inventory_swing_upper_limit_kg"]==18000
    assert b["physical_bank_inventory_swing_upper_limit_kg"]==20000
    assert a["max_contiguous_net_H2_deficit_kg_under_generous_PEM_power_upper_bound"]==pytest.approx(
        b["max_contiguous_net_H2_deficit_kg_under_generous_PEM_power_upper_bound"])
    assert a["max_interval_deficit_minus_available_inventory_kg"]==pytest.approx(
        b["max_interval_deficit_minus_available_inventory_kg"]+2000)


def test_analytical_energy_cut_refuses_invalid_pressure_bank_and_negative_wind():
    p=expected_params(20000)
    with pytest.raises(ExternalYearReviewError):
        m.necessary_interval_deficit([0.,-1.],[1500.,1500.],p,duty())
    with pytest.raises(ExternalYearReviewError):
        m.necessary_interval_deficit([0.,0.],[1500.,1500.],p,duty(cap=40000))
    with pytest.raises(ExternalYearReviewError):
        m.necessary_interval_deficit([0.],[1500.],p,duty())


def build_exact_feasible_source_mip_witness(n=5):
    p=expected_params(20000)
    d=duty()
    w=np.full(n,60.,dtype=float)
    pr=np.full(n,30.,dtype=float)
    q=np.full(n,1000.,dtype=float)
    model=construct_lp(w,pr,q,p,d)
    x=np.zeros((n,8),dtype=float)
    y=p["h2_coefficient_kg_mwh"]
    comp=d["compressor_electrical_kwh_per_kg_charged"]/1000.
    # Source original no loss other than 1kg/h from initial 10t bank:
    # choose 1kg/h charge each hour so S = 10t and terminal = 10t.
    power=(1000.+1.)/y
    x[:,0]=power
    x[:,1]=1.
    x[:,2]=power+comp*1.-60.
    x[:,3]=0.
    x[:,4]=10000.
    x[:,5]=1.
    x[:,6]=0.
    x[:,7]=1.
    return model,x


def test_feasible_original_MILP_witness_satisfies_independently_rebuilt_LP():
    lp,states=build_exact_feasible_source_mip_witness()
    result=m.independent_reconstructed_constraint_feasibility(lp,states.ravel())
    assert result["source_MILP_witness_passes_independent_reconstructed_LP_feasibility"]
    assert result["maximum_independently_rebuilt_equality_residual"]<1e-8
    assert result["maximum_independently_rebuilt_inequality_violation"]<1e-8


def test_tampered_source_integer_witness_fails_independently_rebuilt_LP():
    lp,states=build_exact_feasible_source_mip_witness()
    states[2,5]+=100.
    with pytest.raises(ExternalYearReviewError):
        m.independent_reconstructed_constraint_feasibility(lp,states.ravel())


def test_fractional_commitment_not_promoted_from_relaxed_LP_to_MILP_witness():
    lp,states=build_exact_feasible_source_mip_witness()
    states[:,1]=0.5
    with pytest.raises(ExternalYearReviewError):
        m.independent_reconstructed_constraint_feasibility(lp,states.ravel())


def test_invalid_public_model_proof_not_asserted_from_synthetic_tests():
    assert m.VARIANT=="wind_power_090"
    assert m.SCHEMA.endswith("_LP_feasibility.v1")
    assert "PRIVATE" in m.__doc__


def test_numpy_float64_provenance_hash_matches_native_python_float_exactly():
    """Regression for independent wind reviewer traceback on numpy.float64."""
    from ptxlens.f3d_external_year_private_witness_replay import f64_hash
    v=[0.0, 12.345678901234567, 112.25, -8.5, 1.0e-12]
    native_sha=f64_hash(v)
    numeric=np.asarray(v,dtype=np.float64)
    assert m.source_f64_vector_hash(numeric)==native_sha
    assert m.source_f64_vector_hash(v)==native_sha
    assert m.source_f64_vector_hash(np.float64(0.9)*numeric)==f64_hash(
        (np.float64(0.9)*numeric).tolist())
    assert m.source_f64_vector_hash(numeric.reshape(-1))==native_sha
    assert m.source_f64_vector_hash(np.asarray(v,dtype="<f8"))==native_sha
    assert m.source_f64_vector_hash(numeric[::-1])!=native_sha


def test_source_hash_rejects_nonfinite_or_multidimensional_synthetic_arrays():
    for bad in (
        np.array([0.,float("nan")],dtype=np.float64),
        np.array([0.,float("inf")],dtype=np.float64),
        np.zeros((2,2),dtype=np.float64),
        np.zeros((0,),dtype=np.float64),
    ):
        with pytest.raises(ExternalYearReviewError):
            m.source_f64_vector_hash(bad)


def test_numpy_flattened_eight_column_witness_hash_remains_original():
    from ptxlens.f3d_external_year_private_witness_replay import f64_hash
    original=np.arange(24,dtype=np.float64).reshape(3,8)/17.
    expected=f64_hash(original.ravel().tolist())
    assert m.source_f64_vector_hash(original.ravel())==expected
    # Hourly permutation must change witness provenance hash.
    assert m.source_f64_vector_hash(original[::-1].ravel())!=expected
