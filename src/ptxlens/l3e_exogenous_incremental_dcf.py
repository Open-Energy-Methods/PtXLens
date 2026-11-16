"""L3-E: matched H30/W090 2022/2024 exogenous-service incremental storage DCF.

SOURCE: the immutable published public 2022/2024 PtXLens cross-year JSON
containing independently replayed original E20t/E+S40t *integer* physical
dispatch for 30 t/day hydrogen and 90% original year-specific modeled wind
ELECTRIC power. The only measured mathematical effect is annual source-model
signed WHOLESALE ELECTRICITY SETTLEMENT saving; NOT annual full-plant profit.

CONDITIONAL future thought experiments, not bankable forecasts:
  - repeat a specified fraction of ONE year-specific historic nominal savings
    in a synthetic constant-purchasing-power unit for that source year;
  - use a separately disclosed REAL discount rate, horizon and degradation;
  - model added annual incremental OPEX, incremental storage replacements at
    explicitly given end years, final salvage and decommission, time-zero
    entire incrementally installed CAPEX;
  - calculate the *zero-NPV upfront CAPEX CEILING* and the inverse annual
    incremental OPEX ceiling at a hypothetical initial CAPEX.

One never averages, inflation-adjusts, pools or assigns a probability to
2022 and 2024. HiGHS source original integer cost bounds propagate ONLY as
numerical optimizer-error intervals, not market/weather/site uncertainty.
No physical vendor quote or raw ENTSO-E/ERA5 provider/witness vectors.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/"data/results/F3D_2022_2024_max_inventory_H30_W090_TWO_YEAR_MATCHED_SERVICE_ECONOMICS_v1.json"
SOURCE_GIT_BLOB="c24b4cb0d6a409798c8a7e764965fffd51478a77"
SOURCE_SCHEMA="ptxlens.f3d_original_2022_2024_H30_W090_cross_year_source_economics_verified_public.v1"
SCHEMA="ptxlens.l3e_exogenous_H30_W090_incremental_storage_conditional_CAPEX_OPEX_frontiers.v1"
OUT_JSON="L3E_2022_2024_H30_W090_EXOGENOUS_INCREMENTAL_DCF_FRONTIERS_NOT_VENDOR_NPV_v1.json"
OUT_MD="L3E_2022_2024_H30_W090_EXOGENOUS_INCREMENTAL_DCF_FRONTIERS_NOT_VENDOR_NPV_v1.md"
YEARS=(2022,2024)
HORIZONS=(10,20,25)
RATES=(0.03,0.08,0.12)
REPEAT_FACTORS=(0.5,0.75,1.0)
DEGRADATIONS=(0.,0.02)
ANNUAL_OPEX=(0.,250000.,500000.)
BENCHMARK_CAPEX=10000000.
REPLACEMENT_BENCHMARK_EUR=1000000.
REPLACEMENT_BENCHMARK_YEAR=10


class MatchedStorageDCFError(ValueError):
    pass


def need(ok,message):
    if not ok:
        raise MatchedStorageDCFError("L3-E incremental DCF: "+message)


def number(value,label,*,minimum=None):
    need(type(value) in (int,float) and math.isfinite(value),
         label+" must be finite numeric, never null or bool")
    v=float(value)
    if minimum is not None:
        need(v>=minimum,label+" below permitted bound")
    return v


def git_blob_sha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest()


def load_admitted_source(path=SOURCE):
    path=Path(path)
    need(path.is_file() and not path.is_symlink(),
         "independent public H30 2022/2024 result missing or symlinked")
    raw=path.read_bytes()
    need(git_blob_sha(raw)==SOURCE_GIT_BLOB,
         "published exogenous two-year Git blob differs: STOP for independent review")
    d=json.loads(raw.decode("utf-8"))
    need(d.get("schema_version")==SOURCE_SCHEMA and
         d.get("source_years")==list(YEARS) and
         d.get("storage_capacity_interpretation")=="max_inventory" and
         d.get("H2_product_prespecified_externally_from_maximum_E") is True and
         d.get("matched_hydrogen_delivery_tonnes_per_day")==30. and
         d.get("modelled_wind_ELECTRIC_POWER_availability_factor")==.9 and
         d.get("same_fixed_hydrogen_every_hour_of_each_year_for_E_and_ES") is True and
         d.get("both_source_years_storage_reduces_modelled_wholesale_electricity_cost") is True and
         d.get("comparison_2022_2024_nominal_EUR_NOT_inflation_adjusted") is True and
         d.get("no_actual_installed_CAPEX_OPEX_fuel_LCIA_manufacturer_BAFU_site_or_v1") is True and
         d.get("public_hourly_provider_price_wind_or_original_MILP_witness_arrays_in_report") is False,
         "selected source model, historical currency or scientific research scope changed")
    rows=d.get("source_year_results")
    need(type(rows) is list and [r.get("source_year") for r in rows]==list(YEARS),
         "expected independently compared 2022 and 2024 source years only")
    out={}
    for row in rows:
        year=row["source_year"]
        n=8760 if year==2022 else 8784
        delivered=1250.*n
        need(row.get("calendar_UTC_hours")==n and
             row.get("exogenous_hydrogen_tonnes_per_day")==30. and
             row.get("original_wind_electric_power_multiplier")==.9 and
             row.get("original_source_two_integer_primal_replays") is True and
             row.get("integer_search_tree_dual_independently_reconstructed") is False and
             row.get("original_2022_vs_2024_EUR_inflation_adjusted") is False and
             abs(number(row.get("annual_delivered_H2_kg"),"annual H2")-delivered)<.005,
             "annual original-source H2 service, mode or integer primal evidence drift")
        e=number(row.get("source_year_E_20t_wholesale_eur"),"E signed wholesale EUR")
        es=number(row.get("source_year_EplusS_40t_wholesale_eur"),"ES signed wholesale EUR")
        saved=number(row.get("source_year_wholesale_E_minus_EplusS_saving_eur"),"saving")
        lohi=row.get("source_solver_reported_cost_saving_lower_upper_eur")
        need(type(lohi) is list and len(lohi)==2,
             "original HiGHS source solver bound interval missing")
        low=number(lohi[0],"source HiGHS saving lower")
        high=number(lohi[1],"source HiGHS saving upper")
        cases=row.get("source_cases")
        need(type(cases) is dict and set(cases)=={"E","E_plus_S"},
             "both original integer storage architectures missing")
        for case in ("E","E_plus_S"):
            c=cases[case]
            need(c.get("private_hourly_state_arrays_in_public") is False and
                 number(c.get("source_reported_relative_gap"),"original MILP gap",minimum=0.)<=1e-6 and
                 number(c.get("independently_replayed_annual_hydrogen_kg"),"case H2")==delivered,
                 "source case H2/integer solver bound/private disclosure invalid")
        need(abs(e-es-saved)<.02 and
             low-.02<=saved<=high+.02 and
             abs(number(row.get("source_year_wholesale_saving_eur_per_kg"),"saving/kg")-
                 saved/delivered)<1e-11 and
             abs(low-(cases["E"]["source_reported_lower_bound_eur"]-es))<.05 and
             abs(high-(e-cases["E_plus_S"]["source_reported_lower_bound_eur"]))<.05,
             "source model paired saving/HiGHS error bounds arithmetic not reproducible")
        out[year]={
            "source_year":year,"annual_h2_kg":delivered,"source_annual_saving_eur":saved,
            "source_solver_only_lower_eur":low,"source_solver_only_upper_eur":high,
            "currency_basis":f"hypothetical constant {year}-EUR purchasing power; no future electricity-price forecast",
            "observed_cost_inputs_are_year_specific":True,
        }
    return out


@dataclass(frozen=True)
class Scenario:
    horizon_years:int=20
    real_discount_rate:float=.08
    historical_saving_repeat_fraction:float=1.
    annual_saving_fade_fraction:float=0.
    added_annual_opex_year_eur:float=0.
    hypothetical_initial_capex_year_eur:float=BENCHMARK_CAPEX
    replacements:tuple[tuple[int,float],...]=()
    end_salvage_year_eur:float=0.
    end_decommission_year_eur:float=0.

    def __post_init__(self):
        need(type(self.horizon_years) is int and 1<=self.horizon_years<=60,
             "horizon outside prespecified physical accounting bound")
        need(0<=number(self.real_discount_rate,"real discount")<1,
             "real discount rate outside [0,1)")
        number(self.historical_saving_repeat_fraction,"savings repeat fraction",minimum=0.)
        need(0<=number(self.annual_saving_fade_fraction,"annual fade")<1,
             "annual fade outside [0,1)")
        for fld in ("added_annual_opex_year_eur","hypothetical_initial_capex_year_eur",
                    "end_salvage_year_eur","end_decommission_year_eur"):
            number(getattr(self,fld),fld,minimum=0.)
        need(type(self.replacements) is tuple,
             "replacement events must be a tuple with explicit end-year timing")
        yrs=[]
        for y,cost in self.replacements:
            need(type(y) is int and 1<=y<=self.horizon_years,
                 "replacement year outside analysis horizon")
            number(cost,"replacement incremental cost",minimum=0.)
            yrs.append(y)
        need(len(yrs)==len(set(yrs)),
             "multiple replacement cost events in same year must be consolidated")


def discount_stream(source_saving,sc):
    """Two independently inspectable PV components with explicit cash timing."""
    saving=number(source_saving,"source-year modelled signed power saving")
    r=sc.real_discount_rate
    inflows=[]
    annual_opex_pv=[]
    for t in range(1,sc.horizon_years+1):
        d=(1+r)**(-t)
        inflows.append(saving*sc.historical_saving_repeat_fraction*
                       (1-sc.annual_saving_fade_fraction)**(t-1)*d)
        annual_opex_pv.append(sc.added_annual_opex_year_eur*d)
    annuity=math.fsum((1+r)**(-t) for t in range(1,sc.horizon_years+1))
    replacements_pv=math.fsum(c*(1+r)**(-y) for y,c in sc.replacements)
    terminal_net_pv=(sc.end_salvage_year_eur-sc.end_decommission_year_eur)*\
                    (1+r)**(-sc.horizon_years)
    return {
        "PV_repeated_modelled_wholesale_savings_year_eur":math.fsum(inflows),
        "PV_hypothetical_incremental_opex_year_eur":math.fsum(annual_opex_pv),
        "PV_hypothetical_replacements_year_eur":replacements_pv,
        "PV_hypothetical_net_terminal_salvage_minus_decommission_year_eur":
            terminal_net_pv,
        "annuity_present_value_factor_years":annuity,
    }


def frontier(source_saving,source_lower,source_upper,sc):
    number(source_lower,"lower bound")
    number(source_upper,"upper bound")
    need(source_lower<=source_saving<=source_upper,
         "source HiGHS numerical cost interval does not enclose primal saving")
    pv=discount_stream(source_saving,sc)
    base=pv["PV_repeated_modelled_wholesale_savings_year_eur"]
    fixed=pv["PV_hypothetical_incremental_opex_year_eur"]+\
          pv["PV_hypothetical_replacements_year_eur"]-\
          pv["PV_hypothetical_net_terminal_salvage_minus_decommission_year_eur"]
    ceiling=base-fixed
    annuity=pv["annuity_present_value_factor_years"]
    opex_boundary=(base-pv["PV_hypothetical_replacements_year_eur"]+
                  pv["PV_hypothetical_net_terminal_salvage_minus_decommission_year_eur"]-
                  sc.hypothetical_initial_capex_year_eur)/annuity
    lo=discount_stream(source_lower,sc)["PV_repeated_modelled_wholesale_savings_year_eur"]-fixed
    hi=discount_stream(source_upper,sc)["PV_repeated_modelled_wholesale_savings_year_eur"]-fixed
    need(lo-1e-7<=ceiling<=hi+1e-7,
         "monotonic original-source solver bounds not preserved under DCF")
    return {
        **pv,
        "hypothetical_extra_all_in_installed_CAPEX_zero_NPV_ceiling_year_eur":
            ceiling,
        "hypothetical_extra_all_in_CAPEX_solver_numerical_lower_upper_year_eur":
            [lo,hi],
        "at_assumed_CAPEX_hypothetical_incremental_NPV_year_eur":
            ceiling-sc.hypothetical_initial_capex_year_eur,
        "hypothetical_annual_incremental_OPEX_zero_NPV_ceiling_at_assumed_CAPEX_year_eur":
            opex_boundary,
        "negative_CAPEX_ceiling_means_no_nonnegative_extra_CAPEX_justified":ceiling<0,
        "negative_OPEX_ceiling_means_no_nonnegative_incremental_OPEX_justified":
            opex_boundary<0,
        "original_solver_error_bound_only_NOT_future_saving_uncertainty":True,
        "project_actually_profitable_with_verified_vendor_costs":None,
    }


def scenarios():
    for n in HORIZONS:
        for rate in RATES:
            for factor in REPEAT_FACTORS:
                for fade in DEGRADATIONS:
                    for opex in ANNUAL_OPEX:
                        yield Scenario(
                            horizon_years=n,real_discount_rate=rate,
                            historical_saving_repeat_fraction=factor,
                            annual_saving_fade_fraction=fade,
                            added_annual_opex_year_eur=opex,
                        )


def build(source_cases):
    need(set(source_cases)==set(YEARS),
         "no implicit source-year mixing, both independent replay years needed")
    result=[]
    for year in YEARS:
        c=source_cases[year]
        for s in scenarios():
            val=frontier(c["source_annual_saving_eur"],
                         c["source_solver_only_lower_eur"],
                         c["source_solver_only_upper_eur"],s)
            result.append({
                "source_year":year,
                "scenario_description":"HYPOTHETICAL constant historic-year EUR; NOT a projected electricity price path",
                "horizon_years":s.horizon_years,
                "real_discount_rate":s.real_discount_rate,
                "assumed_annual_repetition_fraction_of_HISTORICAL_wholesale_saving":
                    s.historical_saving_repeat_fraction,
                "hypothetical_year_on_year_annual_savings_fade":s.annual_saving_fade_fraction,
                "added_annual_incremental_OPEX_hypothetical_year_eur":
                    s.added_annual_opex_year_eur,
                "hypothetical_test_all_in_CAPEX_year_eur":s.hypothetical_initial_capex_year_eur,
                "real_installed_all_in_incremental_CAPEX_supplier_verified":None,
                "real_incremental_OPEX_supplier_verified":None,
                "scenario_2022_and_2024_EUR_units_are_NOT_exchangeable":True,
                **val,
            })
    need(len(result)==2*len(HORIZONS)*len(RATES)*len(REPEAT_FACTORS)*
         len(DEGRADATIONS)*len(ANNUAL_OPEX),
         "prespecified economic scenario grid incomplete")
    benchmark={}
    for year in YEARS:
        c=source_cases[year]
        base=Scenario(horizon_years=20,real_discount_rate=.08,
                      historical_saving_repeat_fraction=1.,
                      added_annual_opex_year_eur=250000.)
        repl=Scenario(horizon_years=20,real_discount_rate=.08,
                      historical_saving_repeat_fraction=1.,
                      added_annual_opex_year_eur=250000.,
                      replacements=((10,REPLACEMENT_BENCHMARK_EUR),))
        benchmark[str(year)]={
            "original_historical_year_currency_label":c["currency_basis"],
            "original_source_model_wholesale_savings_eur":c["source_annual_saving_eur"],
            "same_hydrogen_daily_tonnes":30.,
            "annual_delivered_H2_kg":c["annual_h2_kg"],
            "without_replacement":frontier(c["source_annual_saving_eur"],
                                           c["source_solver_only_lower_eur"],
                                           c["source_solver_only_upper_eur"],base),
            "with_END_OF_YEAR_10_hypothetical_1M_eur_replacement":
                frontier(c["source_annual_saving_eur"],
                         c["source_solver_only_lower_eur"],
                         c["source_solver_only_upper_eur"],repl),
        }
    return {
        "schema_version":SCHEMA,
        "source_public_crossyear_Git_blob_SHA1":SOURCE_GIT_BLOB,
        "source_historical_years":[2022,2024],
        "source_storage_capacity_semantics":"max_inventory",
        "modelled_H2_delivery_tonnes_per_day":30.,
        "modelled_original_year_wind_electric_POWER_multiplier":.9,
        "projected_future_electricity_price_distribution_supplied":False,
        "manufacturer_supplier_verified_incremental_all_in_CAPEX_eur":None,
        "manufacturer_supplier_verified_incremental_annual_OPEX_eur":None,
        "hardware_specific_replacement_schedule_verified":False,
        "BAFU_native_v11_incremental_inventory_and_LCIA_verified":False,
        "no_claim_of_profitable_actual_storage_investment":True,
        "no_source_years_averaged_or_future_expected_savings_implied":True,
        "all_scenarios_are_disclosed_assumptions_NOT_supplier_cost_estimates":True,
        "accounting":"t=0 incremental all-in CAPEX; end-of-year benefits/OPEX/replacements; final-year net salvage/decommission; constant source-year EUR assumed purchasing power and REAL discount",
        "grid_specification":{
            "life_years":list(HORIZONS),"real_discount_rates":list(RATES),
            "fraction_of_original_source_year_savings":list(REPEAT_FACTORS),
            "annual_saving_degradation_fraction":list(DEGRADATIONS),
            "analyst_assumed_incremental_annual_OPEX_year_eur":list(ANNUAL_OPEX),
            "illustrative_CAPEX_for_inverse_OPEX_frontier_year_eur":BENCHMARK_CAPEX,
            "grid_replacement_events":"none; explicit 1M EUR in year 10 benchmark is separate",
        },
        "matched_hydrogen_product_evidence":source_cases,
        "two_year_assumption_scenario_grid":result,
        "explicit_replacement_sensitivity_at_20_years_real_8pct_250k_annual_OPEX":
            benchmark,
        "actual_site_storage_financial_feasibility_admitted":False,
        "scientific_v1_0_economic_gate_passed":False,
    }


def markdown(record):
    b=record["explicit_replacement_sensitivity_at_20_years_real_8pct_250k_annual_OPEX"]
    lines=[
        "# L3-E: exogenous H30/W090 source-year storage CAPEX/OPEX break-even frontiers",
        "",
        "Source: published 2022 and 2024 30 tonnes H2/day, 90% original modeled "
        "wind ELECTRIC POWER independent E20t/E+S40t integer/electricity/EOS "
        "replay. The yearly monetary figures are NOT site profit.",
        "",
        "**Benchmark assumptions (NOT vendor costs):** 20 years, 8% real "
        "discount, 100% hypothetical annual repetition of the specified "
        "historical-source wholesale cost reduction, €250,000/year added "
        "incremental operating cost, €10,000,000 illustrative initial "
        "incremental CAPEX, no salvage/decommission. Historical nominal "
        "source-year EUR units are treated as separate hypothetical constant "
        "purchasing-power scenarios; they are NOT an inflation-adjusted forecast.",
        "",
        "| Conditional source-year illustration | 2022-like source year | 2024-like source year |",
        "|---|---:|---:|",
    ]
    for label,key in (
        ("Published annual E minus E+S net WHOLESALE electricity saving EUR",
         "original_source_model_wholesale_savings_eur"),
        ("Zero-NPV all-in extra installed CAPEX ceiling EUR, NO replacement",
         "without_replacement"),
    ):
        if isinstance(b["2022"][key],dict):
            v22=b["2022"][key]["hypothetical_extra_all_in_installed_CAPEX_zero_NPV_ceiling_year_eur"]
            v24=b["2024"][key]["hypothetical_extra_all_in_installed_CAPEX_zero_NPV_ceiling_year_eur"]
        else:
            v22=b["2022"][key];v24=b["2024"][key]
        lines.append(f"| {label} | {v22:,.2f} | {v24:,.2f} |")
    v22=b["2022"]["with_END_OF_YEAR_10_hypothetical_1M_eur_replacement"][
        "hypothetical_extra_all_in_installed_CAPEX_zero_NPV_ceiling_year_eur"]
    v24=b["2024"]["with_END_OF_YEAR_10_hypothetical_1M_eur_replacement"][
        "hypothetical_extra_all_in_installed_CAPEX_zero_NPV_ceiling_year_eur"]
    lines.extend([
        f"| Zero-NPV CAPEX ceiling EUR with extra €1m replacement END-year 10 | {v22:,.2f} | {v24:,.2f} |",
        "",
        "The ceiling is NOT a manufacturer price and does NOT imply profitable "
        "investment. Real manufacturer/Supplier all-in CAPEX, annual OPEX, "
        "inspection/replacement/decommission, freight, P&ID, pressure-vessel "
        "certification, net grid tariffs and real offtake terms are UNKNOWN. "
        "A positive conditional CAPEX ceiling is not an observed project NPV.",
        "",
        "The complete JSON contains **324** fully labelled hypothetical "
        "discount-horizon-OPEX-repeat/degradation combinations, for each "
        "source year separately, and source HiGHS reported COST-BOUND intervals "
        "that are NOT weather/market forecast uncertainty bands. "
        "It never averages 2022 and 2024 monetary values.",
        "",
        "No native BAFU:2026 v1.1 verified foreground manufacturing or "
        "replacement impacts, complete manufacturer equipment BOM or "
        "scientific whole-project v1.0 are established.",
        "",
    ])
    return "\n".join(lines)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,default=SOURCE)
    p.add_argument("--output-dir",type=Path,default=ROOT/"data/results")
    v=p.parse_args(argv)
    results=build(load_admitted_source(v.source))
    dest=Path(v.output_dir)
    need(dest.is_dir() and not dest.is_symlink(),
         "source repo public output location must already exist")
    files=[
        (dest/OUT_JSON,json.dumps(results,sort_keys=True,indent=2,allow_nan=False)+"\n"),
        (dest/OUT_MD,markdown(results)),
    ]
    for path,body in files:
        need(not path.is_symlink() and (not path.exists() or
             (path.is_file() and path.read_text(encoding="utf-8")==body)),
             "immutable scientific DCF report already exists but differs; stop")
    for path,body in files:
        if not path.exists():
            with path.open("x",encoding="utf-8",newline="\n") as out:
                out.write(body)
    print("L3E_EXOGENOUS_2022_2024_SOURCE_LOCKED_INCREMENTAL_CAPEX_OPEX_DCF_COMPLETE",
          "grid",len(results["two_year_assumption_scenario_grid"]),
          "separate nominal historic-year currency assumptions; NOT actual site NPV")
    for name in (OUT_JSON,OUT_MD):
        print("UNTRACKED_PUBLIC_RESEARCH_SCENARIO_CANDIDATE",name)


if __name__=="__main__":
    main()
