"""Hermetic independently verifiable original LP/controlled-pair summary.

Uses small synthetic source-data fingerprints and costs; no private hourly
originals and no real-world source-year optimality result is asserted here.
"""
import copy
import pytest
from ptxlens import f3d_lp_cf_public_consolidation as m

P="a"*64;W="b"*64;T="c"*64

def fixture():
    original={
        "schema_version":"oem.ptx.f3d_2022_2024_public_source_aggregate_independent_replay.v1",
        "independent_year_mode_full_hourly_primal_E_EplusS_and_EOS_replay_passed":True,
        "independent_solver_dual_certificates_recomputed":False,
        "scientific_v1_0_release_allowed":False,
        "cases":[{"year":2022,"storage_capacity_semantics":"max_inventory",
             "source_year_price_f64_sha256":P,"source_year_wind_f64_sha256":W,
             "price_neutral_E_uniform_hydrogen_service":{
                "hourly_target_f64_sha256":T,"modelled_delivered_h2_kg_per_year":100000.},
             "matched_service_annual_operational_savings_nominal_eur":100.,
             "E":{"modelled_nominal_eur_wholesale_cost":300.},
             "E_plus_S":{"modelled_nominal_eur_wholesale_cost":200.}},
             {"year":2022,"storage_capacity_semantics":"usable_service"},
             {"year":2024,"storage_capacity_semantics":"max_inventory"},
             {"year":2024,"storage_capacity_semantics":"usable_service"}],
    }
    lp={
        "schema_version":m.LP_SCHEMA,"source_year":2022,"mode":"max_inventory",
        "source_hours":8760,"original_source_public_Git_blob":m.PIN,
        "original_source_price_f64_sha256":P,"original_source_wind_f64_sha256":W,
        "original_hourly_hydrogen_service_f64_sha256":T,
        "original_HiGHS_branch_and_bound_dual_reconstructed":False,
        "E_and_EplusS_independent_LP_relaxed_global_cost_lower_bound_cases":{},
    }
    for case,primal,lower in (("E",300.,295.),("E_plus_S",200.,190.)):
        lp["E_and_EplusS_independent_LP_relaxed_global_cost_lower_bound_cases"][case]={
            "LP_optimally_solved":True,
            "independent_relaxed_LP_dual_KKT_passed":True,
            "source_cost_lower_bound_eur":lower,
            "original_source_integer_primal_cost_eur":primal,
            "LP_to_original_integer_primal_relative_cost_gap":(primal-lower)/primal,
        }
    cf={
        "schema_version":m.CF_SCHEMA,"year":2022,"mode":"max_inventory",
        "source_calendar_hours":8760,"variant":"price_roll_168h",
        "reference_original_public_four_case_Git_blob_sha1":m.PIN,
        "original_provider_price_f64_SHA256":P,
        "original_provider_wind_f64_SHA256":W,
        "fixed_original_price_blind_E_hydrogen_service_f64_SHA256":T,
        "fixed_hydrogen_same_hour_kg_year":100000.,
        "independent_cost_dual_or_LP_infeasibility_proof_completed":False,
        "measured_site_or_manufacturer_or_BAFU_or_v1_0_validated":False,
        "physical_original_full_year_primal_replay_passed_for_both":True,
        "economic_result_null_if_any_unverified_or_infeasible":False,
        "paired_E_minus_EplusS_nominal_operational_saving_eur":60.,
        "paired_source_solver_reported_bound_interval_eur":[59.999,60.001],
        "cases":{
            "E":{"status":"INDEPENDENT_FULL_YEAR_PRIMAL_AND_PRESSURE_COST_REPLAY_PASSED",
                  "source_model_cost_eur":240.},
            "E_plus_S":{"status":"INDEPENDENT_FULL_YEAR_PRIMAL_AND_PRESSURE_COST_REPLAY_PASSED",
                        "source_model_cost_eur":180.},
        },
    }
    return original,lp,cf


def test_independent_lp_yields_wide_but_positive_source_saving_certificate():
    original,lp,cf=fixture()
    answer=m.review(original,lp,cf)
    assert answer["independent_original_LP_global_savings_interval_eur"]==pytest.approx([95.,110.])
    assert answer["independent_original_LP_proves_positive_saving"] is True
    assert answer["controlled_pair_modelled_savings_eur"]==pytest.approx(60.)
    assert answer["controlled_savings_change_from_original_eur"]==pytest.approx(-40.)
    assert answer["controlled_savings_change_from_original_percent"]==-40.
    assert answer["controlled_pair_modelled_savings_eur_per_kg_H2"]==pytest.approx(0.0006)
    assert answer["source_original_INTEGER_branch_and_bound_independently_certified"] is False
    assert "confidence" in m.prose(answer)


def test_intervention_must_preserve_exact_original_source_hourly_H2_SHA():
    orig,lp,cf=fixture()
    cf["fixed_original_price_blind_E_hydrogen_service_f64_SHA256"]="different"
    with pytest.raises(m.ReviewError,match="H2"):
        m.review(orig,lp,cf)


def test_corrupt_relaxed_LP_lower_bound_and_faked_KKT_rejected():
    orig,lp,cf=fixture()
    lp["E_and_EplusS_independent_LP_relaxed_global_cost_lower_bound_cases"]["E"]["source_cost_lower_bound_eur"]=301
    with pytest.raises(m.ReviewError):
        m.review(orig,lp,cf)
    orig,lp,cf=fixture()
    lp["E_and_EplusS_independent_LP_relaxed_global_cost_lower_bound_cases"]["E"]["independent_relaxed_LP_dual_KKT_passed"]=False
    with pytest.raises(m.ReviewError,match="KKT"):
        m.review(orig,lp,cf)


def test_opaque_unverified_LP_or_any_bogus_native_v1_flag_forbidden():
    original,lp,cf=fixture()
    cf["measured_site_or_manufacturer_or_BAFU_or_v1_0_validated"]=True
    with pytest.raises(m.ReviewError):
        m.review(original,lp,cf)
    original,lp,cf=fixture()
    original["scientific_v1_0_release_allowed"]=True
    with pytest.raises(m.ReviewError):
        m.review(original,lp,cf)


def test_price_shift_partial_or_infeasible_modelled_h2_has_NULL_saving():
    original,lp,cf=fixture()
    cf["physical_original_full_year_primal_replay_passed_for_both"]=False
    cf["economic_result_null_if_any_unverified_or_infeasible"]=True
    cf["paired_E_minus_EplusS_nominal_operational_saving_eur"]=None
    cf["paired_source_solver_reported_bound_interval_eur"]=None
    cf["cases"]["E"]["status"]="SOURCE_SOLVER_REPORTED_LP_INFEASIBLE_NO_COST"
    result=m.review(original,lp,cf)
    assert result["controlled_pair_modelled_savings_eur"] is None
    assert result["controlled_savings_change_from_original_percent"] is None
    assert "NULL" in m.prose(result)
