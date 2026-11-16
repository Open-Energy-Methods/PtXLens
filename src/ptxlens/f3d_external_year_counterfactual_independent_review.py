"""Independent PRIVATE PtXLens replay of F3-D 2022/2024 controlled stresses.

Reads no original private source data from Git; independently reconstructs
controlled price/wind transformations and E/E+S physical balances from each
PRIVATE PtXFlex solver primal. Only after both scenario members are reviewed
does it emit an allowlisted PUBLIC per-pair economic aggregate. No fake price
effect estimate is produced when wind changes make fixed H2 delivery infeasible.
The original producer-reported HiGHS dual cost bound is NOT independently proven.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import statistics
from pathlib import Path

import numpy as np

from .f3d_external_year_independent_review import check_result,YEAR_HOURS
from .f3d_external_year_private_witness_replay import (
    f64_hash,read_private_year_csv,replay_equations,verify_eos,
    review_private_witness,expected_params,need,
)

SCHEMA="ptxlens.f3d_controlled_original_year_private_pair_independent_primal_replay.v1"
PRIVATE_SOURCE_SCHEMA="ptxflex.f3d_private_source_year_counterfactual_exact_dispatch.v1"
SOURCE_GIT_BLOB="ca07f5ef1e381fa157982bc5a68e46ce3022003a"
MODEL_FARM_POWER_CAP_MW=125.685
MODES=("max_inventory","usable_service")
STRESSES=("price_roll_168h","price_spread_150pct","wind_power_090","wind_power_110_capped")


def transformed(price,wind,variant):
    """A logically separate transformation of observed original price/wind lists."""
    need(variant in STRESSES,"unregistered price/wind intervention")
    need(len(price)==len(wind) and len(price)>=2 and
         all(math.isfinite(x) for x in price+wind) and
         all(0<=x<=MODEL_FARM_POWER_CAP_MW+1e-8 for x in wind),
         "invalid original market/weather arrays")
    if variant=="price_roll_168h":
        need(len(price)>168,"168h chronological shift needs full observed UTC year")
        return price[-168:]+price[:-168],list(wind)
    if variant=="price_spread_150pct":
        median=statistics.median(price)
        return [float(median+1.5*(x-median)) for x in price],list(wind)
    if variant=="wind_power_090":
        return list(price),[float(x*.9) for x in wind]
    return list(price),[min(float(x*1.1),MODEL_FARM_POWER_CAP_MW) for x in wind]


def _source_public(original,year,mode):
    raw=Path(original).read_bytes().replace(b"\r\n",b"\n")
    git_hash=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    need(git_hash==SOURCE_GIT_BLOB,
         "public verified original F3-D source data Git blob SHA mismatch")
    data=json.loads(raw.decode("utf-8"))
    need(data["schema_version"]==
         "oem.ptx.f3d_2022_2024_public_source_aggregate_independent_replay.v1" and
         data.get("scientific_v1_0_release_allowed") is False and
         data.get("independent_solver_dual_certificates_recomputed") is False,
         "original observed-year source scope changed")
    matches=[x for x in data.get("cases",[]) if x.get("year")==year and
             x.get("storage_capacity_semantics")==mode]
    need(len(data.get("cases",[]))==4 and len(matches)==1,
         "full original source-year four-case verified bundle required")
    return matches[0]


def independent_pair(year,mode,variant,private_root,original_public):
    need(year in YEAR_HOURS and mode in MODES and variant in STRESSES,
         "unsupported source year, pressure semantics or controlled intervention")
    original=_source_public(original_public,year,mode)
    private=Path(private_root).resolve(strict=True)
    need(private.name=="PtX_PRIVATE_RESEARCH" and private.is_dir(),
         "original data must remain in approved private research directory")
    report_file=private/"results"/f"F3D_ARCO_{year}_{mode}.json"
    original_primal_file=private/"results"/f"PRIVATE_F3D_ARCO_{year}_{mode}_primal.json"
    source_prices=private/f"price-{year}"/"normalized_UTC_price.csv"
    source_wind=private/f"wind-arco-{year}"/"normalized_UTC_wind.csv"
    baseline=check_result(json.loads(report_file.read_text(encoding="utf-8")))
    need(baseline["year"]==year and baseline["capacity_semantics"]==mode and
         baseline["source_price_SHA256"]==original["source_year_price_f64_sha256"] and
         baseline["source_wind_SHA256"]==original["source_year_wind_f64_sha256"],
         "original private report does not match original published public reviewer")
    source_price=read_private_year_csv(source_prices,year,"day_ahead_eur_mwh")
    source_w=read_private_year_csv(source_wind,year,"wind_available_mw",nonnegative=True)
    need(f64_hash(source_price)==original["source_year_price_f64_sha256"] and
         f64_hash(source_w)==original["source_year_wind_f64_sha256"],
         "private original 2022/2024 provider series no longer matches published SHA")
    # Confirm original four-case baseline has the same immutable physical H2
    # product and independent source primal proof BEFORE reading a perturbation.
    rereview=review_private_witness(original_primal_file,report_file,
                                   source_prices,source_wind)
    need(rereview["E_source_year_E_and_ES_full_hourly_primal_mass_energy_cost_recomputed"] is True and
         rereview["20_200bar_CoolProp_independent_EOS_extrema_recomputed"] is True,
         "original independently source-replayed 2022/2024 baseline missing")
    original_primal=json.loads(original_primal_file.read_text(encoding="utf-8"))
    target=original_primal["target_hourly_kg"]
    need(len(target)==YEAR_HOURS[year] and
         f64_hash(target)==original["price_neutral_E_uniform_hydrogen_service"]["hourly_target_f64_sha256"],
         "counterfactual cannot change original price-blind hydrogen functional unit")
    altered_price,altered_wind=transformed(source_price,source_w,variant)
    psha=f64_hash(altered_price);wsha=f64_hash(altered_wind)
    common={
        "original_year":year,"mode":mode,"variant":variant,
        "source_original_price_SHA256":f64_hash(source_price),
        "source_original_wind_SHA256":f64_hash(source_w),
        "source_original_selected_H2_SHA256":f64_hash(target),
        "counterfactual_price_SHA256":psha,
        "counterfactual_wind_SHA256":wsha,
        "original_public_aggregate_Git_blob_sha1":SOURCE_GIT_BLOB,
        "source_original_baseline_modelled_saving_eur":
            original["matched_service_annual_operational_savings_nominal_eur"],
        "source_original_service_kg":float(np.sum(target)),
        "source_wind_model_power_limit_mw":MODEL_FARM_POWER_CAP_MW,
    }
    result_cases={}
    for case,capacity in (("E",20000),("E_plus_S",40000)):
        path=private/"results"/"counterfactuals"/f"PRIVATE_F3D_CF_{year}_{mode}_{variant}_{case}.json"
        need(path.is_file(),"private counterfactual producer case is not solved/saved: "+case)
        record=json.loads(path.read_text(encoding="utf-8"))
        need(record.get("schema_version")==PRIVATE_SOURCE_SCHEMA and
             record.get("metadata")==common and record.get("scenario")==case and
             record.get("native_BAFU_or_vendor_or_v1_release") is False and
             record.get("original_provider_hourly_arrays_NOT_redistributed") is True and
             record.get("independent_model_dual_certificate_replayed") is False,
             "private stress source provenance does not match independent reconstruction")
        if record.get("outcome")=="LP_RELAXATION_INFEASIBLE_FIXED_H2_NO_COST_RESULT":
            need(variant.startswith("wind_") and
                 record.get("modelled_counterfactual_cost_eur") is None and
                 record.get("LP_zero_objective_infeasible_HiGHS_status_2") is True,
                 "price-only experiment cannot be declared LP-infeasible without independent proof")
            result_cases[case]={
                "status":"SOURCE_SOLVER_REPORTED_LP_INFEASIBLE_NO_COST",
                "independent_LP_infeasibility_certificate_reconstructed":False,
                "source_model_cost_eur":None,
            }
            continue
        need(record.get("outcome")==
             "ORIGINAL_FULL_YEAR_MILP_PRIMAL_SOLVER_BOUND_CERTIFIED_LOCAL_NOT_EXTERNAL_DUAL",
             "incomplete counterfactual source MILP cannot imply economic saving")
        states=record.get("source_original_model_8field_primal_witness")
        duty=original_primal["cases"][case]["Type_I_200bar_model_pressure_duty"]
        p=expected_params(capacity)
        need(duty.get("capacity_semantics")==mode and
             duty.get("scenario_capacity_kg")==capacity,
             "source pressure/station interpretation changed across stress")
        audit=replay_equations(states,target,altered_wind,altered_price,p,duty)
        eos=verify_eos(duty,audit["minimum_source_bank_model_kg"],
                       audit["maximum_source_bank_model_kg"])
        need(eos["independent_313K_CoolProp_Hydrogen_EOS_recomputed"] is True,
             "independent pressure EOS audit missing")
        cost=record["modelled_counterfactual_cost_eur"]
        lb=record["solver_reported_cost_lower_bound_eur"]
        gap=record["solver_reported_mip_relative_gap"]
        need(type(cost) in (int,float) and type(lb) in (int,float) and
             all(math.isfinite(float(v)) for v in (cost,lb,gap)) and
             0<=gap<=1e-6 and lb<=cost+.10,
             "original source solver cost bound not independently arithmetic admissible")
        need(abs(audit["independent_source_year_signed_grid_cost_eur"]-cost)<=.05 and
             abs(audit["modelled_annual_hydrogen_kg"]-
                 record["source_case_modelled_annual_kg_H2"])<=.005 and
             audit["hourly_states_sha256"]==record["source_original_primal_f64_sha256"]==
             record["pressure_and_conservation_original_source_model_audit"]["source_hourly_dispatch_float64_sha256"],
             "independent full-hour mass/electricity/cost/private witness inconsistent")
        result_cases[case]={
            "status":"INDEPENDENT_FULL_YEAR_PRIMAL_AND_PRESSURE_COST_REPLAY_PASSED",
            "source_model_cost_eur":cost,
            "source_reported_cost_lower_bound_eur":lb,
            "source_reported_MIP_relative_gap":gap,
            "independent_hourly_primal_SHA256":audit["hourly_states_sha256"],
            "independent_max_mass_power_inventory_error":
                max(audit["maxima"].values()),
            "independent_pressure_min_bar_absolute":eos["min_bar_absolute"],
            "independent_pressure_max_bar_absolute":eos["max_bar_absolute"],
            "source_original_hourly_primal_NOT_in_public_report":True,
        }
    e=result_cases["E"];s=result_cases["E_plus_S"]
    both=(e["status"]=="INDEPENDENT_FULL_YEAR_PRIMAL_AND_PRESSURE_COST_REPLAY_PASSED" and
          s["status"]=="INDEPENDENT_FULL_YEAR_PRIMAL_AND_PRESSURE_COST_REPLAY_PASSED")
    saving=None;interval=None
    if both:
        saving=e["source_model_cost_eur"]-s["source_model_cost_eur"]
        low=e["source_reported_cost_lower_bound_eur"]-s["source_model_cost_eur"]
        high=e["source_model_cost_eur"]-s["source_reported_cost_lower_bound_eur"]
        need(low<=saving+1e-3<=high+1e-3,
             "pair E minus E+S source solver bound interval invalid")
        interval=[low,high]
    return {
        "schema_version":SCHEMA,"year":year,"mode":mode,"variant":variant,
        "source_calendar_hours":YEAR_HOURS[year],
        "source_market_year_nominal_eur_not_inflation_adjusted":True,
        "reference_original_public_four_case_Git_blob_sha1":SOURCE_GIT_BLOB,
        "original_provider_price_f64_SHA256":common["source_original_price_SHA256"],
        "original_provider_wind_f64_SHA256":common["source_original_wind_SHA256"],
        "counterfactual_price_f64_SHA256":psha,
        "counterfactual_wind_power_f64_SHA256":wsha,
        "fixed_original_price_blind_E_hydrogen_service_f64_SHA256":f64_hash(target),
        "fixed_hydrogen_same_hour_kg_year":float(np.sum(target)),
        "control_change":"one predeclared observed-year price OR modeled wind-output transformation; not a future market forecast",
        "cases":result_cases,
        "paired_E_minus_EplusS_nominal_operational_saving_eur":saving,
        "paired_source_solver_reported_bound_interval_eur":interval,
        "economic_result_null_if_any_unverified_or_infeasible":not both,
        "physical_original_full_year_primal_replay_passed_for_both":both,
        "independent_cost_dual_or_LP_infeasibility_proof_completed":False,
        "measured_site_or_manufacturer_or_BAFU_or_v1_0_validated":False,
        "original_private_hourly_market_wind_H2_and_primal_arrays_NOT_in_public":True,
    }

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--year",type=int,choices=sorted(YEAR_HOURS),required=True)
    p.add_argument("--mode",choices=MODES,required=True)
    p.add_argument("--variant",choices=STRESSES,required=True)
    p.add_argument("--private-root",type=Path,
                   default=Path.home()/"PtX_PRIVATE_RESEARCH")
    p.add_argument("--public-source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args(argv)
    out=Path(args.output)
    need(out.parent.is_dir() and not out.is_symlink(),
         "destination must be existing publicly-reviewed directory")
    record=independent_pair(args.year,args.mode,args.variant,
                            args.private_root,args.public_source)
    body=json.dumps(record,sort_keys=True,indent=2,allow_nan=False)+"\n"
    need(not out.exists() or (out.is_file() and
         out.read_text(encoding="utf-8")==body),
         "existing source-reviewed aggregate cannot be overwritten")
    if not out.exists():
        with out.open("x",encoding="utf-8",newline="\n") as fp:fp.write(body)
    print("PTXLENS_F3D_CF_SOURCE_YEAR_INDEPENDENT_PRIMAL_REPLAY_DONE "
          f"{args.year} {args.mode} {args.variant}; "
          "infeasible or noncertified paired cash result always null; no dual/v1 claims")

if __name__=="__main__":
    main()
