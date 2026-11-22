"""F3-D strict 2024 public admission and reproducible 2022/2024 matched-H2 comparison.

Reuses the completed, source-Git-blob-verified NINE-file 2022 publication
admission, validates the THREE separately locally produced PUBLIC 2024 source
results, then derives immutable scalar-only two-year summaries. Never reads
PtX_PRIVATE_RESEARCH, hourly provider vectors, or private original MILP
witnesses. No 2024 data is currently in the repo until manual review/push.

This does not reinterpret nominal historical EUR as inflation-adjusted value,
does not turn two years into an uncertainty distribution, and cannot establish
vendor costs, actual project IRR, native BAFU LCIA or a scientific v1.0 claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from . import f3d_2022_public_evidence_admission as base
from .f3d_exogenous_service_lp_screen import SCHEMA as LP_SCHEMA
from .f3d_exogenous_h2_integer_independent_replay import SCHEMA as INTEGER_SCHEMA

SCHEMA="ptxlens.f3d_original_2022_2024_H30_W090_cross_year_source_economics_verified_public.v1"
YEAR=2024
MODE="max_inventory"
LP_FILE="F3D_2024_max_inventory_EXOGENOUS_H2_SOURCE_LP_FEASIBILITY_SCREEN_v1.json"
LP_MD="F3D_2024_max_inventory_EXOGENOUS_H2_SOURCE_LP_FEASIBILITY_SCREEN_v1.md"
INTEGER_FILE="F3D_EXOGENOUS_2024_max_inventory_H30_W090_BOTH_INTEGER_INDEPENDENT_REPLAY_v1.json"
THREE=(LP_FILE,LP_MD,INTEGER_FILE)
STEM="F3D_2022_2024_max_inventory_H30_W090_TWO_YEAR_MATCHED_SERVICE_ECONOMICS_v1"


def get_2024_files(root):
    """Check the THREE 2024 original-source publication candidates, not all untracked files."""
    root=Path(root)
    base.need(root.is_dir() and not root.is_symlink(),
              "original public scientific output directory missing/symlinked")
    values={}
    digest={}
    for name in THREE:
        p=root/name
        base.need(p.is_file() and not p.is_symlink() and p.parent==root,
                  "required 2024 source publication candidate missing/symlinked "+name)
        raw=p.read_bytes()
        size_limit=base.MAX_MD_BYTES if name.endswith(".md") else base.MAX_JSON_BYTES
        base.need(0<len(raw)<=size_limit and b"\x00" not in raw and b"\r" not in raw,
                  "2024 source evidence is empty, oversized, binary or not canonical LF")
        digest[name]=hashlib.sha256(raw).hexdigest()
        if name.endswith(".json"):
            data=json.loads(raw.decode("utf-8"))
            base.minimize_tree(data,stack=name)
            schema=LP_SCHEMA if name==LP_FILE else INTEGER_SCHEMA
            base.need(data.get("schema_version")==schema,
                      "2024 independent reviewer schema not source-authenticated")
            values[name]=data
        else:
            md=raw.decode("utf-8")
            base.need(
                "PRIVATE_F3D_" not in md and
                "PtX_PRIVATE_RESEARCH" not in md and
                "BEGIN PRIVATE KEY" not in md,
                "2024 markdown contains high-risk private research references")
    return values,digest


def require_reviewed_pair(year,model,annual_kg):
    """Recompute costs, savings and *source-reported* MIP bounds (not new dual)."""
    base.need(model.get("source_year")==year and
              model.get("capacity_semantics")==MODE and
              model.get("E_and_ES_fully_independent_primal_mass_electricity_EOS_market_replay") is True and
              model.get("matched_exogenous_hydrogen_service_tonnes_day")==30. and
              model.get("cost_lower_bound_source_reported_NOT_independent_dual_reconstruction") is True and
              model.get("actual_site_or_manufacturer_or_BAFU_LCIA_or_scientific_v1_0_certified") is False and
              model.get("original_hourly_provider_arrays_or_solver_witnesses_in_public") is False,
              "annual integer result not a valid independent H30 source physics replay")
    annual=base.numeric(model.get("matched_exogenous_service_annual_H2_kg"),
                        "annual matched H2 kg")
    base.need(abs(annual-annual_kg)<=.005,
              "exogenous actual annual H2 delivery not identical daily matched service")
    results=model.get("case_results")
    base.need(type(results) is dict and set(results)=={"E","E_plus_S"},
              "both original equipment variants must be independently reviewed")
    annual_cases={}
    for case in ("E","E_plus_S"):
        r=results[case]
        base.need(r.get("status")==
                  "INDEPENDENT_ORIGINAL_FULL_YEAR_INTEGER_PRIMAL_H2_ELECTRIC_EOS_REPLAY_PASSED" and
                  r.get("original_private_hourly_H2_wind_price_primal_vectors_NOT_in_public") is True and
                  r.get("independent_integer_cost_dual_tree_proof") is False,
                  "source original integer dispatch witness not independently verified")
        base.need(abs(base.numeric(r.get("independent_annual_delivered_H2_kg"),
                                      case+" H2 kg")-annual)<.005 and
                  0<=base.numeric(r.get("source_reported_relative_MIP_gap"),
                                  case+" MIP gap")<=1e-6 and
                  base.numeric(r.get("independent_source_max_physical_residual"),
                               case+" physical residual")<=2e-4 and
                  base.numeric(r.get("independent_EOS_min_absolute_bar"),
                               case+" EOS pressure minimum")>=20.-1e-4 and
                  base.numeric(r.get("independent_EOS_max_absolute_bar"),
                               case+" EOS pressure maximum")<=200.+1e-4,
                  "independent hourly H2/EOS/source MIP numerical acceptance changed")
        h=r.get("independent_hourly_primal_SHA256")
        base.need(type(h) is str and len(h)==64 and all(x in "0123456789abcdef" for x in h),
                  "unmatched original private source dispatch SHA")
        cost=base.numeric(r.get("source_modelled_nominal_original_year_wholesale_eur"),
                          case+" original source-year wholesale cost")
        lower=base.numeric(r.get("source_reported_solver_cost_lower_bound_eur"),
                           case+" source-reported HiGHS cost lower bound")
        base.need(lower<=cost+.1,
                  "reported original source solver cost bound exceeds original feasible cost")
        annual_cases[case]={
            "source_year_nominal_wholesale_cost_eur":cost,
            "source_reported_lower_bound_eur":lower,
            "source_reported_relative_gap":r["source_reported_relative_MIP_gap"],
            "independently_replayed_annual_hydrogen_kg":annual,
            "original_hourly_primal_SHA256":h,
            "private_hourly_state_arrays_in_public":False,
        }
    cost_e=annual_cases["E"]["source_year_nominal_wholesale_cost_eur"]
    cost_s=annual_cases["E_plus_S"]["source_year_nominal_wholesale_cost_eur"]
    saving=cost_e-cost_s
    lo=annual_cases["E"]["source_reported_lower_bound_eur"]-cost_s
    hi=cost_e-annual_cases["E_plus_S"]["source_reported_lower_bound_eur"]
    original_bounds=model.get("matched_service_source_solver_reported_savings_lower_upper_eur")
    base.need(type(original_bounds) is list and len(original_bounds)==2 and
              abs(base.numeric(original_bounds[0],"source saving bound low")-lo)<.05 and
              abs(base.numeric(original_bounds[1],"source saving bound high")-hi)<.05 and
              lo-.02<=saving<=hi+.02 and
              abs(base.numeric(model.get("matched_service_modelled_wholesale_E_minus_ES_saving_source_eur"),
                               "matched annual saving")-saving)<.02 and
              abs(base.numeric(model.get("matched_service_modelled_saving_eur_per_kg_H2"),
                               "EUR per kg")-saving/annual)<1e-10,
              "2024 independent source saving, service-normalization or reported source bounds mismatch")
    return {
        "source_year":year,
        "calendar_UTC_hours":8760 if year==2022 else 8784,
        "exogenous_hydrogen_tonnes_per_day":30.,
        "annual_delivered_H2_kg":annual,
        "original_wind_electric_power_multiplier":.9,
        "source_year_E_20t_wholesale_eur":cost_e,
        "source_year_EplusS_40t_wholesale_eur":cost_s,
        "source_year_wholesale_E_minus_EplusS_saving_eur":saving,
        "source_year_wholesale_saving_eur_per_kg":saving/annual,
        "source_year_EplusS_wholesale_cost_reduction_fraction_of_E":
            saving/cost_e if cost_e>0 else None,
        "source_solver_reported_cost_saving_lower_upper_eur":[lo,hi],
        "original_source_two_integer_primal_replays":True,
        "original_2022_vs_2024_EUR_inflation_adjusted":False,
        "integer_search_tree_dual_independently_reconstructed":False,
        "source_cases":annual_cases,
    }


def audit_2024_and_compare(records,sha,source_bytes,old_audit,old_integer):
    """Proof checks before publishing ANY of three 2024 files or cross-year results."""
    base.need(base.source_blob_sha(source_bytes)==base.SOURCE_PUBLISHED_GIT_BLOB,
              "original four-case 2022/2024 public source Git blob fingerprint mismatch")
    source=json.loads(source_bytes.decode("utf-8"))
    case_list=[x for x in source["cases"] if x["year"]==2024 and
               x["storage_capacity_semantics"]==MODE]
    base.need(len(case_list)==1,"unique original source 2024 max_inventory case missing")
    original=case_list[0]
    price=original["source_year_price_f64_sha256"]
    wind=original["source_year_wind_f64_sha256"]
    selected=original["price_neutral_E_uniform_hydrogen_service"]
    selected_sha=selected["hourly_target_f64_sha256"]
    selected_tpd=base.numeric(selected["modelled_delivered_h2_tonnes_per_day"],
                              "source E-selected maximum 2024 H2")
    base.need(selected_tpd>30.,
              "2024 externally fixed 30t/d target cannot be E-selected maximal service")
    lp=records.get(LP_FILE)
    integer=records.get(INTEGER_FILE)
    base.need(type(lp) is dict and type(integer) is dict,
              "2024 independently reviewed LP and integer source evidence missing")
    base.need(lp.get("source_year")==2024 and
              lp.get("capacity_semantics")==MODE and
              lp.get("source_calendar_UTC_hours")==8784 and
              lp.get("source_original_4_case_public_Git_blob_sha1")==
                  base.SOURCE_PUBLISHED_GIT_BLOB and
              lp.get("source_original_price_float64_SHA256")==price and
              lp.get("source_original_wind_power_float64_SHA256")==wind and
              lp.get("source_original_E_max_selected_hourly_H2_float64_SHA256")==selected_sha and
              abs(base.numeric(lp.get("original_selected_E_max_nominal_tonnes_day"),
                               "2024 selected H2 t/day")-selected_tpd)<1e-8 and
              lp.get("prespecified_exogenous_delivery_tonnes_day")==[25.,27.5,30.] and
              lp.get("source_wind_electric_power_multipliers")==[.9,.95,1.] and
              lp.get("source_price_year_input_unchanged") is True and
              lp.get("same_H2_target_hourly_for_E_and_ES_at_every_wind_factor") is True and
              lp.get("exogenous_delivery_schedules_selected_without_looking_at_stressed_wind_outcomes") is True and
              lp.get("original_integer_dispatch_or_matched_wholesale_savings_certified") is False and
              lp.get("real_site_or_manufacturer_or_native_BAFU_or_scientific_v1_0") is False,
              "2024 LP original observed source model/provider or registered service shifted")
    grid=lp.get("nine_service_factor_pairs_two_architectures_LP_cells")
    base.need(type(grid) is list and len(grid)==9 and
              {(r.get("exogenous_H2_tonnes_per_day"),r.get("source_wind_power_multiplier"))
               for r in grid}==
              {(d,k) for d in (25.,27.5,30.) for k in (.9,.95,1.)},
              "complete original prespecified 2024 exogenous 9-pair grid missing")
    for row in grid:
        base.need(row.get("source_year")==2024 and
                  row.get("capacity_semantics")==MODE and
                  row.get("E_and_ES_original_integer_dispatch_both_certified") is False and
                  row.get("matched_source_annual_E_minus_EplusS_cost_saving_eur") is None,
                  "2024 LP case asserted invalid original integer/economics certificate")
        cases=row.get("cases")
        base.need(type(cases) is dict and set(cases)=={"E","E_plus_S"} and
                  all(case.get("HiGHS_LP_status_code")==0 and
                      case.get("original_integer_MILP_feasible") is None and
                      case.get("source_E_or_EplusS_original_model_LP_status")==
                          "SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED"
                      for case in cases.values()),
                  "registered 2024 original LP screen failed its independent feasibility gate")
    target_hash=base.floating_sha([1250.]*8784)
    chosen=[r for r in grid if r["exogenous_H2_tonnes_per_day"]==30. and
            r["source_wind_power_multiplier"]==.9]
    base.need(len(chosen)==1 and
              chosen[0].get("exogenous_H2_original_same_hourly_SHA256")==target_hash and
              abs(base.numeric(chosen[0].get("exogenous_same_product_annual_H2_kg"),
                               "2024 matched H2 kg")-10980000.)<.005,
              "2024 source target hourly SHA or leap-year full H2 service changed")
    base.need(integer.get("source_year_UTC_hours")==8784 and
              integer.get("source_original_four_case_public_Git_blob_sha1")==
                  base.SOURCE_PUBLISHED_GIT_BLOB and
              integer.get("independent_LP_screen_bytes_SHA256")==sha[LP_FILE] and
              integer.get("original_price_f64_SHA256")==price and
              integer.get("original_wind_electric_power_f64_SHA256")==wind and
              integer.get("exogenous_fixed_hourly_hydrogen_service_f64_SHA256")==target_hash and
              abs(base.numeric(integer.get("source_original_E_selected_max_H2_tonnes_day"),
                               "2024 original E-selected H2 t/d")-selected_tpd)<1e-8 and
              integer.get("original_source_year_eur_not_inflation_adjusted") is True,
              "2024 source integer witness provenance not identical to 2024 LP/provider source")
    old=old_audit
    base.need(old.get("exogenous_year")==2022 and
              old.get("capacity_semantics")==MODE and
              old.get("independently_replayed_original_integer_H2_power_EOS_market") is True and
              old.get("verified_original_historical_source_public_blob")==
                  base.SOURCE_PUBLISHED_GIT_BLOB and
              old.get("real_site_OEM_native_BAFU_and_scientific_v1_0_verified") is False,
              "2022 originally published source-year reference not independently audited")
    old_pair=require_reviewed_pair(2022,old_integer,10950000.)
    new_pair=require_reviewed_pair(2024,integer,10980000.)
    base.need(old_pair["source_year_wholesale_E_minus_EplusS_saving_eur"]==
              old["paired_E_minus_EplusS_nominal_source_year_eur"] and
              old_pair["source_year_wholesale_saving_eur_per_kg"]==
              old["per_kg_modelled_source_year_nominal_eur"],
              "2022 original published cost/savings audit no longer consistent")
    base.need(price!=old_integer.get("original_price_f64_SHA256") and
              wind!=old_integer.get("original_wind_electric_power_f64_SHA256"),
              "2024 provider-year chronology mistakenly duplicates original 2022 source")
    base.need(old_pair["source_year_wholesale_E_minus_EplusS_saving_eur"]>0 and
              new_pair["source_year_wholesale_E_minus_EplusS_saving_eur"]>0,
              "do not publish both-year-positive storage claim if source signs disagree")
    norm_old=old_pair["source_year_wholesale_saving_eur_per_kg"]
    norm_new=new_pair["source_year_wholesale_saving_eur_per_kg"]
    diff=norm_new-norm_old
    return {
        "schema_version":SCHEMA,
        "original_four_case_public_Git_blob_sha1":base.SOURCE_PUBLISHED_GIT_BLOB,
        "source_years":[2022,2024],
        "storage_capacity_interpretation":MODE,
        "H2_product_prespecified_externally_from_maximum_E":True,
        "matched_hydrogen_delivery_tonnes_per_day":30.,
        "modelled_wind_ELECTRIC_POWER_availability_factor":.9,
        "same_fixed_hydrogen_every_hour_of_each_year_for_E_and_ES":True,
        "year_specific_nominal_electricity_price_and_wind_chronologies_not_mixed":True,
        "source_year_results":[old_pair,new_pair],
        "source_2022_audit_verified_historical_cost_saving_eur":
            old["paired_E_minus_EplusS_nominal_source_year_eur"],
        "2024_minus_2022_nominal_saving_eur_per_kg":diff,
        "2024_vs_2022_fractional_change_in_nominal_saving_per_kg":diff/norm_old,
        "2024_saving_fraction_of_2022_saving_per_kg":norm_new/norm_old,
        "both_source_years_storage_reduces_modelled_wholesale_electricity_cost":True,
        "scientific_independence":"Independent equation/historical-year replay; source reported HiGHS integer cost bounds, NOT independently rebuilt integer tree",
        "comparison_does_NOT_establish_statistics_future_expected_value_weather_probability":
            True,
        "comparison_2022_2024_nominal_EUR_NOT_inflation_adjusted":True,
        "source_year_2022_and_2024_are_NOT_independent_random_draws":True,
        "source_years_included_only_2022_and_2024_NOT_intermediate_2023":True,
        "no_actual_installed_CAPEX_OPEX_fuel_LCIA_manufacturer_BAFU_site_or_v1":True,
        "public_hourly_provider_price_wind_or_original_MILP_witness_arrays_in_report":False,
    }


def report_markdown(report):
    years=report["source_year_results"]
    rows=[
        "# F3-D: independently replayed exogenous 30t/day H2 source-year economics — 2022 and 2024",
        "",
        "Both 2022 and 2024 original E20t and E+S40t full-year integer-model",
        "dispatches independently passed original-hour physical, pressure/EOS",
        "and signed 2022/2024 wholesale electricity settlement replay.",
        "Every scenario holds 30 tonnes/day H2 constant, and",
        "the intervention is 90% of source-year modelled wind ELECTRIC POWER.",
        "No source 2023 data, weather uncertainty distribution or forward forecast is included.",
        "",
        "| Metric | 2022 (8,760 h) | 2024 (8,784 h) |",
        "|---|---:|---:|",
        f"| Delivered H2 (kg) | {years[0]['annual_delivered_H2_kg']:,.0f} | {years[1]['annual_delivered_H2_kg']:,.0f} |",
        f"| E20t nominal source-year wholesale electricity cost (EUR) | {years[0]['source_year_E_20t_wholesale_eur']:,.2f} | {years[1]['source_year_E_20t_wholesale_eur']:,.2f} |",
        f"| E+S40t nominal source-year wholesale electricity cost (EUR) | {years[0]['source_year_EplusS_40t_wholesale_eur']:,.2f} | {years[1]['source_year_EplusS_40t_wholesale_eur']:,.2f} |",
        f"| E−E+S annual nominal source-year saving (EUR) | **{years[0]['source_year_wholesale_E_minus_EplusS_saving_eur']:,.2f}** | **{years[1]['source_year_wholesale_E_minus_EplusS_saving_eur']:,.2f}** |",
        f"| E−E+S nominal saving per kg delivered H2 (EUR/kg) | {years[0]['source_year_wholesale_saving_eur_per_kg']:.8f} | {years[1]['source_year_wholesale_saving_eur_per_kg']:.8f} |",
        f"| E+S reduction versus E wholesale cost | {100*years[0]['source_year_EplusS_wholesale_cost_reduction_fraction_of_E']:.3f}% | {100*years[1]['source_year_EplusS_wholesale_cost_reduction_fraction_of_E']:.3f}% |",
        "",
        f"Difference in nominal source-year normalized savings (2024 minus 2022): "
        f"**{report['2024_minus_2022_nominal_saving_eur_per_kg']:+.8f} EUR/kg**, "
        f"or **{100*report['2024_vs_2022_fractional_change_in_nominal_saving_per_kg']:+.2f}%** "
        "relative to 2022. It is not inflation-adjusted and is not a weather-risk "
        "confidence interval or expected annual savings estimate.",
        "",
        "The only optimization lower bounds here are original-source HiGHS "
        "reported integer cost bounds, with individual full-year MILP gaps "
        "<=1e-6. Their source-reported annual savings intervals are in the "
        "validated JSON, and are numerical bounds, NOT uncertainty bands. "
        "PtXLens independently recomputes all hourly state constraints and "
        "market-cost arithmetic but not the original full mixed-integer solver tree.",
        "",
        "This does not establish matched-site vendor CAPEX/OPEX, actual grid export "
        "rights or power contracts, stack degradation, measured real plant "
        "performance, a statistically representative distribution of wind/price "
        "regimes, native BAFU:2026 v1.1 process-linked BOM or complete environmental "
        "LCA, additional storage investment viability or programme scientific v1.0.",
        "",
    ]
    return "\n".join(rows)


def audit(root,original_public):
    root=Path(root)
    original_public=Path(original_public)
    base.need(original_public.is_file() and not original_public.is_symlink(),
              "original four-case source publication not an ordinary file")
    source_raw=original_public.read_bytes()
    old=base.audit(root,original_public)
    old_integer=json.loads(
        (root/"F3D_EXOGENOUS_2022_max_inventory_H30_W090_BOTH_INTEGER_INDEPENDENT_REPLAY_v1.json").read_text(
            encoding="utf-8"))
    values,hashes=get_2024_files(root)
    output=audit_2024_and_compare(values,hashes,source_raw,old,old_integer)
    output["2022_completed_nine_source_result_files_audited_count"]=len(old["approved_public_files"])
    output["2024_safe_evidence_allowlist_sha256"]=[
        {"relative_path":"data/results/"+name,"sha256":hashes[name]}
        for name in THREE
    ]
    output["source_2022_independent_integer_evidence_sha256"]=next(
        x["file_SHA256"] for x in old["approved_public_files"]
        if x["relative_path"].endswith(
            "F3D_EXOGENOUS_2022_max_inventory_H30_W090_BOTH_INTEGER_INDEPENDENT_REPLAY_v1.json"))
    return output


def write_immutable_output(root,report):
    root=Path(root)
    base.need(root.is_dir() and not root.is_symlink(),
              "public output directory missing")
    data=[
        (root/(STEM+".json"),json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n"),
        (root/(STEM+".md"),report_markdown(report)),
    ]
    for path,body in data:
        base.need(not path.is_symlink() and
                  (not path.exists() or
                   (path.is_file() and path.read_text(encoding="utf-8")==body)),
                  "source-locked cross-year scientific result already exists and differs")
        base.need(len(body.encode("utf-8"))<=base.MAX_JSON_BYTES,
                  "cross-year report too large for publication")
    for path,body in data:
        if not path.exists():
            with path.open("x",encoding="utf-8",newline="\n") as out:
                out.write(body)
    return [p.name for p,_ in data]


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir",required=True,type=Path)
    parser.add_argument("--original-public-source",required=True,type=Path)
    args=parser.parse_args(argv)
    report=audit(args.results_dir,args.original_public_source)
    created=write_immutable_output(args.results_dir,report)
    print("F3D_2024_SOURCE_EVIDENCE_AND_2022_2024_CROSS_YEAR_AUDIT_PASS")
    for item in report["2024_safe_evidence_allowlist_sha256"]:
        print(item["relative_path"],item["sha256"])
    print("CROSS_YEAR original 2022 EUR/kg=",report["source_year_results"][0]["source_year_wholesale_saving_eur_per_kg"],
          "original 2024 EUR/kg=",report["source_year_results"][1]["source_year_wholesale_saving_eur_per_kg"],
          "source 2022 and 2024 year-specific NOMINAL EUR, NOT market forecast")
    for filename in created:
        print("NEW_CROSS_YEAR_PUBLIC_SCIENTIFIC_RESULT", "data/results/"+filename)
    print("Three original 2024 source E/ES research artifacts + two derived comparison files can be MANUALLY staged AFTER inspecting every file; no publishing performed")


if __name__=="__main__":
    main()
