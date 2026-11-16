"""F3-D exogenous H2-service matched architecture robustness, INDEPENDENT LP SCREEN.

The existing historical 2022/2024 study selects an E-maximal hourly H2
reference *from the same E source model* and then reduces modeled wind power.
Near-boundary E infeasibility is therefore partially built in. This new
experiment prespecifies the original named 50 t/day hydrogen service at
50%, 55%, and 60% (25, 27.5, 30 t/day), strictly BELOW every E-selected
2022/2024 source-year reference. E and E+S then receive identical H2 in
every hour within a year/mode/energy scenario: one fixed external service,
not a response chosen after looking at the reduced-wind outcome.

Reconstruct exactly the SOURCE-model LP relaxation under 90%, 95%, or 100%
of recorded wind available ELECTRIC POWER from original provider-year private
arrays. Each LP solves zero objective, reports feasible after independent
matrix residual checks or infeasible when HiGHS status is 2. An LP-feasible
result NEVER proves that the original binary equipment dispatch is feasible;
an LP-infeasible result rules out the matching exact source MILP. Also apply
a conservative solvent-independent necessary energy and inventory inequality
to each case. No paired cost is inferred; economics require a subsequent
original matched-service *integer* MILP for both alternatives.

Outputs are scalar-only SOURCE-HASH verified public JSON and Markdown. No raw
price/wind arrays, private full-year H2 schedule, or hourly dispatch released.
This is NOT a future contract, industrial safety case, physical uncertainty
distribution, site-LCA, manufacturer economics, or scientific v1.0 release.
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
    construct_lp, check_private_source, SOURCE_PUBLISHED_GIT_BLOB
)
from .f3d_independent_wind_lp_bracket import (
    independently_validate_feasible_lp_witness
)
from .f3d_wind_reduction_independent_feasibility import (
    necessary_interval_deficit, source_f64_vector_hash
)
from .f3d_external_year_private_witness_replay import expected_params, need

SCHEMA="ptxlens.f3d_original_year_exogenous_fixed_h2_service_pair_LP_screen.v1"
DAY_TONNES=(25.,27.5,30.)
WIND_POWER_FACTORS=(.90,.95,1.00)
CASES=("E","E_plus_S")
UTC_HOURS={2022:8760,2024:8784}
ORIGINAL_CONTRACT_REFERENCE_T_PER_DAY=50.
MAX_SOURCE_WIND_POWER_MW=125.685


def fixed_service(utc_hours,tonnes_day):
    """Invariant original user-requested H2 product, never selected post-stress."""
    need(type(utc_hours) is int and utc_hours in UTC_HOURS.values(),
         "only exact source-registered 2022/2024 hourly calendars admitted")
    need(type(tonnes_day) in (int,float) and
         float(tonnes_day) in DAY_TONNES,
         "only preregistered exogenous H2 service contracts admitted")
    return np.full(utc_hours, float(tonnes_day)*1000./24.,dtype=np.float64)


def check_reference_below_original_service(selected_original_hourly,tonnes_day,hours):
    """Do not rename the maximal-E boundary stress as exogenous demand."""
    need(type(selected_original_hourly) in (list,tuple,np.ndarray) and
         len(selected_original_hourly)==hours and
         np.isfinite(selected_original_hourly).all(),
         "source original maximal-hourly H2 selection not validated")
    fixed=fixed_service(hours,tonnes_day)
    selected=np.asarray(selected_original_hourly,dtype=np.float64)
    need(np.max(np.abs(selected-selected[0]))<1e-9,
         "original source E service must be price-neutral uniform")
    need(float(fixed[0])<float(np.min(selected))-1e-6,
         "independently selected contract must be STRICTLY below original E-max reference")
    return fixed


def screen_case(wind,price,target,params,duty,wind_factor,*,time_limit_s=120):
    """Independent original-source model LP, with explicit status + constraints."""
    need(type(time_limit_s) is int and 10<=time_limit_s<=7200,
         "LP time budget invalid")
    need(type(wind_factor) in (float,int) and float(wind_factor) in WIND_POWER_FACTORS,
         "wind scenario not preregistered")
    w=np.asarray(wind,dtype=np.float64)
    p=np.asarray(price,dtype=np.float64)
    q=np.asarray(target,dtype=np.float64)
    need(w.ndim==p.ndim==q.ndim==1 and w.shape==p.shape==q.shape and
         np.isfinite(w).all() and np.isfinite(p).all() and np.isfinite(q).all() and
         0.<=float(np.min(w)) and float(np.max(w))<=MAX_SOURCE_WIND_POWER_MW+1e-7 and
         float(np.min(q))>0.,
         "source price/wind/externally prescribed H2 vectors invalid")
    wind_stressed=w*float(wind_factor)
    problem=construct_lp(wind_stressed,p,q,params,duty)
    necessary=necessary_interval_deficit(wind_stressed,q,params,duty)
    result=linprog(
        c=np.zeros_like(problem["c"]), A_eq=problem["A_eq"],b_eq=problem["b_eq"],
        A_ub=problem["A_ub"],b_ub=problem["b_ub"],
        bounds=list(zip(problem["lower"],problem["upper"])),
        method="highs",
        options={"presolve":True,"time_limit":float(time_limit_s)},
    )
    need(result.status in (0,2),
         "source exogenous LP returned inconclusive numerical/time/memory result; abort")
    if result.status==0:
        need(not necessary["simple_energy_interval_necessary_condition_violated"],
             "LP feasible status CONTRADICTS independently established storage/energy bound")
        checks=independently_validate_feasible_lp_witness(problem,result.x)
        outcome="SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED"
    else:
        need(result.x is None,
             "source LP reported infeasible but returned a non-null incumbent")
        checks=None
        outcome="SOURCE_LP_INFEASIBLE_ORIGINAL_INTEGER_MODEL_IMPOSSIBLE"
    return {
        "source_stress_wind_electric_power_multiplier":float(wind_factor),
        "source_E_or_EplusS_original_model_LP_status":outcome,
        "HiGHS_LP_status_code":int(result.status),
        "necessary_energy_inventory_cut_proved_infeasible":
            necessary["simple_energy_interval_necessary_condition_violated"],
        "necessary_inventory_energy_deficit_minus_bank_swing_kg":
            necessary["max_interval_deficit_minus_available_inventory_kg"],
        "source_equation_reconstructed_LP_primal_residuals_if_feasible":checks,
        "original_integer_MILP_feasible":None if result.status==0 else False,
        "LP_solver_family_independent":False,
        "no_primal_Farkas_certificate":True,
        "source_matched_service_annual_cost_saving_eur":None,
        "real_site_or_vendor_capex_or_BAFU_LCIA_certified":False,
    }


def screen_year(year,mode,private_root,original_public,*,time_limit_s=120):
    need(year in UTC_HOURS and mode in ("max_inventory","usable_service"),
         "unknown original source year and physical bank capacity semantics")
    original,private_witness,wind,price,original_h2=check_private_source(
        year,mode,private_root,original_public)
    need(len(wind)==len(price)==len(original_h2)==UTC_HOURS[year],
         "original source year hourly calendar wrong")
    need(source_f64_vector_hash(wind)==original["source_year_wind_f64_sha256"] and
         source_f64_vector_hash(price)==original["source_year_price_f64_sha256"] and
         source_f64_vector_hash(original_h2)==
         original["price_neutral_E_uniform_hydrogen_service"]["hourly_target_f64_sha256"],
         "original 2022/2024 source input and price-blind selected H2 SHA changed")
    hardware={
        name:(expected_params(capacity),
              private_witness["cases"][name]["Type_I_200bar_model_pressure_duty"])
        for name,capacity in (("E",20000),("E_plus_S",40000))
    }
    cases=[]
    for tonnes_day in DAY_TONNES:
        target=check_reference_below_original_service(
            original_h2,tonnes_day,UTC_HOURS[year])
        # The exogenous target is REUSED byte-for-byte for E and E+S
        # and for all k. No price-blind selector rerun per stress.
        target_sha=source_f64_vector_hash(target)
        for multiplier in WIND_POWER_FACTORS:
            pair={}
            for name in CASES:
                params,duty=hardware[name]
                pair[name]=screen_case(
                    wind,price,target,params,duty,multiplier,
                    time_limit_s=time_limit_s)
            e=pair["E"];es=pair["E_plus_S"]
            e_status=e["HiGHS_LP_status_code"]
            s_status=es["HiGHS_LP_status_code"]
            # A relaxed LP cannot prove either E or E+S integer feasibility.
            # Even when both LPs are feasible, a cost case must be solved
            # separately for both binary original models.
            if e_status==2 and s_status==0:
                inference="E_INTEGER_INFEASIBLE__ES_RELAXED_LP_ONLY_FEASIBLE_NOT_INTEGER"
            elif e_status==2 and s_status==2:
                inference="BOTH_ORIGINAL_INTEGER_MODELS_INFEASIBLE"
            elif e_status==0 and s_status==2:
                inference="ES_INTEGER_INFEASIBLE__E_RELAXED_LP_ONLY_FEASIBLE"
            else:
                inference="BOTH_RELAXED_LPS_FEASIBLE__INTEGER_STATUS_UNKNOWN"
            cases.append({
                "source_year":year,"capacity_semantics":mode,
                "exogenous_H2_tonnes_per_day":float(tonnes_day),
                "exogenous_H2_fraction_of_original_50t_day_reference":
                    float(tonnes_day)/ORIGINAL_CONTRACT_REFERENCE_T_PER_DAY,
                "exogenous_H2_original_same_hourly_SHA256":target_sha,
                "exogenous_same_product_annual_H2_kg":float(np.sum(target)),
                "source_wind_power_multiplier":float(multiplier),
                "E_vs_EplusS_source_LP_status":inference,
                "cases":pair,
                "matched_source_annual_E_minus_EplusS_cost_saving_eur":None,
                "E_and_ES_original_integer_dispatch_both_certified":False,
            })
    need(len(cases)==len(DAY_TONNES)*len(WIND_POWER_FACTORS),
         "missing prespecified source-year matched-service comparison cells")
    return {
        "schema_version":SCHEMA,"source_year":year,"capacity_semantics":mode,
        "source_calendar_UTC_hours":UTC_HOURS[year],
        "source_original_4_case_public_Git_blob_sha1":SOURCE_PUBLISHED_GIT_BLOB,
        "source_original_price_float64_SHA256":original["source_year_price_f64_sha256"],
        "source_original_wind_power_float64_SHA256":original["source_year_wind_f64_sha256"],
        "source_original_E_max_selected_hourly_H2_float64_SHA256":
            original["price_neutral_E_uniform_hydrogen_service"]["hourly_target_f64_sha256"],
        "original_selected_E_max_nominal_tonnes_day":
            original["price_neutral_E_uniform_hydrogen_service"]["modelled_delivered_h2_tonnes_per_day"],
        "prespecified_exogenous_delivery_tonnes_day":list(DAY_TONNES),
        "source_wind_electric_power_multipliers":list(WIND_POWER_FACTORS),
        "source_price_year_input_unchanged":True,
        "same_H2_target_hourly_for_E_and_ES_at_every_wind_factor":True,
        "exogenous_delivery_schedules_selected_without_looking_at_stressed_wind_outcomes":True,
        "nine_service_factor_pairs_two_architectures_LP_cells":cases,
        "original_integer_dispatch_or_matched_wholesale_savings_certified":False,
        "real_site_or_manufacturer_or_native_BAFU_or_scientific_v1_0":False,
    }


def markdown(result):
    rows=result["nine_service_factor_pairs_two_architectures_LP_cells"]
    lines=[
        "# F3-D exogenous H2 matched-service model resilience LP screening",
        "",
        f"Original observed source year: {result['source_year']}; physical "
        f"storage interpretation: {result['capacity_semantics']}.",
        "",
        "Predeclared service levels **25, 27.5 and 30 tonnes/day** from the "
        "original nominal 50t/day H2 contract, each STRICTLY below the "
        "original source selected E-only maximal uniform service. "
        "Their hourly H2 targets are identical for E and E+S and each "
        "observed-wind-electricity multiplier 0.90, 0.95 and 1.00.",
        "",
        "| Exogenous H2 t/day | Original wind POWER factor | E 20t relaxed LP | "
        "E+S 40t relaxed LP | Source matched service economics |",
        "|---:|---:|---|---|---|",
    ]
    for r in rows:
        e=r["cases"]["E"]["source_E_or_EplusS_original_model_LP_status"]
        es=r["cases"]["E_plus_S"]["source_E_or_EplusS_original_model_LP_status"]
        lines.append(
            f"| {r['exogenous_H2_tonnes_per_day']:.1f} | "
            f"{r['source_wind_power_multiplier']:.2f} | "
            f"{e} | {es} | NULL |"
        )
    lines.extend([
        "",
        "Independent PtXLens reconstructs the original full hourly E/E+S "
        "constraints and tests *linear-programming relaxations only*; "
        "a feasible LP solution does NOT prove the original mixed-integer "
        "equipment-dispatch model can operate. A source LP status-2 "
        "infeasibility rules out the original integer model. A separate "
        "necessary storage-and-energy inequality can independently prove "
        "certain infeasible cases, but nonviolation proves nothing.",
        "",
        "This is a preregistered throughput comparison designed to remove "
        "the E-only maximal-throughput selection artifact of the earlier "
        "90%-wind resilience demonstration. Successful LP screening "
        "must be followed by both E and E+S ORIGINAL-MODEL integer feasibility "
        "replays and, if economic costs are compared, original annual MILP "
        "cost minimization under the identical exogenous product.",
        "",
        "No site-measured wind, hydrogen contracts, modelled availability "
        "probabilities, native BAFU:2026 manufacturing LCIA, manufacturer "
        "CAPEX/OPEX, forward price forecasts, whole-plant viability or "
        "programme scientific v1.0 is established.",
        "",
    ])
    return "\n".join(lines)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year",required=True,type=int,choices=(2022,2024))
    parser.add_argument("--mode",required=True,choices=("max_inventory","usable_service"))
    parser.add_argument("--private-root",required=True,type=Path)
    parser.add_argument("--public-source",required=True,type=Path)
    parser.add_argument("--output-dir",required=True,type=Path)
    parser.add_argument("--time-limit",type=int,default=120)
    opt=parser.parse_args(argv)
    result=screen_year(opt.year,opt.mode,opt.private_root,opt.public_source,
                       time_limit_s=opt.time_limit)
    need(opt.output_dir.is_dir() and not opt.output_dir.is_symlink(),
         "public output directory must be present and nonsymlink")
    basename=f"F3D_{opt.year}_{opt.mode}_EXOGENOUS_H2_SOURCE_LP_FEASIBILITY_SCREEN_v1"
    files=[
        (opt.output_dir/(basename+".json"),
         json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n"),
        (opt.output_dir/(basename+".md"),markdown(result)),
    ]
    for path,payload in files:
        need(not path.exists() or (path.is_file() and not path.is_symlink() and
             path.read_text(encoding="utf-8")==payload),
             "cannot overwrite conflicting original source-model publication")
    for path,payload in files:
        if not path.exists():
            with path.open("x",encoding="utf-8",newline="\n") as output:
                output.write(payload)
    print("F3D_ORIGINAL_YEAR_EXOGENOUS_MATCHED_H2_LP_SCREEN",
          opt.year,opt.mode,
          "3 fixed service levels x 3 source power factors x 2 equipment variants",
          "original integer feasibility and source-market saving NOT YET PROVEN")


if __name__=="__main__":
    main()
