"""F3-D independent assessment of the -10% modelled wind POWER experiment.

The source PtXFlex E cost solver marked 2022 fixed-hour H2 delivery infeasible
even after relaxing binaries; source E+S reported a feasible optimized model.
This reviewer:
  (1) recreates the wind change from source-hash verified PRIVATE original data,
  (2) independently reconstructs the original LP from physical constraints,
  (3) resolves zero-objective E feasibility using SciPy/HiGHS,
  (4) independently checks the E+S full-hour witness against THAT matrix,
  (5) searches for an analytic bounded-storage energy deficit interval.
Publication is scalar-only and the E-vs-E+S *cost difference stays NULL*.

An LP solver status 2 is NOT independently exported as a Farkas certificate.
The analytical interval test, if positive, proves a necessary condition is
violated without relying on any LP solver; if negative, it proves nothing.
All findings apply only to the frozen source model, not physical installations.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from .f3d_source_year_independent_cost_lp_dual import (
    construct_lp, check_private_source, SOURCE_PUBLISHED_GIT_BLOB,
)
from .f3d_external_year_counterfactual_independent_review import (
    independent_pair, PRIVATE_SOURCE_SCHEMA, CF_SCHEMA,
)
from .f3d_external_year_private_witness_replay import (
    expected_params, f64_hash, need,
)

SCHEMA="ptxlens.f3d_2022_2024_wind_reduction_independently_rebuilt_LP_feasibility.v1"
VARIANT="wind_power_090"


def necessary_interval_deficit(wind_power_mw, target_kg_h, params, duty):
    """Find maximum contiguous *necessary* energy/storage deficit in O(N).

    For an interval [a,b], conservation and nonnegative leakage imply
      SUM(H2 demand) <= yield * SUM(PEM power) + max_bank - min_bank.
    The power/electricity balance and nonnegative compression/curtailment imply
      PEM power <= min(rated max load, wind available + signed grid import limit).
    Therefore a single interval for which demand exceeds this conservative
    upper bound *proves* that no physical primal dispatch exists under the
    original LP/MILP constraints. It ignores ramp, charge bounds, compression,
    leak, commitment and cyclic endpoint; omitting these makes the bound
    more permissive, NOT more restrictive. Nonviolating intervals do not
    demonstrate feasibility.

    Return indices only, never user-private source vectors.
    """
    w=np.asarray(wind_power_mw,dtype=float)
    q=np.asarray(target_kg_h,dtype=float)
    need(w.shape==q.shape and w.ndim==1 and len(w)>1 and
         np.isfinite(w).all() and np.isfinite(q).all() and
         np.min(w)>=0 and np.min(q)>=0,
         "nonnegative equal-length finite original model power/H2 needed")
    need(params["capacity_kg"]==duty["scenario_capacity_kg"] and
         duty["capacity_semantics"] in ("max_inventory","usable_service"),
         "unverified source pressure bank or capacity convention")
    bottom=(float(duty["gas_heel_kg"]) if
            duty["capacity_semantics"]=="max_inventory" else 0.)
    usable=float(params["capacity_kg"])-bottom
    need(0<usable and bottom>=0,"invalid physical inventory interval")
    pmax=float(params["rated_mw"])*float(params["max_load_fraction"])
    gridmax=float(params["grid_max_mw"])
    y=float(params["h2_coefficient_kg_mwh"])
    need(pmax>0 and gridmax>0 and y>0,
         "invalid original physical PEM/grid yield boundary")
    upper_h2=y*np.minimum(pmax,w+gridmax)
    deficit=q-upper_h2
    # O(N) maximum subarray (Kadane); also works with variable hourly target.
    best=0.
    running=0.
    active_start=0
    best_start=0
    best_end=0
    for index,val in enumerate(deficit):
        if running<=0.:
            active_start=index
            running=float(val)
        else:
            running+=float(val)
        if running>best:
            best=running
            best_start=active_start
            best_end=index+1
    slack=best-usable
    # A safety margin of 1e-4 kg avoids treating float accumulation at exact
    # equality as a mathematical contradiction.
    decisive=slack>1e-4
    return {
        "max_contiguous_net_H2_deficit_kg_under_generous_PEM_power_upper_bound":float(best),
        "physical_bank_inventory_swing_upper_limit_kg":float(usable),
        "max_interval_deficit_minus_available_inventory_kg":float(slack),
        "violating_interval_start_UTC_hour_index":int(best_start) if decisive else None,
        "violating_interval_end_exclusive_UTC_hour_index":int(best_end) if decisive else None,
        "simple_energy_interval_necessary_condition_violated":bool(decisive),
        "simple_energy_interval_condition_is_sufficient_for_infeasibility_only":True,
        "did_NOT_assume_wind_speed_reduction":True,
    }


def independent_reconstructed_constraint_feasibility(problem,x):
    """Recheck previously reviewed integer feasible ES witness using new LP."""
    x=np.asarray(x,dtype=float)
    lo=problem["lower"];hi=problem["upper"]
    need(x.shape==lo.shape==hi.shape and np.isfinite(x).all(),
         "counterfactual hourly ES primal missing/size changed")
    equality=float(np.max(np.abs(problem["A_eq"]@x-problem["b_eq"])))
    inequality=float(np.max(np.maximum(problem["A_ub"]@x-problem["b_ub"],0.)))
    box=float(np.max(np.maximum(np.maximum(lo-x,x-hi),0.)))
    # Independently built model has both relaxed unit/direction vars.
    states=x.reshape(-1,8)
    binary=float(max(np.max(np.abs(states[:,1]-np.rint(states[:,1]))),
                     np.max(np.abs(states[:,7]-np.rint(states[:,7])))))
    result={
        "maximum_independently_rebuilt_equality_residual":equality,
        "maximum_independently_rebuilt_inequality_violation":inequality,
        "maximum_independently_rebuilt_variable_bound_violation":box,
        "maximum_integer_commitment_direction_violation":binary,
        "source_MILP_witness_passes_independent_reconstructed_LP_feasibility":
            equality<=2e-4 and inequality<=2e-4 and box<=2e-4 and binary<=1e-5,
    }
    need(result["source_MILP_witness_passes_independent_reconstructed_LP_feasibility"],
         "original source E+S feasible MILP witness failed independently rebuilt LP")
    return result


def review(year,mode,private_root,public_source,*,limit_s=900):
    need(year in (2022,2024) and mode in ("max_inventory","usable_service"),
         "unregistered original observed year/capacity semantics")
    need(type(limit_s) is int and 10<=limit_s<=7200,
         "independent original wind LP time limit outside allowed range")
    published,original_witness,original_wind,original_price,target=check_private_source(
        year,mode,private_root,public_source)
    pair=independent_pair(year,mode,VARIANT,private_root,public_source)
    need(pair.get("schema_version")==CF_SCHEMA and
         pair.get("year")==year and pair.get("mode")==mode and
         pair.get("variant")==VARIANT and
         pair.get("reference_original_public_four_case_Git_blob_sha1")==
         SOURCE_PUBLISHED_GIT_BLOB,
         "independent original-source counterfactual pair invalid")
    reported=pair.get("cases",{})
    need(set(reported)=={"E","E_plus_S"} and
         reported["E"]["status"]=="SOURCE_SOLVER_REPORTED_LP_INFEASIBLE_NO_COST" and
         reported["E_plus_S"]["status"]==
             "INDEPENDENT_FULL_YEAR_PRIMAL_AND_PRESSURE_COST_REPLAY_PASSED",
         "require E source-reported LP-infeasible and independently replayed E+S feasible")
    need(pair.get("paired_E_minus_EplusS_nominal_operational_saving_eur") is None and
         pair.get("paired_source_solver_reported_bound_interval_eur") is None and
         pair.get("economic_result_null_if_any_unverified_or_infeasible") is True,
         "source economic comparison must be NULL under original E infeasibility")
    w=np.asarray(original_wind,dtype=float)*.9
    p=np.asarray(original_price,dtype=float)
    q=np.asarray(target,dtype=float)
    need(f64_hash(w)==pair["counterfactual_wind_power_f64_SHA256"] and
         f64_hash(p)==pair["counterfactual_price_f64_SHA256"] and
         f64_hash(q)==pair["fixed_original_price_blind_E_hydrogen_service_f64_SHA256"],
         "independent new wind electrical-power transformation/H2 source SHA differs")
    e_params=expected_params(20000)
    es_params=expected_params(40000)
    e_duty=original_witness["cases"]["E"]["Type_I_200bar_model_pressure_duty"]
    es_duty=original_witness["cases"]["E_plus_S"]["Type_I_200bar_model_pressure_duty"]
    E=construct_lp(w,p,q,e_params,e_duty)
    # E-only zero objective, not price-optimized or a new H2 target.
    solver=linprog(
        c=np.zeros_like(E["c"]), A_eq=E["A_eq"],b_eq=E["b_eq"],
        A_ub=E["A_ub"],b_ub=E["b_ub"],
        bounds=list(zip(E["lower"],E["upper"])),method="highs",
        options={"time_limit":float(limit_s),"presolve":True},
    )
    need(solver.status in (0,2),
         "independent original E LP returned numerical/time-limit inconclusive status")
    independent_infeasible=(int(solver.status)==2 and solver.x is None)
    # Even if the independent LP finds a feasible vector, we preserve the
    # disagreement and REFUSE an admission claim rather than misreporting E.
    necessity=necessary_interval_deficit(w,q,e_params,e_duty)
    es_file=(Path(private_root)/"results"/"counterfactuals"/
             f"PRIVATE_F3D_CF_{year}_{mode}_{VARIANT}_E_plus_S.json")
    private_es=json.loads(es_file.read_text(encoding="utf-8"))
    need(private_es.get("schema_version")==PRIVATE_SOURCE_SCHEMA and
         private_es.get("scenario")=="E_plus_S" and
         private_es.get("outcome")==
         "ORIGINAL_FULL_YEAR_MILP_PRIMAL_SOLVER_BOUND_CERTIFIED_LOCAL_NOT_EXTERNAL_DUAL",
         "changed ES integer source model witness or unverified MILP result")
    es_original=np.asarray(private_es["source_original_model_8field_primal_witness"],
                           dtype=np.float64)
    need(es_original.shape==(len(q),8) and
         f64_hash(es_original.reshape(-1))==
         reported["E_plus_S"]["independent_hourly_primal_SHA256"],
         "independent E+S original hourly witness hash differs from prior PtXLens")
    ES=construct_lp(w,p,q,es_params,es_duty)
    escheck=independent_reconstructed_constraint_feasibility(ES,es_original.ravel())
    assert_explicit_algebraic_contradiction=necessity[
        "simple_energy_interval_necessary_condition_violated"]
    # If necessary-condition proof contradicts the LP solver, flag it, not
    # silently certify an unsupported model assumption.
    need(not assert_explicit_algebraic_contradiction or independent_infeasible,
         "analytical model E necessary-condition contradicts independently reconstructed E LP")
    need(independent_infeasible,
         "original source E LP status 2 NOT confirmed by independent source-matrix rebuild")
    return {
        "schema_version":SCHEMA,
        "year":year,"capacity_semantics":mode,
        "source_calendar_hours":len(q),
        "original_4_case_public_Git_blob_sha1":SOURCE_PUBLISHED_GIT_BLOB,
        "original_observed_price_float64_SHA256":f64_hash(p),
        "original_observed_wind_float64_SHA256":f64_hash(original_wind),
        "counterfactual_wind_model_electric_power_float64_SHA256":f64_hash(w),
        "same_frozen_hourly_hydrogen_service_float64_SHA256":f64_hash(q),
        "original_hourly_H2_service_kg":float(q[0]),
        "original_matched_annual_H2_service_kg":float(np.sum(q)),
        "intervention":"original PyNEXUS modeled available wind electrical POWER * 0.90, original NL A44 price fixed",
        "source_reported_E_LP_status_2_infeasible":True,
        "independently_rebuilt_E_relaxed_LP_model_zero_objective_HiGHS_status":int(solver.status),
        "independent_reconstruction_reports_E_LP_infeasible":independent_infeasible,
        "independent_source_matrix_same_HiGHS_backend_not_second_solver":True,
        "native_Farkas_dual_infeasibility_ray_exported":False,
        "analytical_energy_storage_interval":necessity,
        "independent_EplusS_feasible_full_year_original_primal_replay_passed":True,
        "EplusS_independent_new_LP_matrix_constraint_residuals":escheck,
        "EplusS_modelled_wholesale_cost_nominal_source_eur":
            reported["E_plus_S"]["source_model_cost_eur"],
        "E_modelled_wholesale_cost_nominal_source_eur":None,
        "paired_E_minus_EplusS_cost_saving_eur":None,
        "paired_saving_EUR_per_kg_H2":None,
        "original_source_model_E_infeasible_EplusS_feasible_under_fixed_hourly_H2":True,
        "source_model_operational_feasibility_advantage_NOT_financial_saving":True,
        "real_site_physical_infeasibility_certified":False,
        "actual_vendor_equipment_or_native_BAFU_LCIA_or_v1_0_certified":False,
        "no_hourly_provider_prices_wind_or_private_dispatch_vectors_exported":True,
    }


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--year",type=int,choices=(2022,2024),required=True)
    p.add_argument("--mode",choices=("max_inventory","usable_service"),required=True)
    p.add_argument("--private-root",required=True,type=Path)
    p.add_argument("--public-source",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--LP-time-limit",type=int,default=900)
    a=p.parse_args(argv)
    result=review(a.year,a.mode,a.private_root,a.public_source,limit_s=a.LP_time_limit)
    path=a.output
    need(path.parent.is_dir() and not path.is_symlink(),
         "existing allowed scientific public output folder required")
    body=json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n"
    need(not path.exists() or (path.is_file() and
         path.read_text(encoding="utf-8")==body),
         "immutable source-model feasibility report already exists and differs")
    if not path.exists():
        with path.open("x",encoding="utf-8",newline="\n") as fp:fp.write(body)
    print(f"F3D_WIND_REDUCTION_INDEPENDENT_SOURCE_MATRIX_LP_INFEASIBILITY "
          f"{a.year} {a.mode}: E reported infeasible, "
          "E+S independently feasible; paired value NULL; "
          f"direct analytic cut violation={result['analytical_energy_storage_interval']['simple_energy_interval_necessary_condition_violated']}; "
          "no independent Farkas or full-site / BAFU / v1 release")


if __name__=="__main__":
    main()
