"""F3-D strict analytical WIND POWER availability necessary-condition threshold.

This is a reproducible, scalar-only analysis of source-registered 2022/2024
hourly wind electrical availability and the ORIGINAL identical hourly H2
service.  No new MILPs, raw market/weather vectors, or private hourly primal
witnesses are published.

The necessary energy/storage inequality over every contiguous interval is:
 sum(H2_required) <= H2_yield * sum(min(PEM_max_MW, wind*k + grid_max_MW))
                     + bank_inventory_swing.
A violation PROVES source-model E infeasibility. A nonviolation NEVER proves
feasibility or an optimal dispatch. We bracket only the transition of this
specific inequality's strongest interval cut. Actual integer feasibility
may require a greater wind factor. Original E at k=1 is independently
physically replayed and model-feasible for the original source record.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from .f3d_source_year_independent_cost_lp_dual import (
    check_private_source, SOURCE_PUBLISHED_GIT_BLOB
)
from .f3d_wind_reduction_independent_feasibility import (
    necessary_interval_deficit, source_f64_vector_hash, SCHEMA as INDEPENDENT_FEASIBILITY_SCHEMA
)
from .f3d_external_year_private_witness_replay import expected_params,need

SCHEMA="ptxlens.f3d_analytic_original_H2_source_wind_power_feasibility_lower_bound.v1"
VARIANT="wind_power_090"
STEPS=32


def scan_interval_factor(original_wind_power, target_hourly, model, pressure_duty,
                         *, factor):
    """Apply k to wind ELECTRIC power, not weather wind speed."""
    need(type(factor) in (float,int) and math.isfinite(factor) and
         0 <= factor <= 1, "only original-source wind power fractions 0..1 supported")
    wind=np.asarray(original_wind_power,dtype=np.float64)
    target=np.asarray(target_hourly,dtype=np.float64)
    need(wind.ndim==1 and target.shape==wind.shape and
         len(wind)>1 and np.isfinite(wind).all() and np.isfinite(target).all(),
         "source wind and fixed H2 target must be finite 1-D matching vectors")
    return necessary_interval_deficit(
        (wind*float(factor)), target, model,pressure_duty)


def necessary_cut_threshold(original_wind_power,target_hourly,model,pressure_duty,
                             *,low=.90,high=1.,steps=STEPS):
    """Bracket wind k where strongest *necessary* interval cut stops proving no-E.

    Every factor <= verified lower failing k violates an actual
    conservative source-model necessary constraint due to monotonicity.
    Every k >= first nonviolating upper k is merely NOT ruled out by
    this particular cut; the original integer model still might be infeasible.
    A known separately validated k=1 source integer feasible dispatch is
    required before claiming an actual physical-model feasibility bracket.
    """
    need(type(steps) is int and 1<=steps<=48,
         "analytical cut bisection iterations must be 1..48")
    need(type(low) in (float,int) and type(high) in (float,int) and
         math.isfinite(low) and math.isfinite(high) and 0<low<high<=1.,
         "registered observed-year wind power threshold must use 0<low<high<=1")
    left=scan_interval_factor(
        original_wind_power,target_hourly,model,pressure_duty,factor=float(low))
    right=scan_interval_factor(
        original_wind_power,target_hourly,model,pressure_duty,factor=float(high))
    need(left["simple_energy_interval_necessary_condition_violated"] is True,
         "initial reduced-wind necessary-condition inequality did not prove infeasibility")
    need(right["simple_energy_interval_necessary_condition_violated"] is False,
         "original full-wind source reference unexpectedly violates necessary inequality")
    lo=float(low);hi=float(high)
    for _ in range(steps):
        mid=(lo+hi)/2.
        probe=scan_interval_factor(
            original_wind_power,target_hourly,model,pressure_duty,factor=mid)
        if probe["simple_energy_interval_necessary_condition_violated"]:
            lo=mid;left=probe
        else:
            hi=mid;right=probe
    need(lo<hi and
         left["simple_energy_interval_necessary_condition_violated"] is True and
         right["simple_energy_interval_necessary_condition_violated"] is False,
         "analytical constraint threshold bracket broken or stalled numerically")
    return {
        "method":"monotone bisection of exact source-hourly generous PEM/wind/grid/storage necessary H2 energy inequality",
        "lower_factor_at_which_energy_storage_inequality_still_PROVES_infeasible":lo,
        "first_higher_factor_at_which_inequality_NO_LONGER_PROVES_infeasible":hi,
        "analytical_necessary_condition_boundary_factor_bracket_width":hi-lo,
        "source_E_integer_feasible_reference_wind_factor_proven_elsewhere":float(high),
        "actual_E_MILP_feasibility_transition_factor_verified":None,
        "actual_E_MILP_feasible_threshold_must_exceed_analytical_failing_lower_factor":True,
        "independent_new_full_year_MILP_or_dual_solved":False,
        "lower_end_violating_interval_start_UTC_hour_index":
            left["violating_interval_start_UTC_hour_index"],
        "lower_end_violating_interval_end_exclusive_UTC_hour_index":
            left["violating_interval_end_exclusive_UTC_hour_index"],
        "lower_end_analytical_energy_balance_violation_kg":
            left["max_interval_deficit_minus_available_inventory_kg"],
        "upper_end_analytical_energy_balance_violation_kg":
            right["max_interval_deficit_minus_available_inventory_kg"],
        "nonviolation_at_upper_factor_does_not_prove_MILP_feasibility":True,
        "wind_is_model_electric_POWER_not_meteorological_wind_speed":True,
    }


def validate_original_review(year,mode,independent_report,original_wind,target):
    original=independent_report
    need(type(original) is dict and
         original.get("schema_version")==INDEPENDENT_FEASIBILITY_SCHEMA and
         original.get("year")==year and
         original.get("capacity_semantics")==mode and
         original.get("original_4_case_public_Git_blob_sha1")==SOURCE_PUBLISHED_GIT_BLOB,
         "wrong original independent E/E+S low-wind result or source revision")
    need(original.get("independent_reconstruction_reports_E_LP_infeasible") is True and
         original.get("independent_EplusS_feasible_full_year_original_primal_replay_passed") is True and
         original.get("paired_E_minus_EplusS_cost_saving_eur") is None and
         original.get("original_source_model_E_infeasible_EplusS_feasible_under_fixed_hourly_H2") is True and
         original.get("real_site_physical_infeasibility_certified") is False,
         "do not infer wind factor threshold from an unconfirmed low-wind reference")
    need(original.get("original_observed_wind_float64_SHA256")==
         source_f64_vector_hash(original_wind) and
         original.get("same_frozen_hourly_hydrogen_service_float64_SHA256")==
         source_f64_vector_hash(target) and
         original.get("counterfactual_wind_model_electric_power_float64_SHA256")==
         source_f64_vector_hash(np.asarray(original_wind,dtype=float)*.9),
         "original historical source wind or target arrays do not match independent 0.9 study")
    observed=original["analytical_energy_storage_interval"]
    need(observed.get("simple_energy_interval_necessary_condition_violated") is True,
         "independent low-wind original interval analytic proof not accepted")
    return observed


def summarize(year,mode,original_wind,target,model,duty,independent_report):
    observed=validate_original_review(year,mode,independent_report,original_wind,target)
    original_90=scan_interval_factor(original_wind,target,model,duty,factor=.90)
    for key in ("max_contiguous_net_H2_deficit_kg_under_generous_PEM_power_upper_bound",
                "physical_bank_inventory_swing_upper_limit_kg",
                "max_interval_deficit_minus_available_inventory_kg"):
        need(abs(original_90[key]-observed[key])<1e-5,
             "source 0.90 low-wind analytical H2 bound changed since independent review")
    need(original_90["violating_interval_start_UTC_hour_index"]==
         observed["violating_interval_start_UTC_hour_index"] and
         original_90["violating_interval_end_exclusive_UTC_hour_index"]==
         observed["violating_interval_end_exclusive_UTC_hour_index"],
         "same original violation interval unexpectedly moved")
    n=len(original_wind)
    need(n==({2022:8760,2024:8784}[year]) and mode in ("max_inventory","usable_service"),
         "original wind power calendar or capacity mode changed")
    first=int(original_90["violating_interval_start_UTC_hour_index"])
    end=int(original_90["violating_interval_end_exclusive_UTC_hour_index"])
    epoch=datetime(year,1,1,tzinfo=timezone.utc)
    start_utc=(epoch+timedelta(hours=first)).isoformat().replace("+00:00","Z")
    end_utc=(epoch+timedelta(hours=end)).isoformat().replace("+00:00","Z")
    bracket=necessary_cut_threshold(
        original_wind,target,model,duty,low=.9,high=1.)
    return {
        "schema_version":SCHEMA,
        "source_evidence":"verified fixed-service original-year provider wind and independent reduced-wind feasibility report",
        "year":year,"capacity_semantics":mode,
        "UTC_hours":n,
        "source_four_case_original_Git_blob_sha1":SOURCE_PUBLISHED_GIT_BLOB,
        "original_registered_source_wind_power_float64_SHA256":
            source_f64_vector_hash(original_wind),
        "original_registered_source_fixed_hourly_H2_float64_SHA256":
            source_f64_vector_hash(target),
        "fixed_hourly_H2_service_original_reference_kg":float(target[0]),
        "fixed_annual_H2_original_reference_kg":float(np.sum(target)),
        "reduced_wind_factor_verified":.90,
        "independent_E_LP_infeasible_at_90pct_wind":True,
        "independent_EplusS_MILP_full_hourly_witness_feasible_at_90pct_wind":True,
        "independently_REPRODUCED_90pct_energy_storage_interval":original_90,
        "90pct_proof_interval_start_UTC_inclusive":start_utc,
        "90pct_proof_interval_end_UTC_exclusive":end_utc,
        "90pct_proof_interval_hours":end-first,
        "analytical_cut_boundary_not_actual_optimal_integer_threshold":bracket,
        "90pct_paired_wholesale_cost_saving_eur":None,
        "private_provider_or_primal_hourly_values_released":False,
        "real_world_site_reliability_vendor_or_BAFU_LCIA_verified":False,
        "scientific_v1_0_release_allowed":False,
    }


def markdown(r):
    interval=r["independently_REPRODUCED_90pct_energy_storage_interval"]
    br=r["analytical_cut_boundary_not_actual_optimal_integer_threshold"]
    lower=br["lower_factor_at_which_energy_storage_inequality_still_PROVES_infeasible"]
    upper=br["first_higher_factor_at_which_inequality_NO_LONGER_PROVES_infeasible"]
    return (
        "# F3-D: analytically certified low-wind model infeasibility and "
        "necessary-condition wind-factor boundary\n\n"
        f"Observed source year {r['year']}, {r['capacity_semantics']}. "
        "Wind availability is modelled ELECTRIC POWER, not wind speed. "
        "Original fixed hourly hydrogen service is unchanged.\n\n"
        "At 0.90 times original source wind-power availability, the original "
        "20t E case is independently rebuilt LP-infeasible and 40t E+S has "
        "an independently feasible full-year integer primal witness. "
        f"From {r['90pct_proof_interval_start_UTC_inclusive']} to "
        f"{r['90pct_proof_interval_end_UTC_exclusive']} (end excluded; "
        f"{r['90pct_proof_interval_hours']} hours), "
        "the direct generous upper bound of source H2 production plus "
        "possible discharge requires "
        f"{interval['max_contiguous_net_H2_deficit_kg_under_generous_PEM_power_upper_bound']:,.3f} "
        "kg net storage, exceeding possible inventory swing "
        f"{interval['physical_bank_inventory_swing_upper_limit_kg']:,.3f} kg "
        "by "
        f"{interval['max_interval_deficit_minus_available_inventory_kg']:,.3f} kg. "
        "This contradiction uses no optimization solver and is independent of "
        "integer commitment assumptions.\n\n"
        f"A bisection of this **necessary inequality only** brackets its "
        f"nonviolation transition in wind-power multiplier **({lower:.10f}, "
        f"{upper:.10f}]**, precision {br['analytical_necessary_condition_boundary_factor_bracket_width']:.3g}. "
        "Every factor at or below the tested violating lower bound still "
        "violates the necessary condition. The no-violation upper bound is "
        "**not** an accepted feasible annual dispatch, and the exact E MILP "
        "feasibility threshold remains UNKNOWN within the interval from "
        "this analytical cut to the separately validated original factor 1.0. "
        "Original full-wind source E is feasible, not a site-service guarantee.\n\n"
        "The E-versus-E+S cost saving at 0.9 remains **NULL**, not zero. "
        "No original provider hourly arrays, private dispatch or native BAFU "
        "inventories were redistributed; complete manufacturer/system "
        "engineering, site performance, financial viability, dual/Farkas "
        "certificates and programme scientific v1.0 remain UNVERIFIED.\n"
    )


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--year",required=True,type=int,choices=(2022,2024))
    p.add_argument("--mode",required=True,choices=("max_inventory","usable_service"))
    p.add_argument("--private-root",required=True,type=Path)
    p.add_argument("--public-source",required=True,type=Path)
    p.add_argument("--independent-90pct-report",required=True,type=Path)
    p.add_argument("--output-dir",required=True,type=Path)
    a=p.parse_args(argv)
    check_report=a.independent_90pct_report
    need(check_report.is_file(),"independent source-year wind reduced feasibility report missing")
    raw=check_report.read_bytes()
    check=json.loads(raw.decode("utf-8"))
    published,witness,wind,price,target=check_private_source(
        a.year,a.mode,a.private_root,a.public_source)
    mode_original=witness["cases"]["E"]["Type_I_200bar_model_pressure_duty"]
    model=expected_params(20000)
    result=summarize(a.year,a.mode,wind,target,model,mode_original,check)
    result["source_independently_rebuilt_90pct_report_SHA256"]=hashlib.sha256(raw).hexdigest()
    need(a.output_dir.is_dir() and not a.output_dir.is_symlink(),
         "existing public scientific results output folder required")
    stem=f"F3D_WIND_090_{a.year}_{a.mode}_ANALYTIC_FEASIBILITY_FACTOR_LOWER_BOUND_v1"
    outputs=[
      (a.output_dir/(stem+".json"),
       json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n"),
      (a.output_dir/(stem+".md"),markdown(result)),
    ]
    for path,payload in outputs:
        need(not path.exists() or (path.is_file() and not path.is_symlink()
             and path.read_text(encoding="utf-8")==payload),
             "source scientific public report exists but differs; refuse overwrite")
    for path,payload in outputs:
        if not path.exists():
            with path.open("x",encoding="utf-8",newline="\n") as writer:
                writer.write(payload)
    br=result["analytical_cut_boundary_not_actual_optimal_integer_threshold"]
    print("F3D_WIND_ANALYTIC_NECESSARY_CUT_BOUND_FROM_SOURCE_RESULTS",
          a.year,a.mode,
          "wind-factor analytically infeasible to",
          br["lower_factor_at_which_energy_storage_inequality_still_PROVES_infeasible"],
          "next nonviolating necessary inequality from",
          br["first_higher_factor_at_which_inequality_NO_LONGER_PROVES_infeasible"],
          "REAL E MILP THRESHOLD NOT YET COMPUTED; NO vendor/BAFU/site/v1")


if __name__=="__main__":
    main()
