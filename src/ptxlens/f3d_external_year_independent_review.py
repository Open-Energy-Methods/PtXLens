"""Independent F3-D metadata/arithmetic review of source-year E/E+S result.

This is intentionally NOT a second solver, a source-original array replay,
a plant measurement audit or a native full BAFU impact assessment.
It checks declared source hashes, year-length, exact equality of H2 service
SHA between E and E+S, uniform-demand arithmetic, HiGHS primal/dual bound
inequalities and explicit non-release semantics. Requires both capacity
interpretations separately; does not pool unlike H2-service quantities.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import struct

SCHEMA="ptxflex.f3d_2022_2024_equal_hourly_model_service_pressure_screening.v1"
REVIEW="ptxlens.f3d_external_year_independent_metadata_financial_scope_review.v1"
SEL="ptxflex.f3d_E_price_blind_maximum_uniform_H2_service.v1"
YEAR_HOURS={2022:8760,2024:8784}
MODES=("max_inventory","usable_service")
E_SHA="069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051"
ES_SHA="cd4101fe62c3f1b8aa2d7508d3651d2fee40d2bafe6d5b87e40d5f4d055070f9"
EPS=1e-6


class ExternalYearReviewError(ValueError):
    pass


def need(test,why):
    if not test:raise ExternalYearReviewError("PtXLens F3-D: "+why)


def finite(x):
    return type(x) in (int,float) and math.isfinite(x)


def _float64_target_hash(flat_hourly_h2_kg,hours):
    # Source PtXFlex reports float64 in little-endian, one uniform source H2
    # target per UTC hour, including 29 February in leap year.
    val=struct.pack("<d",flat_hourly_h2_kg)
    return hashlib.sha256(val*hours).hexdigest()


def check_result(record):
    need(isinstance(record,dict) and record.get("schema_version")==SCHEMA,
         "unknown model report format")
    year=record.get("year")
    mode=record.get("capacity_semantics")
    need(type(year) is int and year in YEAR_HOURS and mode in MODES,
         "year or storage semantics invalid")
    hours=YEAR_HOURS[year]
    need(record.get("year_UTC_hours")==hours,
         "wrong 2022/2024 UTC calendar duration or missing 2024 leap day")
    need(record.get("original_source_E_zip_SHA256")==E_SHA and
         record.get("original_source_ES_zip_SHA256")==ES_SHA,
         "different original PyNEXUS plant configuration")
    need(record.get("provider_pair_source_2023_reconstruction_and_calendar_verified") is True and
         record.get("source_A44_and_ERA5_provider_original_files_held_private") is True,
         "source-pair admission metadata absent")
    ph=record.get("source_year_price_f64_sha256")
    wh=record.get("source_year_wind_f64_sha256")
    need(all(isinstance(x,str) and len(x)==64 and
             all(c in "0123456789abcdef" for c in x) for x in (ph,wh)),
         "source hash absent or not hex-encoded SHA256")
    selected=record.get("E_price_blind_identical_model_H2_service_selection")
    need(isinstance(selected,dict) and selected.get("schema_version")==SEL and
         selected.get("year")==year and selected.get("testing_only") is False and
         selected.get("E_binary_price_neutral_feasible") is True and
         selected.get("source_E_pressure_screen_only") is True,
         "non-physical or synthetic service selector cannot certify observed year")
    alpha=selected.get("selected_fraction_50t_per_day")
    ub=selected.get("certified_fraction_upper_bound")
    gap=selected.get("E_price_neutral_mip_relative_gap")
    need(all(finite(x) for x in (alpha,ub,gap)) and
         0<alpha<=1+1e-8 and alpha<=ub+1e-7 and
         ub<=1+1e-2 and 0<=gap<=1e-6,
         "price-neutral maximal H2 service not integer-bound certified")
    expected_h2_per_hour=(50000./24.)*alpha
    expected_annual=hours*expected_h2_per_hour
    need(finite(selected.get("modelled_E_flat_h2_service_kg_per_hour")) and
         abs(selected["modelled_E_flat_h2_service_kg_per_hour"]-expected_h2_per_hour)<1e-8 and
         finite(selected.get("modelled_E_annual_h2_service_kg")) and
         abs(selected["modelled_E_annual_h2_service_kg"]-expected_annual)<0.005 and
         selected.get("original_nominal_h2_demand_kg")==hours*(50000./24.),
         "annual delivery vs 50 tonne/day leap-year contract reconciliation failed")
    target_hash=_float64_target_hash(expected_h2_per_hour,hours)
    need(selected.get("selected_h2_target_float64_sha256")==target_hash,
         "year-specific constant hourly target vector hash differs")
    need(finite(selected.get("E_price_neutral_physical_residual_max")) and
         selected["E_price_neutral_physical_residual_max"]<=2e-4,
         "E source-year service physical residual exceeds tolerance")
    costs={}
    for case in ("E","E_plus_S"):
        c=record.get(case)
        need(isinstance(c,dict),"missing "+case+" source case")
        need(c.get("modelled_hourly_H2_service_sha256")==target_hash and
             finite(c.get("modelled_annual_hydrogen_kg")) and
             abs(c["modelled_annual_hydrogen_kg"]-expected_annual)<0.005,
             case+" did not deliver the exact same hour-for-hour H2 target")
        upper=c.get("modelled_cost_eur_in_source_calendar_not_inflation_adjusted")
        lower=c.get("solver_cost_lower_bound_eur")
        g=c.get("mip_relative_gap")
        need(all(finite(v) for v in (upper,lower,g)) and 0<=g<=1e-6 and
             lower<=upper+0.1,
             case+" wholesale objective not bounded by certified HiGHS dual")
        need(finite(c.get("max_independent_residual")) and
             c["max_independent_residual"]<=2e-4 and
             c.get("not_actual_industrial_operation") is True,
             case+" modelled mass-energy closure / source scope invalid")
        pressure=c.get("pressure_EOS_screen_bounds")
        need(isinstance(pressure,dict) and
             pressure.get("EOS_hourly_mass_bounds_imply_pressure_limits") is True and
             pressure.get("temperature_k_is_fixed_screening_assumption") is True,
             case+" 20-200bar source physical screen missing")
        need(all(finite(c.get(k)) and c[k]>=-EPS for k in
                 ("modelled_grid_import_mwh","modelled_grid_export_mwh",
                  "modelled_compressor_electricity_mwh","modelled_hydrogen_storage_peak_kg")),
             case+" incomplete gas/electric source annual metrics")
        costs[case]=(upper,lower)
    calc_saving=costs["E"][0]-costs["E_plus_S"][0]
    calc_low=costs["E"][1]-costs["E_plus_S"][0]
    calc_high=costs["E"][0]-costs["E_plus_S"][1]
    bounds=record.get("solver_difference_guaranteed_lower_upper_interval_eur")
    need(finite(record.get("cost_savings_E_minus_EplusS_source_calendar_nominal_eur")) and
         abs(record["cost_savings_E_minus_EplusS_source_calendar_nominal_eur"]-calc_saving)<0.01 and
         isinstance(bounds,list) and len(bounds)==2 and all(finite(x) for x in bounds) and
         abs(bounds[0]-calc_low)<0.01 and abs(bounds[1]-calc_high)<0.01 and
         calc_low-0.01<=calc_saving<=calc_high+0.01,
         "cost savings claim outside independently recomputed HiGHS primal/dual bounds")
    need(record.get("mathematically_matched_exact_same_modelled_hourly_H2_target") is True and
         record.get("actual_industrial_H2_delivery_or_independent_measurements") is False and
         record.get("vendor_200bar_compressor_and_storage_station_BOM_verified") is False and
         record.get("native_BAFU_whole_plant_GWP_verified") is False and
         record.get("installed_plant_LCOH_or_investment_DCF_certified") is False and
         record.get("independent_external_scientific_peer_review_completed") is False and
         record.get("v1_0_scientific_release_allowed") is False and
         record.get("no_provider_price_wind_or_dispatch_hourly_arrays_in_report") is True and
         record.get("energy_year_2022_and_2024_eur_not_yet_inflation_normalized") is True,
         "external-year report promotes unsupported supplier/LCA/DCF/v1 claims")
    return {
        "year":year,"capacity_semantics":mode,
        "year_UTC_hours_verified_by_metadata":hours,
        "same_hourly_modelled_H2_service_float64_SHA256":target_hash,
        "selected_fraction_50t_per_day":alpha,
        "annual_modelled_hydrogen_kg":expected_annual,
        "source_price_SHA256":ph,"source_wind_SHA256":wh,
        "paired_operational_savings_2022_or_2024_nominal_eur":calc_saving,
        "recalculated_solver_error_bound_eur":[calc_low,calc_high],
        "metadata_arithmetic_model_scope_review_passed":True,
        "independent_source_NetCDF_XML_or_dispatch_primal_replay_completed":False,
        "native_whole_plant_LCA_TEA_v1_0_passed":False,
    }


def review_four_cases(files):
    need(len(files)==4,"require BOTH years and BOTH storage capacity interpretations")
    cases={}
    for file in files:
        report=check_result(json.loads(Path(file).read_text(encoding="utf-8")))
        key=(report["year"],report["capacity_semantics"])
        need(key not in cases,"duplicated source-year/mode report")
        cases[key]=report
    need(set(cases)=={(y,m) for y in YEAR_HOURS for m in MODES},
         "missing leap-year or one physical storage interpretation")
    for year in YEAR_HOURS:
        gross=cases[(year,"max_inventory")]
        usable=cases[(year,"usable_service")]
        need(gross["source_price_SHA256"]==usable["source_price_SHA256"] and
             gross["source_wind_SHA256"]==usable["source_wind_SHA256"],
             "same historical year has unmatched original provider price/wind between mode cases")
    return {
        "schema_version":REVIEW,
        "source_years_reviewed":[2022,2024],
        "year_mode_count":len(cases),
        "no_cross_capacity_semantics_service_parity_claim":True,
        "no_inflation_or_exchange_conversion_applied":True,
        "source_data_and_original_dispatch_witnesses_NOT_independently_replayed":True,
        "all_four_scenario_metadata_financial_source_scope_gates_passed":True,
        "original_source_lca_tea_safety_and_v1_0_still_blocked":True,
        "cases":[cases[k] for k in sorted(cases)],
    }


def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("--files",required=True,nargs=4)
    ap.add_argument("--output",required=True)
    a=ap.parse_args(argv)
    output=Path(a.output)
    need(not output.exists(),"do not overwrite reviewer result")
    r=review_four_cases(a.files)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(r,sort_keys=True,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print("PtXLens independently reviewed four annual metadata/finance scope records")
    print("Does not certify primary provider bytes, model physics, site, BAFU, vendor economics or v1.0")


if __name__=="__main__":
    main()
