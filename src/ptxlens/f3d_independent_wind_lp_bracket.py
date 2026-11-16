"""F3-D observed-year E-only source-model *RELAXED LP* wind feasibility bracket.

Previous evidence establishes:
  * k=0.9 original source E LP-infeasible independently AND a solver-free
    maximum contiguous H2 deficit/storable-inventory necessary contradiction.
  * the analytical necessary condition stops rejecting at k≈0.98286
    (this is NOT a feasible primal).
  * k=1.0 original E integer-feasible and independently physically replayed;
    a separate full-year reconstructed cost LP has a valid KKT/primal optimum.

This tool independently reconstructs the EXACT E LP feasibility equations
at 8 additional wind-electric-POWER factors. HiGHS status 2 is a source-model
LP infeasibility observation (no Farkas ray). HiGHS status 0 is accepted as
feasible ONLY after explicit independent sparse equality/inequality/variable
bound residual tests. Every infeasible LP factor lower-bounds the original
integer feasibility transition. A feasible LP upper factor does NOT prove
the integer original-source E model feasible. Only k=1 integer feasible
remains confirmed. Results are scalar-only; source hourly provider arrays,
LP incumbent and private original full-year witnesses are never exported.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from .f3d_source_year_independent_cost_lp_dual import (
    construct_lp, check_private_source, SCHEMA as COST_LP_SCHEMA,
    SOURCE_PUBLISHED_GIT_BLOB
)
from .f3d_wind_reduction_independent_feasibility import (
    source_f64_vector_hash,
    SCHEMA as WIND_INDEPENDENT_SCHEMA,
)
from .f3d_analytic_wind_feasibility_threshold import (
    scan_interval_factor, SCHEMA as ANALYTIC_SCHEMA
)
from .f3d_external_year_private_witness_replay import expected_params,need

SCHEMA="ptxlens.f3d_original_source_E_relaxed_LP_feasibility_wind_multiplier_bracket.v1"


def float_number(value,name):
    need(type(value) in (int,float) and math.isfinite(value),
         "invalid scalar source input: "+name)
    return float(value)


def validate_record_chain(year,mode,wind,target,source,independent,analytic,original_lp,
                          independent_bytes):
    """Check all prior source-registered scientific gates before expensive LPs."""
    need(year in (2022,2024) and mode in ("max_inventory","usable_service"),
         "wrong source-year/pressure capacity semantics")
    need(independent.get("schema_version")==WIND_INDEPENDENT_SCHEMA and
         analytic.get("schema_version")==ANALYTIC_SCHEMA and
         original_lp.get("schema_version")==COST_LP_SCHEMA,
         "wrong original independently verified evidence schema")
    need(independent.get("original_4_case_public_Git_blob_sha1")==SOURCE_PUBLISHED_GIT_BLOB and
         analytic.get("source_four_case_original_Git_blob_sha1")==SOURCE_PUBLISHED_GIT_BLOB and
         original_lp.get("original_source_public_Git_blob")==SOURCE_PUBLISHED_GIT_BLOB,
         "original immutable public 2022/2024 provider source blob changed")
    need(independent.get("year")==year and analytic.get("year")==year and
         original_lp.get("source_year")==year and
         independent.get("capacity_semantics")==mode and
         analytic.get("capacity_semantics")==mode and original_lp.get("mode")==mode,
         "year or storage capacity interpretation inconsistent across evidence")
    need(analytic.get("source_independently_rebuilt_90pct_report_SHA256")==
         hashlib.sha256(independent_bytes).hexdigest(),
         "analytical threshold not linked to exact independent 90% report")
    target_hash=source["price_neutral_E_uniform_hydrogen_service"]["hourly_target_f64_sha256"]
    price_hash=source["source_year_price_f64_sha256"]
    wind_hash=source["source_year_wind_f64_sha256"]
    need(source_f64_vector_hash(wind)==wind_hash and
         source_f64_vector_hash(target)==target_hash,
         "original source hourly immutable provider or H2 SHA mismatch")
    need(independent.get("original_observed_price_float64_SHA256")==price_hash and
         original_lp.get("original_source_price_f64_sha256")==price_hash and
         independent.get("original_observed_wind_float64_SHA256")==wind_hash and
         original_lp.get("original_source_wind_f64_sha256")==wind_hash and
         analytic.get("original_registered_source_wind_power_float64_SHA256")==wind_hash and
         analytic.get("original_registered_source_fixed_hourly_H2_float64_SHA256")==target_hash and
         independent.get("same_frozen_hourly_hydrogen_service_float64_SHA256")==target_hash and
         original_lp.get("original_hourly_hydrogen_service_f64_sha256")==target_hash,
         "published original source price/wind/H2 hashes differ across independent reviews")
    need(independent.get("independent_reconstruction_reports_E_LP_infeasible") is True and
         independent.get("independent_EplusS_feasible_full_year_original_primal_replay_passed") is True and
         independent.get("paired_E_minus_EplusS_cost_saving_eur") is None and
         analytic.get("90pct_paired_wholesale_cost_saving_eur") is None and
         analytic.get("independent_E_LP_infeasible_at_90pct_wind") is True and
         analytic.get("independent_EplusS_MILP_full_hourly_witness_feasible_at_90pct_wind") is True and
         analytic.get("scientific_v1_0_release_allowed") is False and
         independent.get("real_site_physical_infeasibility_certified") is False,
         "independent fixed-service no-cost comparison gate missing")
    origin_cases=original_lp.get("E_and_EplusS_independent_LP_relaxed_global_cost_lower_bound_cases")
    need(type(origin_cases) is dict and set(origin_cases)=={"E","E_plus_S"} and
         origin_cases["E"]["LP_optimally_solved"] is True and
         origin_cases["E"]["independent_relaxed_LP_dual_KKT_passed"] is True and
         original_lp.get("original_HiGHS_branch_and_bound_dual_reconstructed") is False,
         "original full-wind E LP feasibility independently reviewed result missing")
    cut=analytic.get("analytical_cut_boundary_not_actual_optimal_integer_threshold",{})
    low=float_number(
        cut.get("lower_factor_at_which_energy_storage_inequality_still_PROVES_infeasible"),
        "analytic source lower cut")
    high=float_number(
        cut.get("first_higher_factor_at_which_inequality_NO_LONGER_PROVES_infeasible"),
        "analytic no-violation factor")
    need(.9 < low < high < 1. and high-low<1e-7 and
         cut.get("actual_E_MILP_feasibility_transition_factor_verified") is None and
         cut.get("nonviolation_at_upper_factor_does_not_prove_MILP_feasibility") is True,
         "analytical H2 source-energy necessary cut not verified")
    return low,high


def independently_validate_feasible_lp_witness(problem,x):
    """Feasible numerical vector: explicitly check rebuilt source E constraints."""
    x=np.asarray(x,dtype=float)
    need(x.ndim==1 and x.shape==problem["c"].shape and np.isfinite(x).all(),
         "HiGHS feasible E LP missing usable vector")
    eq=float(np.max(np.abs(problem["A_eq"]@x-problem["b_eq"])))
    ub=float(np.max(np.maximum(problem["A_ub"]@x-problem["b_ub"],0.)))
    box=float(np.max(np.maximum(np.maximum(
        problem["lower"]-x,x-problem["upper"]),0.)))
    need(eq<=2e-4 and ub<=2e-4 and box<=2e-4,
         "independently rebuilt E feasibility LP primal violates source equations")
    return {"maximum_LP_primal_equality_residual":eq,
            "maximum_LP_primal_inequality_violation":ub,
            "maximum_LP_variable_bound_violation":box,
            "binary_unit_commitment_or_direction_verified":False,
            "actual_integer_E_dispatch_feasible":False}


def independent_relaxed_lp_feasible_at_factor(wind,price,target,params,duty,factor,
                                             *,time_limit_s=120):
    need(type(time_limit_s) is int and 10<=time_limit_s<=7200,
         "unregistered independent LP per-case resource limit")
    need(type(factor) in (int,float) and .9<=float(factor)<=1.,
         "wind factor outside registered original source-world interval")
    w=np.asarray(wind,dtype=np.float64)*float(factor)
    original_price=np.asarray(price,dtype=np.float64)
    fixed_target=np.asarray(target,dtype=np.float64)
    model=construct_lp(w,original_price,fixed_target,params,duty)
    result=linprog(
        c=np.zeros_like(model["c"]),
        A_eq=model["A_eq"],b_eq=model["b_eq"],
        A_ub=model["A_ub"],b_ub=model["b_ub"],
        bounds=list(zip(model["lower"],model["upper"])),
        method="highs",options={"presolve":True,
                                "time_limit":float(time_limit_s)},
    )
    need(result.status in (0,2),
         "independent E feasibility LP numerical failure/time-limit; do not infer model feasibility")
    if result.status==0:
        checks=independently_validate_feasible_lp_witness(model,result.x)
        return {"factor":float(factor),"status":"LP_PRIMAL_FEASIBLE_NOT_INTEGER",
                "HiGHS_status":0,**checks}
    need(result.x is None,
         "HiGHS reported LP infeasible but unexpectedly returned a feasible vector")
    return {"factor":float(factor),
            "status":"SOURCE_MODEL_LP_INFEASIBLE_NO_FARKAS_RAY",
            "HiGHS_status":2,
            "independent_LP_infeasibility_Farkas_dual_ray_computed":False,
            "actual_integer_E_dispatch_feasible":False}


def bisect_lp_with_explicit_statuses(low,high,assess,*,steps=8):
    """Pure monotone classifier; failures/ambiguous status must abort."""
    need(type(low) in (int,float) and type(high) in (int,float) and
         math.isfinite(low) and math.isfinite(high) and .9<low<high<=1.,
         "invalid original necessary-cut-to-known-feasible wind interval")
    need(type(steps) is int and 1<=steps<=12,
         "avoid unbounded number of expensive annual source LP solves")
    lo=float(low);hi=float(high);history=[]
    for _ in range(steps):
        mid=(lo+hi)/2.
        r=assess(mid)
        need(type(r) is dict and
             abs(float_number(r.get("factor"),"bisection factor")-mid)<1e-13,
             "independent E LP result from wrong source wind factor")
        status=r.get("status")
        need(status in ("SOURCE_MODEL_LP_INFEASIBLE_NO_FARKAS_RAY",
                        "LP_PRIMAL_FEASIBLE_NOT_INTEGER"),
             "LP feasibility status missing/unknown")
        history.append(r)
        if status=="SOURCE_MODEL_LP_INFEASIBLE_NO_FARKAS_RAY":
            lo=mid
        else:
            hi=mid
    need(lo<hi,"source E LP threshold bisection failed to make progress")
    return {"largest_tested_independent_rebuilt_E_LP_infeasible_factor":lo,
            "smallest_tested_independent_rebuilt_E_LP_feasible_factor":hi,
            "independent_LP_transition_bracket_width":hi-lo,
            "evaluated_factors_and_scalar_residuals_only":history,
            "actual_integer_E_feasible_factor_only_proven_at_1":1.,
            "LP_feasible_does_not_prove_original_integer_MILP_feasible":True,
            "independent_Farkas_ray_produced":False}


def examine(year,mode,private_root,original_public,independent_report,
            analytic_report,reference_lp_report,*,steps=8,time_limit_s=120):
    source,witness,wind,price,target=check_private_source(
        year,mode,private_root,original_public)
    raw=Path(independent_report).read_bytes()
    independent=json.loads(raw.decode("utf-8"))
    analytic_raw=Path(analytic_report).read_bytes()
    analytic=json.loads(analytic_raw.decode("utf-8"))
    lp_raw=Path(reference_lp_report).read_bytes()
    original_lp=json.loads(lp_raw.decode("utf-8"))
    analytical_low,analytical_nonviolating=validate_record_chain(
        year,mode,wind,target,source,independent,analytic,original_lp,raw)
    params=expected_params(20000)
    duty=witness["cases"]["E"]["Type_I_200bar_model_pressure_duty"]
    verified_necessary=scan_interval_factor(
        wind,target,params,duty,factor=analytical_low)
    need(verified_necessary["simple_energy_interval_necessary_condition_violated"] is True,
         "original 2022 analytically proven LP-infeasible wind lower cut changed")
    reference_cut=scan_interval_factor(
        wind,target,params,duty,factor=analytical_nonviolating)
    need(reference_cut["simple_energy_interval_necessary_condition_violated"] is False,
         "original 2022 analytic non-violating upper source cut changed")
    # k=1 is originally E INTEGER-feasible, and its independent LP optimum
    # was KKT-reviewed. It is the only accepted integer-feasible reference.
    result=bisect_lp_with_explicit_statuses(
        analytical_low,1.,
        lambda factor:independent_relaxed_lp_feasible_at_factor(
            wind,price,target,params,duty,factor,time_limit_s=time_limit_s),
        steps=steps)
    need(result["largest_tested_independent_rebuilt_E_LP_infeasible_factor"]>=analytical_low,
         "LP infeasible lower bound cannot be weaker than original analytic cut")
    return {
        "schema_version":SCHEMA,"original_source_year":year,
        "capacity_semantics":mode,"original_calendar_UTC_hours":len(wind),
        "source_four_case_original_Git_blob_sha1":SOURCE_PUBLISHED_GIT_BLOB,
        "source_original_price_f64_sha256":source["source_year_price_f64_sha256"],
        "source_original_wind_electric_power_f64_sha256":source["source_year_wind_f64_sha256"],
        "source_original_hourly_h2_f64_sha256":
            source["price_neutral_E_uniform_hydrogen_service"]["hourly_target_f64_sha256"],
        "analytic_necessary_inequality_infeasible_below_factor":analytical_low,
        "analytic_necessary_inequality_nonviolation_above_factor":analytical_nonviolating,
        "independent_E_original_relaxed_LP_boundary":result,
        "original_source_100pct_wind_E_MILP_feasible":True,
        "original_90pct_wind_E_MILP_infeasible_source_model":True,
        "EplusS_original_90pct_wind_MILP_feasible":True,
        "actual_MILP_feasibility_transition_not_determined":True,
        "original_90pct_pair_operating_economic_saving_eur":None,
        "independent_solver_uses_scipy_HiGHS_original_solver_family":True,
        "public_result_contains_no_hourly_input_or_primal_vectors":True,
        "native_BAFU_or_vendor_CAPEX_or_real_site_certified":False,
        "scientific_v1_0_release_allowed":False,
        "independent_90pct_report_SHA256":hashlib.sha256(raw).hexdigest(),
        "analytical_cut_report_SHA256":hashlib.sha256(analytic_raw).hexdigest(),
        "independent_original_full_wind_cost_LP_report_SHA256":
            hashlib.sha256(lp_raw).hexdigest(),
    }


def summary_markdown(result):
    b=result["independent_E_original_relaxed_LP_boundary"]
    lower=b["largest_tested_independent_rebuilt_E_LP_infeasible_factor"]
    upper=b["smallest_tested_independent_rebuilt_E_LP_feasible_factor"]
    return (
        "# F3-D independent relaxed-LP E model wind-electric-power feasibility bracket\n\n"
        f"Historical source: {result['original_source_year']}, "
        f"{result['capacity_semantics']}; original annual fixed-price-blind hourly H2 service.\n\n"
        f"Independent reconstructed LP E infeasible at **{100*lower:.5f}%** "
        "of original modeled wind ELECTRIC POWER, LP feasible at "
        f"**{100*upper:.5f}%**. The LP bracket has width "
        f"{100*(upper-lower):.5f} percentage points. "
        "This is a relaxed-LP feasibility bracket, NOT the original "
        "integer MILP feasibility transition.\n\n"
        "A source-model E MILP feasible dispatch has been independently "
        "replayed at the original **100%** source wind. At 90%, "
        "E is independently LP-infeasible and its largest-contiguous "
        "H2-energy deficit violates the bank swing by 882.97 kg; "
        "E+S has an independently checked feasible MILP dispatch. "
        "For each wind-factor intermediate LP status, this report "
        "contains only status, factors and (when available) scalar primal "
        "constraint residuals. **No integer feasible witness has been "
        "shown at the upper LP threshold.** A separate E MILP feasibility "
        "search and external optimality proof are required to locate it.\n\n"
        "All calculations are conditional on one historical 2022 model "
        "and its selected H2 service, not a weather-reliability confidence "
        "interval, a 2026 price forecast, a real installation safety case, "
        "full annual H2 contract, matched-service cash saving at k=0.9 "
        "(NULL), verified OEM costs, native BAFU LCIA, or scientific v1.0.\n"
    )


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--year",type=int,choices=(2022,2024),required=True)
    p.add_argument("--mode",choices=("max_inventory","usable_service"),required=True)
    p.add_argument("--private-root",type=Path,required=True)
    p.add_argument("--public-source",type=Path,required=True)
    p.add_argument("--independent-wind-review",type=Path,required=True)
    p.add_argument("--analytic-wind-report",type=Path,required=True)
    p.add_argument("--reference-independent-cost-LP",type=Path,required=True)
    p.add_argument("--steps",type=int,default=8)
    p.add_argument("--time-limit",type=int,default=120)
    p.add_argument("--output-dir",type=Path,required=True)
    a=p.parse_args(argv)
    results=examine(a.year,a.mode,a.private_root,a.public_source,
                    a.independent_wind_review,a.analytic_wind_report,
                    a.reference_independent_cost_LP,
                    steps=a.steps,time_limit_s=a.time_limit)
    need(a.output_dir.is_dir() and not a.output_dir.is_symlink(),
         "existing public research results directory required")
    stem=f"F3D_WIND_090_{a.year}_{a.mode}_INDEPENDENT_E_LP_FEASIBILITY_BRACKET_v1"
    outputs=[
        (a.output_dir/(stem+".json"),
         json.dumps(results,sort_keys=True,indent=2,allow_nan=False)+"\n"),
        (a.output_dir/(stem+".md"),summary_markdown(results)),
    ]
    for path,body in outputs:
        need(not path.exists() or (path.is_file() and not path.is_symlink() and
             path.read_text(encoding="utf-8")==body),
             "existing independent source LP evidence differs; refuse overwrite")
    for path,body in outputs:
        if not path.exists():
            with path.open("x",encoding="utf-8",newline="\n") as out:
                out.write(body)
    bracket=results["independent_E_original_relaxed_LP_boundary"]
    print("F3D_ORIGINAL_SOURCE_E_INDEPENDENT_RELAXED_LP_FEASIBILITY_BRACKET",
          a.year,a.mode,
          bracket["largest_tested_independent_rebuilt_E_LP_infeasible_factor"],
          bracket["smallest_tested_independent_rebuilt_E_LP_feasible_factor"],
          "actual INTEGER wind threshold UNKNOWN; no real-site/v1/BAFU")


if __name__=="__main__":
    main()
