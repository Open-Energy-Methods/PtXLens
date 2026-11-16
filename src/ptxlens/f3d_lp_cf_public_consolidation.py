"""Public F3-D independent-LP saving interval and controlled-stress consolidation.

Original source/LP/primal reviewer records are immutable. This method does
not certify independent integer-tree duals, site investments, or native BAFU.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

PIN="ca07f5ef1e381fa157982bc5a68e46ce3022003a"
LP_SCHEMA="ptxlens.f3d_independent_original_source_year_relaxed_LP_cost_dual_KKT.v1"
CF_SCHEMA="ptxlens.f3d_controlled_original_year_private_pair_independent_primal_replay.v1"
OUT_SCHEMA="ptxlens.f3d_independent_LP_positive_saving_and_controlled_counterfactual.v1"

class ReviewError(ValueError): pass

def check(ok,why):
    if not ok: raise ReviewError("F3-D LP/CF public review: "+why)

def finite(x,label):
    check(type(x) in (float,int) and math.isfinite(x),"invalid "+label)
    return float(x)

def review(original,lp,cf):
    year=lp.get("source_year");mode=lp.get("mode")
    check(year in (2022,2024) and mode in ("max_inventory","usable_service"),
          "year or capacity mode not defined")
    check(lp.get("schema_version")==LP_SCHEMA and cf.get("schema_version")==CF_SCHEMA
          and cf.get("year")==year and cf.get("mode")==mode,
          "independent LP/counterfactual schema-year-mode mismatch")
    check(lp.get("original_source_public_Git_blob")==PIN
          and cf.get("reference_original_public_four_case_Git_blob_sha1")==PIN,
          "original public four-case version changed")
    check(lp.get("source_hours")==({2022:8760,2024:8784}[year])
          and cf.get("source_calendar_hours")==({2022:8760,2024:8784}[year]),
          "UTC calendar or leap day missing")
    check(original.get("independent_year_mode_full_hourly_primal_E_EplusS_and_EOS_replay_passed") is True
          and original.get("independent_solver_dual_certificates_recomputed") is False
          and original.get("scientific_v1_0_release_allowed") is False,
          "original independent source or release gate invalid")
    records=original.get("cases")
    check(type(records) is list and len(records)==4,"original public source cases missing")
    match=[x for x in records if x.get("year")==year and x.get("storage_capacity_semantics")==mode]
    check(len(match)==1,"exact year/mode original reference missing")
    baseline=match[0]
    for base_key,lp_key,cf_key in (
        ("source_year_price_f64_sha256","original_source_price_f64_sha256","original_provider_price_f64_SHA256"),
        ("source_year_wind_f64_sha256","original_source_wind_f64_sha256","original_provider_wind_f64_SHA256")
    ):
        check(baseline[base_key]==lp.get(lp_key)==cf.get(cf_key),
              "original source price or wind array SHA mismatch")
    h2=baseline["price_neutral_E_uniform_hydrogen_service"]
    check(lp.get("original_hourly_hydrogen_service_f64_sha256")==
          cf.get("fixed_original_price_blind_E_hydrogen_service_f64_SHA256")==
          h2["hourly_target_f64_sha256"],
          "counterfactual hourly H2 target differs from original year")
    annual=finite(h2["modelled_delivered_h2_kg_per_year"],"H2 kg")
    check(abs(annual-finite(cf.get("fixed_hydrogen_same_hour_kg_year"),"CF H2"))<0.005,
          "annual fixed H2 functional unit changed")
    check(lp.get("original_HiGHS_branch_and_bound_dual_reconstructed") is False
          and cf.get("independent_cost_dual_or_LP_infeasibility_proof_completed") is False
          and cf.get("measured_site_or_manufacturer_or_BAFU_or_v1_0_validated") is False,
          "external dual/native-BAFU/site release falsely claimed")
    rows=lp.get("E_and_EplusS_independent_LP_relaxed_global_cost_lower_bound_cases",{})
    check(set(rows)=={"E","E_plus_S"},"both LP lower bounds required")
    case_bounds={}
    for case in ("E","E_plus_S"):
        r=rows[case]
        check(r.get("LP_optimally_solved") is True and
              r.get("independent_relaxed_LP_dual_KKT_passed") is True,
              "independent source LP KKT failed")
        lb=finite(r.get("source_cost_lower_bound_eur"),case+" LP lower")
        primal=finite(r.get("original_source_integer_primal_cost_eur"),case+" feasible")
        gap=finite(r.get("LP_to_original_integer_primal_relative_cost_gap"),case+" gap")
        check(lb<=primal+0.1 and gap>=0 and
              abs(gap-max(0.,primal-lb)/max(1.,abs(primal)))<1e-10 and
              abs(primal-finite(baseline[case]["modelled_nominal_eur_wholesale_cost"],case+" original"))<0.02,
              "LP/integer feasible costs and gap inconsistent")
        case_bounds[case]={"independent_LP_lower_bound_eur":lb,
                           "previously_physically_replayed_integer_feasible_eur":primal,
                           "LP_to_integer_relative_gap":gap,
                           "integer_optimum_closed_to_1e_minus6_by_independent_LP":gap<=1e-6}
    e=case_bounds["E"];es=case_bounds["E_plus_S"]
    independent_low=e["independent_LP_lower_bound_eur"]-es["previously_physically_replayed_integer_feasible_eur"]
    independent_high=e["previously_physically_replayed_integer_feasible_eur"]-es["independent_LP_lower_bound_eur"]
    base_saving=finite(baseline["matched_service_annual_operational_savings_nominal_eur"],"baseline savings")
    check(independent_low-0.02<=base_saving<=independent_high+0.02,
          "independent source-year LP bounds do not enclose baseline saving")
    pair=cf.get("cases",{})
    check(set(pair)=={"E","E_plus_S"},"both controlled source cases required")
    success=cf.get("physical_original_full_year_primal_replay_passed_for_both") is True
    if success:
        check(all(v.get("status")=="INDEPENDENT_FULL_YEAR_PRIMAL_AND_PRESSURE_COST_REPLAY_PASSED" for v in pair.values())
              and cf.get("economic_result_null_if_any_unverified_or_infeasible") is False,
              "counterfactual independent full-year witness failed")
        new=finite(cf.get("paired_E_minus_EplusS_nominal_operational_saving_eur"),"stress saving")
        check(abs(new-(finite(pair["E"]["source_model_cost_eur"],"CF E")-
                       finite(pair["E_plus_S"]["source_model_cost_eur"],"CF ES")))<0.02,
              "counterfactual independent source costs inconsistent")
        interval=cf.get("paired_source_solver_reported_bound_interval_eur")
        check(type(interval) is list and len(interval)==2 and
              finite(interval[0],"CF low")<=new+0.02<=finite(interval[1],"CF high")+0.02,
              "CF solver bound arithmetic invalid")
        change=new-base_saving;change_percent=100*change/base_saving
        perkg=new/annual
    else:
        check(cf.get("economic_result_null_if_any_unverified_or_infeasible") is True and
              cf.get("paired_E_minus_EplusS_nominal_operational_saving_eur") is None and
              cf.get("paired_source_solver_reported_bound_interval_eur") is None,
              "infeasible or noncertified original H2 scenario must keep NULL saving")
        new=None;change=None;change_percent=None;perkg=None;interval=None
    return {
        "schema_version":OUT_SCHEMA,"original_evidence_Git_blob_SHA1":PIN,
        "year":year,"capacity_semantics":mode,
        "variant":cf["variant"],"hours":{2022:8760,2024:8784}[year],
        "original_verified_h2_hourly_target_SHA256":h2["hourly_target_f64_sha256"],
        "original_matched_h2_kg_per_year":annual,
        "original_nominal_source_year_E_minus_ES_saving_eur":base_saving,
        "independent_original_LP_global_savings_interval_eur":[independent_low,independent_high],
        "independent_original_LP_proves_positive_saving":independent_low>0,
        "independent_original_LP_KKT_both_passed":True,
        "LP_cases":case_bounds,
        "controlled_pair_full_hourly_primal_E_and_ES_independently_replayed":success,
        "controlled_pair_source_solver_reported_interval_eur":interval,
        "controlled_pair_modelled_savings_eur":new,
        "controlled_pair_modelled_savings_eur_per_kg_H2":perkg,
        "controlled_savings_change_from_original_eur":change,
        "controlled_savings_change_from_original_percent":change_percent,
        "source_original_INTEGER_branch_and_bound_independently_certified":False,
        "observed_source_year_EUR_not_harmonized":True,
        "real_site_market_forecast_vendor_BAFU_and_scientific_v1_0_completed":False,
    }

def prose(r):
    y=r["year"];mode=r["capacity_semantics"];v=r["variant"]
    lo,hi=r["independent_original_LP_global_savings_interval_eur"]
    lines=[
        "# F3-D independent LP proof bounds and controlled original-source sensitivity",
        "",
        f"Source year {y}, capacity {mode}, controlled input {v}. Original "
        f"modelled nominal electricity saving EUR {r['original_nominal_source_year_E_minus_ES_saving_eur']:,.2f}.",
        "",
        f"Independent KKT-replayed relaxed-LP E minus E+S annual saving interval: "
        f"**EUR [{lo:,.2f}, {hi:,.2f}]**. This validates the sign of the "
        "modelled operating advantage when its lower bound is positive, "
        "but does NOT reproduce the original integer search-tree dual "
        "or independently close the two MIP optima to 1e-6.",
        "",
    ]
    if r["controlled_pair_full_hourly_primal_E_and_ES_independently_replayed"]:
        s=r["controlled_pair_modelled_savings_eur"]
        delta=r["controlled_savings_change_from_original_eur"]
        p=r["controlled_savings_change_from_original_percent"]
        lines.append(f"The independently PtXLens-replayed controlled E/E+S model "
                     f"annual saving is **EUR {s:,.2f}**, a change of "
                     f"**EUR {delta:,.2f} ({p:+.2f}%)** from the same original "
                     "year/mode under the unchanged exact hourly H2 product.")
    else:
        lines.append("At least one controlled case did not independently certify "
                     "the exact originally required hourly H2 product. "
                     "Controlled paired saving is **NULL**, not zero.")
    lines.extend(["","Controlled intervention is not observed future market data. "
                  "LP/MIP numerical intervals are not statistical forecast "
                  "confidence intervals. Vendor installed CAPEX/OPEX, "
                  "BAFU process inventory and whole-plant GWP and v1.0 remain "
                  "**unverified**."])
    return "
".join(lines)+"
"

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--original-public-source",required=True,type=Path)
    parser.add_argument("--lp-review",required=True,type=Path)
    parser.add_argument("--counterfactual-review",required=True,type=Path)
    parser.add_argument("--output-dir",required=True,type=Path)
    args=parser.parse_args(argv)
    original_bytes=args.original_public_source.read_bytes().replace(b"
",b"
")
    git=hashlib.sha1(b"blob "+str(len(original_bytes)).encode()+b"\0"+original_bytes).hexdigest()
    check(git==PIN,"source 2022/2024 original Git blob changed")
    original=json.loads(original_bytes.decode("utf-8"))
    lpbytes=args.lp_review.read_bytes()
    cfbytes=args.counterfactual_review.read_bytes()
    report=review(original,json.loads(lpbytes),json.loads(cfbytes))
    report["source_independent_LP_review_bytes_SHA256"]=hashlib.sha256(lpbytes).hexdigest()
    report["source_independent_CF_review_bytes_SHA256"]=hashlib.sha256(cfbytes).hexdigest()
    target=args.output_dir
    check(target.is_dir() and not target.is_symlink(),
          "existing public output directory required")
    base=f"F3D_{report['year']}_{report['capacity_semantics']}_{report['variant']}_LP_CF_PUBLIC_v1"
    outputs=[
        (target/(base+".json"),json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"
"),
        (target/(base+".md"),prose(report)),
    ]
    for path,body in outputs:
        check(not path.exists() or (path.is_file() and not path.is_symlink() and
              path.read_text(encoding="utf-8")==body),"cannot overwrite different source review")
    for path,body in outputs:
        if not path.exists():
            with path.open("x",encoding="utf-8",newline="
") as out:out.write(body)
    print("F3D_INDEPENDENT_KKT_LP_SAVINGS_INTERVAL_AND_CF_READY",
          report["year"],report["capacity_semantics"],report["variant"],
          "no v1.0 or vendor/BAFU release")

if __name__=="__main__":
    main()
