"""F3-D independent 2022 exogenous H30 W090 E/E+S integer dispatch replay.

Reads original registered provider-year private hourly prices and ERA5 model
wind, independently rebuilt predeclared 30t/day hourly hydrogen schedule and
both original PtXFlex integer source witnesses in PtX_PRIVATE_RESEARCH.
Independently recomputes ALL 8,760 (or 8,784) physical mass, electrical,
curtailment, ramp, commitment, binary storage exclusivity, variable bounds,
signed market settlement, pressure/CoolProp EOS and source cost accuracy.

Only after BOTH E and E+S individually pass may a PUBLIC scalar-only
original-year paired modelled electricity saving be released. Source-reported
HiGHS integer MIP bounds are NOT independent optimizer dual proofs.
A missing case, timed-out solver, noncertified primal or mismatched service
is NOT converted to zero or negative storage saving.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from .f3d_source_year_independent_cost_lp_dual import (
    check_private_source, SOURCE_PUBLISHED_GIT_BLOB
)
from .f3d_exogenous_service_lp_screen import (
    fixed_service, DAY_TONNES, WIND_POWER_FACTORS, SCHEMA as LP_SCHEMA
)
from .f3d_wind_reduction_independent_feasibility import source_f64_vector_hash
from .f3d_external_year_private_witness_replay import (
    expected_params, replay_equations, verify_eos, need
)

SCHEMA="ptxlens.f3d_exogenous_H30_W090_both_integer_primal_independently_replayed.v1"
PRODUCER_SCHEMA="ptxflex.f3d_PRIVATE_exogenous_fixed_h2_source_year_cost_integer_witness.v1"
ORIGINAL_REFERENCE_SOURCE_GIT_BLOB="ca07f5ef1e381fa157982bc5a68e46ce3022003a"
H2_TPD=30.
WIND_FACTOR=.9
CASES=("E","E_plus_S")


def check_screen(screen,year,mode,original,price,wind,selected,target):
    """Audit source LP screening identity WITHOUT running price-optimized MILPs."""
    need(screen.get("schema_version")==LP_SCHEMA and
         screen.get("source_year")==year and
         screen.get("capacity_semantics")==mode and
         screen.get("source_original_4_case_public_Git_blob_sha1")==SOURCE_PUBLISHED_GIT_BLOB and
         screen.get("source_calendar_UTC_hours")==len(price)==len(wind)==len(target) and
         screen.get("source_original_price_float64_SHA256")==source_f64_vector_hash(price) and
         screen.get("source_original_wind_power_float64_SHA256")==source_f64_vector_hash(wind) and
         screen.get("source_original_E_max_selected_hourly_H2_float64_SHA256")==source_f64_vector_hash(selected) and
         screen.get("source_price_year_input_unchanged") is True and
         screen.get("same_H2_target_hourly_for_E_and_ES_at_every_wind_factor") is True and
         screen.get("exogenous_delivery_schedules_selected_without_looking_at_stressed_wind_outcomes") is True and
         screen.get("original_integer_dispatch_or_matched_wholesale_savings_certified") is False and
         screen.get("real_site_or_manufacturer_or_native_BAFU_or_scientific_v1_0") is False,
         "original exogenous E/ES independently reconstructed LP research source inconsistent")
    need(screen.get("prespecified_exogenous_delivery_tonnes_day")==list(DAY_TONNES) and
         screen.get("source_wind_electric_power_multipliers")==list(WIND_POWER_FACTORS),
         "registered independent service/wind research matrix changed")
    rows=screen.get("nine_service_factor_pairs_two_architectures_LP_cells",[])
    need(type(rows) is list and len(rows)==9,
         "all independent source-year E/E+S exogenous LP observations missing")
    selected_case=[r for r in rows if r.get("exogenous_H2_tonnes_per_day")==H2_TPD and
                   r.get("source_wind_power_multiplier")==WIND_FACTOR]
    need(len(selected_case)==1,"selected H30 W090 prespecified service LP case missing")
    record=selected_case[0]
    need(record.get("exogenous_H2_original_same_hourly_SHA256")==
         source_f64_vector_hash(target) and
         abs(float(record.get("exogenous_same_product_annual_H2_kg",float("nan")))-
             float(np.sum(target)))<.005 and
         record.get("matched_source_annual_E_minus_EplusS_cost_saving_eur") is None and
         record.get("E_and_ES_original_integer_dispatch_both_certified") is False,
         "original H30 W090 LP screen silently changed contract/claimed integer results")
    rows=record.get("cases")
    need(type(rows) is dict and set(rows)==set(CASES),
         "LP screening missing one of the pair")
    for name in CASES:
        row=rows[name]
        need(row.get("HiGHS_LP_status_code")==0 and
             row.get("source_E_or_EplusS_original_model_LP_status")==
                 "SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED" and
             row.get("original_integer_MILP_feasible") is None,
             name+" predeclared LP did not pass or falsely claimed integer feasibility")


def check_private_case(record,metadata,case,original_wind,price,target,params,duty):
    """Fail-closed independent per-hour mass/electricity/pressure/cost checks."""
    need(type(record) is dict and record.get("schema_version")==PRODUCER_SCHEMA and
         record.get("metadata")==metadata and
         record.get("scenario")==case and
         record.get("outcome")==
            "SOURCE_MILP_SOLVER_REPORTED_COST_BOUND_NOT_INDEPENDENTLY_REPLAYED" and
         record.get("hourly_witness_private_not_for_git") is True and
         record.get("original_provider_price_wind_arrays_not_duplicated") is True and
         record.get("independent_full_year_hourly_physical_replay_complete") is False and
         record.get("independent_original_cost_dual_proof_complete") is False and
         record.get("matched_service_E_minus_ES_cost_saving_eur") is None and
         record.get("real_site_or_manufacturer_or_BAFU_v1_certified") is False,
         "source private annual original MILP witness provenance or scope falsely claimed")
    states=record.get("original_full_hourly_states_8var_PRIVATE")
    need(type(states) is list and len(states)==len(target),
         "original full-hourly PRIVATE 8-var solver states missing")
    audit=replay_equations(
        states, target,
        [float(x)*WIND_FACTOR for x in original_wind],
        price, params,duty,
    )
    eos=verify_eos(
        duty,audit["minimum_source_bank_model_kg"],
        audit["maximum_source_bank_model_kg"],
    )
    cost=record.get("source_solver_cost_eur")
    lower=record.get("source_solver_reported_cost_lower_bound_eur")
    gap=record.get("source_solver_reported_relative_MIP_gap")
    need(all(type(x) in (int,float) and math.isfinite(x)
             for x in (cost,lower,gap)) and
         0<=gap<=1e-6 and lower<=cost+.1,
         "source MILP cost primal/solver-bound or accepted 1e-6 gap invalid")
    need(abs(audit["independent_source_year_signed_grid_cost_eur"]-cost)<.05 and
         abs(audit["modelled_annual_hydrogen_kg"]-
             float(record["source_solver_reported_annual_h2_kg"]))<.005 and
         audit["hourly_states_sha256"]==record.get("original_full_hourly_states_SHA256")==
             record["original_source_solver_audit"]["source_hourly_dispatch_float64_sha256"] and
         audit["hourly_service_sha256"]==
             metadata["exogenous_H2_hourly_SHA256"] and
         audit["hourly_source_price_sha256"]==
             metadata["source_original_price_SHA256"] and
         audit["hourly_source_wind_sha256"]==
             metadata["source_stressed_wind_SHA256"] and
         max(audit["maxima"].values())<=2e-4 and
         eos["independent_313K_CoolProp_Hydrogen_EOS_recomputed"] is True,
         "source whole-year integer dispatch independently fails physics/cost/pressure/source hash")
    return {
        "status":"INDEPENDENT_ORIGINAL_FULL_YEAR_INTEGER_PRIMAL_H2_ELECTRIC_EOS_REPLAY_PASSED",
        "source_modelled_nominal_original_year_wholesale_eur":float(cost),
        "source_reported_solver_cost_lower_bound_eur":float(lower),
        "source_reported_relative_MIP_gap":float(gap),
        "independent_hourly_primal_SHA256":audit["hourly_states_sha256"],
        "independent_source_max_physical_residual":float(max(audit["maxima"].values())),
        "independent_EOS_min_absolute_bar":float(eos["min_bar_absolute"]),
        "independent_EOS_max_absolute_bar":float(eos["max_bar_absolute"]),
        "independent_annual_delivered_H2_kg":float(audit["modelled_annual_hydrogen_kg"]),
        "independent_annual_grid_import_MWh":float(audit["independent_grid_import_mwh"]),
        "independent_annual_grid_export_MWh":float(audit["independent_grid_export_mwh"]),
        "independent_annual_compression_MWh":float(audit["independent_annual_compressor_electricity_mwh"]),
        "original_private_hourly_H2_wind_price_primal_vectors_NOT_in_public":True,
        "independent_integer_cost_dual_tree_proof":False,
    }


def independent_review(year,mode,private_root,original_public,lp_screen):
    need(year in (2022,2024) and mode in ("max_inventory","usable_service"),
         "original source year or pressure storage semantics unregistered")
    private=Path(private_root).resolve(strict=True)
    need(private.name=="PtX_PRIVATE_RESEARCH" and private.is_dir(),
         "approved private original-source archive missing")
    original,witness,wind,price,selected=check_private_source(
        year,mode,private,original_public,
    )
    need(len(wind)==len(price)==len(selected) and
         source_f64_vector_hash(wind)==original["source_year_wind_f64_sha256"] and
         source_f64_vector_hash(price)==original["source_year_price_f64_sha256"],
         "registered original source year hourly price/wind changed")
    target=fixed_service(len(wind),H2_TPD)
    need(float(target[0])<float(min(selected))-1e-6,
         "30t/day externally fixed H2 must be below E-selected maximal service")
    lpbytes=Path(lp_screen).read_bytes()
    screen=json.loads(lpbytes.decode("utf-8"))
    check_screen(screen,year,mode,original,price,wind,selected,target)
    metadata_common={
        "year":year,"mode":mode,
        "exogenous_H2_tonnes_day":H2_TPD,
        "exogenous_H2_annual_kg":float(np.sum(target)),
        "exogenous_H2_hourly_SHA256":source_f64_vector_hash(target),
        "wind_model_electric_power_factor":WIND_FACTOR,
        "source_original_price_SHA256":source_f64_vector_hash(price),
        "source_original_wind_SHA256":source_f64_vector_hash(wind),
        "source_stressed_wind_SHA256":
            source_f64_vector_hash(np.asarray(wind,dtype=np.float64)*WIND_FACTOR),
        "source_original_E_max_H2_SHA256":source_f64_vector_hash(selected),
        "source_public_original_source_blob":SOURCE_PUBLISHED_GIT_BLOB,
        "source_independent_LP_screen_SHA256":hashlib.sha256(lpbytes).hexdigest(),
        "original_site_or_BAFU_or_manufacturer_v1_certified":False,
    }
    rows={}
    for case,capacity in (("E",20000),("E_plus_S",40000)):
        name=f"PRIVATE_F3D_EXOGENOUS_{year}_{mode}_H30_W090_{case}.json"
        file=private/"results"/"exogenous_service_robustness"/name
        need(file.is_file() and not file.is_symlink() and
             file.resolve().is_relative_to(private),
             "PRIVATE E/E+S original full-year integer witness missing or escaped archive")
        record=json.loads(file.read_text(encoding="utf-8"))
        metadata={**metadata_common,"case":case}
        duty=witness["cases"][case]["Type_I_200bar_model_pressure_duty"]
        params=expected_params(capacity)
        need(duty.get("capacity_semantics")==mode and
             duty.get("scenario_capacity_kg")==capacity,
             "source pressure-screen hardware interpretation changed")
        rows[case]=check_private_case(
            record,metadata,case,wind,price,target,params,duty,
        )
    e=rows["E"];es=rows["E_plus_S"]
    saving=e["source_modelled_nominal_original_year_wholesale_eur"]-\
           es["source_modelled_nominal_original_year_wholesale_eur"]
    lo=e["source_reported_solver_cost_lower_bound_eur"]-\
       es["source_modelled_nominal_original_year_wholesale_eur"]
    hi=e["source_modelled_nominal_original_year_wholesale_eur"]-\
       es["source_reported_solver_cost_lower_bound_eur"]
    need(lo-.02<=saving<=hi+.02 and
         abs(e["independent_annual_delivered_H2_kg"]-
             es["independent_annual_delivered_H2_kg"])<=.005,
         "original source E/ES cost bound or fixed delivered hourly H2 no longer matched")
    return {
        "schema_version":SCHEMA,
        "source_year":year,"capacity_semantics":mode,
        "source_year_UTC_hours":len(wind),
        "source_original_four_case_public_Git_blob_sha1":SOURCE_PUBLISHED_GIT_BLOB,
        "independent_LP_screen_bytes_SHA256":hashlib.sha256(lpbytes).hexdigest(),
        "original_price_f64_SHA256":metadata_common["source_original_price_SHA256"],
        "original_wind_electric_power_f64_SHA256":metadata_common["source_original_wind_SHA256"],
        "counterfactual_wind_090_f64_SHA256":metadata_common["source_stressed_wind_SHA256"],
        "exogenous_fixed_hourly_hydrogen_service_f64_SHA256":
            metadata_common["exogenous_H2_hourly_SHA256"],
        "matched_exogenous_hydrogen_service_tonnes_day":H2_TPD,
        "matched_exogenous_service_annual_H2_kg":float(np.sum(target)),
        "source_original_E_selected_max_H2_tonnes_day":float(selected[0])*24./1000.,
        "E_and_ES_fully_independent_primal_mass_electricity_EOS_market_replay":True,
        "case_results":rows,
        "matched_service_modelled_wholesale_E_minus_ES_saving_source_eur":saving,
        "matched_service_source_solver_reported_savings_lower_upper_eur":[lo,hi],
        "matched_service_modelled_saving_eur_per_kg_H2":saving/float(np.sum(target)),
        "original_source_year_eur_not_inflation_adjusted":True,
        "cost_lower_bound_source_reported_NOT_independent_dual_reconstruction":True,
        "actual_industrial_client_service_50t_day_unfulfilled":True,
        "actual_site_or_manufacturer_or_BAFU_LCIA_or_scientific_v1_0_certified":False,
        "original_hourly_provider_arrays_or_solver_witnesses_in_public":False,
    }


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--year",type=int,choices=(2022,2024),required=True)
    p.add_argument("--mode",choices=("max_inventory","usable_service"),required=True)
    p.add_argument("--private-root",type=Path,required=True)
    p.add_argument("--public-source",type=Path,required=True)
    p.add_argument("--lp-screen",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args(argv)
    result=independent_review(args.year,args.mode,args.private_root,
                              args.public_source,args.lp_screen)
    need(args.output.parent.is_dir() and not args.output.is_symlink(),
         "existing research/public original-year results directory required")
    body=json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n"
    need(not args.output.exists() or (args.output.is_file() and
         args.output.read_text(encoding="utf-8")==body),
         "existing reviewed source E/ES exogenous result differs, refuse overwrite")
    if not args.output.exists():
        with args.output.open("x",encoding="utf-8",newline="\n") as handle:
            handle.write(body)
    print("PTXLENS_INDEPENDENT_EXOGENOUS_H30_W090_SOURCE_E_AND_ES_REPLAY_PASS",
          args.year,args.mode,
          "same hourly H2 and 20–200bar EOS; source reported cost optimizer bounds only; no vendor/BAFU/site v1")


if __name__=="__main__":
    main()
