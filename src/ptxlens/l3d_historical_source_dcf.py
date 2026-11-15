"""L3-D. Historical 2022/2024 source-model E vs E+S conditional DCF.

Only consumes the Git-blob pinned, independently PtXLens-replayed public PtXFlex
F3-D aggregate. Annual savings are NOT an observed future price forecast;
each source-year monetary unit is kept separate (no CPI adjustment).
Unknown manufacturer installed CAPEX, BoP, OPEX, BAFU and site data stay UNKNOWN.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path

BLOB_SHA="ca07f5ef1e381fa157982bc5a68e46ce3022003a"
SCHEMA="oem.ptx.f3d_2022_2024_public_source_aggregate_independent_replay.v1"
OUTPUT_SCHEMA="ptxlens.l3d_2022_2024_scenario_only_historical_source_DCF.v1"
ORIGINAL_WIND_SHA="9e0e95ddf9c70547ab6ce696f52a82dc312f11d7cd760de5dc779c6ac2b43c9c"
YEARS={2022:8760,2024:8784}
MODES=("max_inventory","usable_service")
FILE_NAME="L3_D_2022_2024_historical_DCF_frontiers_NOT_site_NPV.json"
MD_NAME="L3_D_2022_2024_historical_DCF_frontiers_NOT_site_NPV.md"

class HistoricalSourceDCFError(ValueError):
    pass

def need(yes,why):
    if not yes:
        raise HistoricalSourceDCFError("L3-D: "+why)

def number(value,name,lower=None):
    need(type(value) in (int,float) and math.isfinite(value),name+" not a finite number")
    v=float(value)
    if lower is not None: need(v>=lower,name+" violates lower bound")
    return v

def git_blob_hash(raw):
    need(b"\r" not in raw.replace(b"\r\n",b""),"unexpected noncanonical input newline")
    raw=raw.replace(b"\r\n",b"\n")
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()

def check_four_cases(blob):
    need(type(blob) is dict and blob.get("schema_version")==SCHEMA,"unknown original evidence schema")
    need(blob.get("2023_CDS_to_ARCO_full_year_original_source_calibration_passed") is True and
         blob.get("2023_CDS_to_ARCO_8760_hour_1W_source_reference_SHA256")==ORIGINAL_WIND_SHA,
         "original 2023 wind/CDS source anchor unverified")
    for name in ("scientific_v1_0_release_allowed","installed_plant_investment_DCF_certified",
                 "manufacturer_storage_incremental_CAPEX_OPEX_verified",
                 "native_BAFU_2026_whole_plant_LCIA_verified",
                 "independent_solver_dual_certificates_recomputed",
                 "real_industrial_site_H2_validation_completed",
                 "source_original_hourly_arrays_released","private_hourly_primal_witnesses_released"):
        need(blob.get(name) is False,"unsupported release/scope flag: "+name)
    for name in ("independent_financial_metadata_four_case_review_passed",
                 "independent_year_mode_full_hourly_primal_E_EplusS_and_EOS_replay_passed"):
        need(blob.get(name) is True,"original independent source replay missing: "+name)
    data=blob.get("cases")
    need(type(data) is list and len(data)==4,"all four original year/mode cases required")
    out={}
    for item in data:
        year=item.get("year");mode=item.get("storage_capacity_semantics");key=(year,mode)
        need(year in YEARS and mode in MODES and key not in out and
             item.get("year_utc_hours")==YEARS[year],"wrong 2022/2024 leap-year scenario")
        need(item.get("independent_full_hourly_E_and_EplusS_primal_replay_passed") is True and
             item.get("independent_full_hourly_type_I_20_to_200bar_EOS_replay_passed") is True and
             item.get("source_original_hash_and_calendar_gate_passed") is True and
             item.get("independent_solver_dual_certificates_recomputed") is False,
             "invalid individual source-model and physical replay gate")
        for field in ("source_year_price_f64_sha256","source_year_wind_f64_sha256"):
            value=item.get(field)
            need(type(value) is str and len(value)==64 and
                 all(c in "0123456789abcdef" for c in value),
                 "source array checksum absent")
        sel=item.get("price_neutral_E_uniform_hydrogen_service",{})
        alpha=number(sel.get("fraction_of_nominal_50_tonnes_per_day"),"alpha",0.)
        h2=number(sel.get("modelled_delivered_h2_kg_per_year"),"annual H2",0.)
        need(0<alpha<=1 and abs(h2-YEARS[year]*50000/24*alpha)<.005,
             "cross-hour modelled H2 service mismatch")
        need(number(sel.get("solver_reported_relative_optimality_gap"),"alpha gap",0)<=1e-6,
             "uncertified price-blind service selector")
        save=number(item.get("matched_service_annual_operational_savings_nominal_eur"),"saving")
        lo=number(item.get("solver_reported_savings_lower_eur"),"saving lower")
        hi=number(item.get("solver_reported_savings_upper_eur"),"saving upper")
        need(lo-.02<=save<=hi+.02,"solver source saving bounds invalid")
        for name in ("E","E_plus_S"):
            e=item.get(name,{})
            need(abs(number(e.get("modelled_h2_delivered_kg"),name+" H2")-h2)<.005,
                 "E and E+S must deliver same hour-by-hour product within a mode")
            need(number(e.get("solver_reported_relative_mip_gap"),name+" mip gap",0)<=1e-6,
                 "source solver relative gap exceeds 1e-6")
            need(number(e.get("solver_reported_cost_dual_lower_bound_eur"),name+" lower")<=
                 number(e.get("modelled_nominal_eur_wholesale_cost"),name+" primal")+.1,
                 "cost lower bound invalid")
        e=item["E"];s=item["E_plus_S"]
        need(abs(e["modelled_nominal_eur_wholesale_cost"]-s["modelled_nominal_eur_wholesale_cost"]-save)<.02 and
             abs(e["solver_reported_cost_dual_lower_bound_eur"]-s["modelled_nominal_eur_wholesale_cost"]-lo)<.02 and
             abs(e["modelled_nominal_eur_wholesale_cost"]-s["solver_reported_cost_dual_lower_bound_eur"]-hi)<.02,
             "source E/E+S economic primal or dual-bound arithmetic inconsistent")
        need(abs(number(item.get("savings_modelled_nominal_eur_per_kg_of_same_h2_service"),"saving/kg")-save/h2)<1e-8,
             "source annual service normalization inconsistent")
        out[key]=item
    need(set(out)=={(year,mode) for year in YEARS for mode in MODES},
         "missing four historical years and capacity interpretations")
    for year in YEARS:
        a=out[year,MODES[0]];b=out[year,MODES[1]]
        need(a["source_year_price_f64_sha256"]==b["source_year_price_f64_sha256"] and
             a["source_year_wind_f64_sha256"]==b["source_year_wind_f64_sha256"],
             "historical inputs differ within one year")
    return out

def load_pinned_source(path):
    path=Path(path)
    need(path.is_file(),"published original public F3-D aggregate missing")
    raw=path.read_bytes()
    need(git_blob_hash(raw)==BLOB_SHA,"source Git blob has changed; stop for independent review")
    data=json.loads(raw.decode("utf-8-sig"))
    return check_four_cases(data),hashlib.sha256(raw.replace(b"\r\n",b"\n")).hexdigest()

@dataclass(frozen=True)
class Scenario:
    years:int=20
    discount_real:float=.08
    repeat_factor:float=1.
    annual_degradation:float=0.
    opex:float=0.
    capex:float=0.
    replacement_year:int|None=None
    replacement_cost:float=0.
    salvage:float=0.
    decommission:float=0.

    def __post_init__(self):
        need(type(self.years) is int and 1<=self.years<=60,"invalid DCF horizon")
        need(0<=number(self.discount_real,"discount")<1,"discount outside 0...1")
        number(self.repeat_factor,"benefit repeat",0)
        need(0<=number(self.annual_degradation,"degradation")<=1,"degradation outside 0...1")
        for name in ("opex","capex","replacement_cost","salvage","decommission"):
            number(getattr(self,name),name,0)
        if self.replacement_year is None:
            need(self.replacement_cost==0,"replacement cost requires explicit end year")
        else:
            need(type(self.replacement_year) is int and
                 1<=self.replacement_year<=self.years,"replacement year outside horizon")

def cashflows(saving,scenario):
    """t=0 capital; end-year 1..N flow, replacement and salvage timing explicit."""
    saving=number(saving,"historical modelled saving")
    a=scenario
    flows=[-a.capex]
    for year in range(1,a.years+1):
        flow=saving*a.repeat_factor*(1-a.annual_degradation)**(year-1)-a.opex
        if year==a.replacement_year:flow-=a.replacement_cost
        if year==a.years:flow+=a.salvage-a.decommission
        flows.append(flow)
    return flows

def dcf(saving,scenario):
    a=scenario
    flows=cashflows(saving,a)
    pv=[f/(1+a.discount_real)**t for t,f in enumerate(flows)]
    npv=math.fsum(pv)
    capex_ceiling=math.fsum(pv[1:])
    annuity=math.fsum(1/(1+a.discount_real)**t for t in range(1,a.years+1))
    need(annuity>0,"annuity must be positive")
    opex_ceiling=(npv+a.opex*annuity)/annuity
    running=pv[0];first_crossing=None
    for year in range(1,a.years+1):
        running+=pv[year]
        if first_crossing is None and running>=-1e-8:
            first_crossing=year
    return {
        "hypothetical_incremental_NPV_source_year_eur":npv,
        "zero_NPV_extra_all_in_CAPEX_ceiling_source_year_eur":capex_ceiling,
        "break_even_extra_annual_OPEX_at_selected_CAPEX_source_year_eur":opex_ceiling,
        "discounted_first_recovery_year_only_if_final_NPV_nonnegative":
            first_crossing if npv>=0 else None,
        "negative_capex_ceiling_means_no_nonnegative_CAPEX_feasible":capex_ceiling<0,
        "negative_opex_ceiling_means_no_nonnegative_OPEX_feasible":opex_ceiling<0,
    }

def case_dcf(case,scenario):
    """Use source MILP cost interval only; it is not a statistical confidence band."""
    low=case["solver_reported_savings_lower_eur"]
    mid=case["matched_service_annual_operational_savings_nominal_eur"]
    high=case["solver_reported_savings_upper_eur"]
    vals=[dcf(s,scenario) for s in (low,mid,high)]
    cap_key="zero_NPV_extra_all_in_CAPEX_ceiling_source_year_eur"
    npv_key="hypothetical_incremental_NPV_source_year_eur"
    need(vals[0][cap_key]<=vals[1][cap_key]+1e-8<=vals[2][cap_key]+1e-8,
         "solver-derived DCF interval not monotonic")
    return {
        "year":case["year"],"mode":case["storage_capacity_semantics"],
        "source_year_price_unit":f"hypothetical constant {case['year']}-EUR purchasing-power unit; not inflation-adjusted 2026 EUR",
        "same_modelled_H2_kg_year":case["price_neutral_E_uniform_hydrogen_service"]["modelled_delivered_h2_kg_per_year"],
        "source_annual_savings_nominal_eur":mid,
        "source_solver_saving_interval_eur":[low,high],
        "assumed_parameters_HYPOTHETICAL_not_vendor_prices":vars(scenario),
        "modelled_central_economic_result":vals[1],
        "solver_reported_bound_propagated_NPV_interval_eur":[vals[0][npv_key],vals[2][npv_key]],
        "solver_reported_bound_propagated_CAPEX_ceiling_interval_eur":[vals[0][cap_key],vals[2][cap_key]],
        "statistical_confidence_band":False,
        "independent_HiGHS_cost_dual_proof":False,
        "manufacturer_CAPEX_OPEX_verification":False,
        "forecast_of_future_wind_price_or_hydrogen":False,
        "native_BAFU_2026_full_LCIA":False,
        "investment_viability_demonstrated":False,
    }

def output_grid(cases):
    grid=[]
    for key in sorted(cases):
        case=cases[key]
        for years in (10,20,30):
            for discount in (.03,.08,.12):
                for repeat in (.5,1.,1.5):
                    for opex in (0.,250000.,500000.):
                        x=case_dcf(case,Scenario(years=years,discount_real=discount,
                                   repeat_factor=repeat,opex=opex,
                                   replacement_year=10,replacement_cost=1e6))
                        grid.append({
                            "year":key[0],"mode":key[1],"years":years,
                            "discount_real":discount,"repeat_factor":repeat,
                            "annual_extra_OPEX_assumed_eur":opex,
                            "EOY10_replacement_assumed_eur":1000000.,
                            "maximum_extra_initial_CAPEX_at_zero_NPV_eur":
                                x["modelled_central_economic_result"]["zero_NPV_extra_all_in_CAPEX_ceiling_source_year_eur"],
                            "CAPEX_ceiling_source_solver_bound_interval_eur":
                                x["solver_reported_bound_propagated_CAPEX_ceiling_interval_eur"],
                        })
    need(len(grid)==324,"expected exactly 324 DCF deterministic stress cells")
    return grid

def build(cases,source_sha):
    return {
        "schema_version":OUTPUT_SCHEMA,
        "source_original_PtXFlex_git_blob_sha1":BLOB_SHA,
        "source_original_PtXFlex_LF_bytes_sha256":source_sha,
        "source_H2_product_is_matched_ONLY_within_year_and_mode":True,
        "different_2022_and_2024_EUR_and_H2_not_pooled_as_project_cashflow":True,
        "no_future_market_forecast_or_statistical_probability_weights":True,
        "each_source_year_money_basis_separately":True,
        "cashflow_timing":"year0 extra CAPEX, end-year annual net benefits minus extra OPEX, EOY replacements, terminal salvage/decommission",
        "baseline_20_year_8pct_zero_incremental_opex_and_no_replacement":[
            case_dcf(cases[k],Scenario()) for k in sorted(cases)],
        "stress_20_year_8pct_250k_extra_opex_1m_EOY10_replacement":[
            case_dcf(cases[k],Scenario(opex=250000.,replacement_year=10,
                                     replacement_cost=1000000.)) for k in sorted(cases)],
        "analyst_324_case_deterministic_sensitivity_matrix":output_grid(cases),
        "no_manufacturer_CAPEX_quote":True,
        "native_BAFU_LCIA_not_complete":True,
        "independent_dual_certification_not_complete":True,
        "no_full_industrial_H2_contract_or_project_NPV":True,
        "scientific_v1_0_release_allowed":False,
    }

def markdown_report(record):
    a=record["baseline_20_year_8pct_zero_incremental_opex_and_no_replacement"]
    b=record["stress_20_year_8pct_250k_extra_opex_1m_EOY10_replacement"]
    lines=[
        "# L3-D: 2022/2024 source-year conditional hydrogen storage DCF frontiers",
        "",
        "Source: Git-blob pinned PtXFlex original four-case F3-D independently "
        "physical-replayed hourly matched H2 model; no original hourly data redistributed.",
        "",
        "| Historical year | Capacity semantics | Annual modelled wholesale saving EUR | "
        "Modelled H2 t/day | 20y 8% zero-OPEX zero-replacement CAPEX ceiling EUR | "
        "20y 8% 250k OPEX 1m EOY10 replacement CAPEX ceiling EUR |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for x,y in zip(a,b):
        need(x["year"]==y["year"] and x["mode"]==y["mode"],"mismatched DCF display")
        annual=x["same_modelled_H2_kg_year"]
        daily=annual/(YEARS[x["year"]]/24)/1000
        col="zero_NPV_extra_all_in_CAPEX_ceiling_source_year_eur"
        p=x["modelled_central_economic_result"][col]
        q=y["modelled_central_economic_result"][col]
        lines.append(f"| {x['year']} | {x['mode']} | "
                     f"{x['source_annual_savings_nominal_eur']:,.2f} | "
                     f"{daily:.3f} | {p:,.2f} | {q:,.2f} |")
    lines += [
        "",
        "## Mathematical definition",
        "",
        "For each scenario separately: NPV = -I0 + sum over t=1..N of "
        "[S_original * k * (1-d)^(t-1) - O - R_t] / (1+r)^t + "
        "(salvage - decommission)/(1+r)^N. Capital ceiling is the "
        "discounted cashflow excluding I0. All payments occur at specified "
        "year ends. A negative capital or OPEX ceiling implies that no "
        "nonnegative expenditure breaks even.",
        "",
        "S_original is a source-year observed-price/wind model DIFFERENCE, "
        "not a future market forecast. The 20-year 8% real rate, savings "
        "persistence, annual incremental OPEX, replacement costs and site "
        "economics are illustrative analyst assumptions ONLY. Each result "
        "has its own 2022 or 2024 nominal purchasing-power euro unit, "
        "without inflation harmonization. 2023 L3-A uses a different "
        "product H2 target and cannot be spliced into future years.",
        "",
        "The accompanying JSON includes 324 sensitivity cells (4 scenarios x "
        "3 lives x 3 rates x 3 persistence factors x 3 OPEX assumptions; "
        "one 1m EUR replacement at end year 10) and propagates source-solver "
        "economic bounds without calling them statistical confidence limits.",
        "",
        "No independently reconstructed HiGHS dual, vendor installed CAPEX/OPEX "
        "or compressor BOM, production forecast, native BAFU whole-system LCIA, "
        "site permit or financial viability is demonstrated. "
        "Scientific v1.0 remains blocked.",
    ]
    return "\n".join(lines)+"\n"

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source",required=True,type=Path)
    ap.add_argument("--output-dir",required=True,type=Path)
    args=ap.parse_args(argv)
    cases,sha=load_pinned_source(args.source)
    result=build(cases,sha)
    need(args.output_dir.is_dir() and not args.output_dir.is_symlink(),
         "preexisting output directory required")
    outputs=[(args.output_dir/FILE_NAME,
              json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n"),
             (args.output_dir/MD_NAME,markdown_report(result))]
    for path,value in outputs:
        need(not path.exists() or (path.is_file() and not path.is_symlink() and
             path.read_text(encoding="utf-8")==value),
             "existing immutable output differs; use a new source version")
    for path,value in outputs:
        if not path.exists():
            with path.open("x",encoding="utf-8",newline="\n") as f:f.write(value)
    print("L3_D_F3D_SOURCE_BLOB_PINNED_4_CASES 324 deterministic scenarios; "
          "no provider raw arrays; no vendor costs; no native BAFU v1 release")

if __name__=="__main__":
    main()
