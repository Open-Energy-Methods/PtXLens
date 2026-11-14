"""L3-A: source-2023 same-hour E/E+S wholesale-only incremental DCF frontiers.

The source operating benefit is EXACTLY the matched 2023 F3-C *modelled net
WHOLESALE GRID settlement* reduction, under one feasible (not globally
maximum) common-hour hydrogen target for each DISTINCT storage semantics.
No future Dutch power market forecast, vendor storage costs, added compressor
auxiliary, manufacturing BOM, full electricity emissions or full plant H2 LCOH.

This module answers only conditional thresholds:
  given hypothetically repeated 2023 wholesale difference, what extra
  ALL-IN installed CAPEX could be tolerated for explicit discount/lifetime/
  hypothetical annual incremental OPEX and replacement/salvage assumptions?

All money is constant 2023-EUR: REAL cash flows require REAL discount rate.
Capital is booked t=0, operating cash flows end years 1..N; replacement
events are paid at the year end in which they occur, residual and
decommission at t=N. No taxes, depreciation or financing. Explicitly
distinct from DOE H2A complete hydrogen selling-price DCF.

All original F3-C and F2 JSON files MUST PASS SHA and independent source
physical accounting before any threshold calculation is admissible.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
from typing import Optional

from .f3c_common_service_bridge import compare_all_modes, BRIDGE_SCHEMA, REGISTERED

ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/"research/L3_A_2023_source_locked_incremental_wholesale_DCF_handoff_v1.json"
SCHEMA="ptxlens.l3a_source2023_equal_hourly_h2_incremental_wholesale_only_DCF_frontier.v1"
MANIFEST_SCHEMA="oem.ptx.l3a_2023_physical_hourly_service_wholesale_savings_handoff.v1"
F3C_SHA="dddd07d5c0a3d4f276e80af44e28cf3cfdbc93421107fb5d9e39843a0d1d90e2"
F2_SHA="1315d1181b9d1eab6d3368425c9571dbe295c3360935d2972403bf3c60e2dc47"
MODES=("max_inventory","usable_service")
SOURCE_H2_HASHES={
    "max_inventory":"8e0d55994c7fe5f1abd952771a1b169336893d12698147fb3a93cb61a4ee7a16",
    "usable_service":"6a30baf00ddb065cd906dedd711db7cbf67504c50b4fda5809c5dfd29b23fa87"
}

class InvalidIncrementalCashflow(ValueError):pass


def require(ok,reason):
    if not ok:raise InvalidIncrementalCashflow(reason)


def real_number(v,what,*,min_value=None):
    require(type(v) in (float,int) and math.isfinite(v),"nonfinite or nonnumeric real EUR cash flow: "+what)
    z=float(v)
    if min_value is not None:require(z>=min_value,"negative or unsupported real EUR value: "+what)
    return z


def digest(path):
    p=Path(path)
    require(p.is_file(),"missing immutable original-source derived research artifact: "+str(path))
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_verified_inputs():
    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(m.get("schema_version")==MANIFEST_SCHEMA and
            m.get("original_modelled_hydrogen_source_year")==2023 and
            m.get("money_basis","").startswith("2023 EUR;") and
            m.get("source_research_release_full_v1_allowed") is False,
            "unregistered source year/2023 EUR basis or L3 full release falsely asserted")
    require(m.get("f3c_sha256")==F3C_SHA and m.get("f2_typeI_bom_sha256")==F2_SHA,
            "altered registered 2023 F3C or F2 Type I equipment source")
    require(m.get("original_2023_E_zip_sha256")==
             "069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051" and
            m.get("original_2023_ES_zip_sha256")==
             "cd4101fe62c3f1b8aa2d7508d3651d2fee40d2bafe6d5b87e40d5f4d055070f9",
            "wrong frozen original 2023 E or ES archive")
    require(m.get("strict_modes")==list(MODES),
            "gross and usable bank reference cannot be cross-compared as identical service")
    guard=m.get("not_qualified_claims",{})
    require(guard and len(guard)>=10 and all(v is False for v in guard.values()),
            "source or scenario handoff falsely claims manufacturer full plant verification")
    controls=m.get("scenario_grid_analyst_selected_NOT_vendor_estimates",{})
    expected={
     "life_years":[5,10,15,20,25,30],
     "real_discount_rates":[0,0.03,0.05,0.08,0.12],
     "repeat_2023_savings_factors":[0.25,0.5,0.75,1,1.25,1.5],
     "constant_annual_incremental_opex_2023_eur":[0,250000,500000],
     "hypothetical_replacement_event_year":10,
     "hypothetical_replacement_cost_2023_eur":1000000,
     "benchmark_life_years":20,
     "benchmark_real_discount_rate":0.08,
     "default_terminal_salvage_eur":0,
     "default_terminal_decommission_eur":0
    }
    require(controls==expected,"parameter grid altered without changing source research revision")
    require(m.get("f3c_path")==str(Path("data/results/F3_C_2023_source_real_gas_equal_H2_hour_E_vs_ES_Lens_operational_bridge.json"))
            and m.get("f2_path")==str(Path("data/results/F2_L1_2023_source_incremental_20t_to_40t_stationary_typeI_200bar_BOM_SCOPE_NOT_complete_native_LCI.json")),
            "unexpected research data path")
    f3path=ROOT/m["f3c_path"];f2path=ROOT/m["f2_path"]
    require(digest(f3path)==F3C_SHA and digest(f2path)==F2_SHA,
            "F3-C 2023 hourly service / F2 stationary Type I original source SHA violation")
    f3=json.loads(f3path.read_text(encoding="utf-8"))
    f2=json.loads(f2path.read_text(encoding="utf-8"))
    independent=compare_all_modes()  # verifies 4 original PyNEXUS F3-C results by SHA,
                                     # exact matched hour H2, 2023 money and MIP bounds.
    require(f3==independent and
            f3.get("schema_version")==BRIDGE_SCHEMA and
            f3.get("l1_l2_l3_v1_0_RELEASE_PASSED") is False and
            f3.get("native_BAFU_complete_LCA_and_discounted_LCOH_missing") is True,
            "2023 F3-C source operation not independently verified or falsely declared full DCF")
    require(f2.get("schema_version")==
            "ptxflex.f2_l1_typeI_200bar_incremental_stationary_h2_equipment_requirements.v1" and
            f2.get("full_project_LCA_TE_A_allowed") is False and
            f2.get("modelled_original_PyNEXUS_year")==2023 and
            set(f2.get("modes",{}))==set(MODES),
            "2023 steel-vessel source reference falsely made complete physical hardware")
    cases={}
    for mode in MODES:
        a=f3["modes"][mode]
        b=f2["modes"][mode]
        require(a["reference_common_hourly_H2_float64_sha256"]==SOURCE_H2_HASHES[mode] and
                a["source_data_evidence_sha256"]==REGISTERED[mode] and
                a["operational_saving_can_be_compared_within_mode_not_across_modes"] is True and
                a["actual_economic_preference_or_full_plant_LCA_claim_permitted"] is False and
                a["original_full_demand_kg"]==18250000.,
                "original 2023 hourly product service or commercial boundary drift")
        require(b["capacity_semantics"]==mode and
                b["complete_manufacturer_warrantied_typeI_bank_BOM"] is False and
                b["unknown_non_vessel_equipment_total_mass_kg"] is None and
                b["BAFU2026_v11_standalone_typeI_native_LCI_created"] is False,
                "manufacturer physical cost or native BAFU storage LCI fabricated")
        ref=b["incremental_only_research_sensitivity"]
        require(ref["incremental_installed_storage_CAPEX_eur"] is None and
                ref["incremental_native_BAFU_storage_CO2e_kg"] is None and
                ref["source_vessel_mass_is_NOT_virgin_steel_input_kg"] is True,
                "published empty equipment mass is NOT a 2023 manufacturing/provider cash cost")
        count=ref["net_additional_published_reference_vessel_count"]
        mass=ref["net_additional_published_empty_vessel_equipment_mass_kg"]
        require(type(count) is int and count>0 and mass==count*2400. and
                count==({"max_inventory":802,"usable_service":902}[mode]),
                "F2 313K pressure-swing Type I reference mass invalid")
        require(len(b["required_incremental_system_foreground_BOM"])==19 and
                all(x["empty_mass_kg"] is None and x["manufacturer_quote_eur"] is None
                    for x in b["required_incremental_system_foreground_BOM"][1:]),
                "missing incremental equipment source costs cannot be assumed zero")
        saving=real_number(a["EplusS_2023_wholesale_saving_eur"],"source 2023 savings",min_value=0)
        low,high=(real_number(z,"solver bound") for z in a["EplusS_saving_interval_mip_bounds_eur"])
        require(0<low<=saving<=high and high-low<100,
                "source 2023 exact-hour optimization's objective dual/upper bound invalid")
        cases[mode]={
            "mode":mode,
            "source_2023_net_grid_wholesale_annual_saving_eur":saving,
            "source_2023_net_grid_wholesale_solver_saving_interval_eur":[low,high],
            "source_2023_annual_equal_hour_modelled_H2_kg":a["reference_common_annual_modelled_service_kg"],
            "original_full_2023_contract_unserved_H2_kg":a["remaining_unserved_original_full_contract_kg"],
            "frozen_8760hour_H2_service_float64_sha256":SOURCE_H2_HASHES[mode],
            "reference_incremental_empty_vessel_equipment_mass_kg":mass,
            "reference_incremental_vessels_count":count,
            "existing_vendor_all_in_incremental_installed_capex_eur":None,
            "actual_opex_replacement_disposal_schedules_eur":None,
            "source_full_LCOH_or_2026_native_BAFU_GWP":None
        }
    # Independent original PtXFlex economic handoff: a separate producer
    # checks the SAME original hourly F3C and F2 source JSON and serialises
    # only the 2023-wholesale hardware source boundary.  This new L3-A
    # consumer MUST reject it if its bytes or case content diverge.
    handoff_path=ROOT/"data/results/L3_A_PtXFlex_2023_source_hourly_equal_service_wholesale_only_financial_handoff.json"
    handoff_expected="0de22f7ff566dc50101b085366e47ef9965d545dca1dfa9bca3dd6d115274829"
    require(digest(handoff_path)==handoff_expected,
            "PtXFlex original-source financial handoff file SHA mismatch")
    handoff=json.loads(handoff_path.read_text(encoding="utf-8"))
    require(handoff.get("schema_version")==
            "ptxflex.l3a_2023_8760hour_e_vs_es_real_eur_wholesale_annual_evidence_handoff.v1" and
            handoff.get("model_hydrogen_data_year")==2023 and
            handoff.get("source_registered_F3C_2023_original_sha256")==F3C_SHA and
            handoff.get("source_registered_F2_200bar_313K_empty_shell_sha256")==F2_SHA and
            handoff.get("true_plant_vendor_financial_result_or_full_LCOH_permitted") is False,
            "original PyNEXUS source production cashflow boundary is not authentic")
    source_modes=handoff.get("distinct_source_capacity_interpretations")
    require(isinstance(source_modes,dict) and set(source_modes)==set(MODES),
            "original PtXFlex source economic handoff has wrong H2 capacity semantics")
    for mode in MODES:
        original=source_modes[mode];actual=cases[mode]
        require(original.get("registered_source_mode")==mode and
            original.get("original_E_modelled_feasible_not_maximum_same_hourly_H2_hash")==
                actual["frozen_8760hour_H2_service_float64_sha256"] and
            abs(original.get("same_hourly_reduced_modelled_H2_kg_year",0)-
                actual["source_2023_annual_equal_hour_modelled_H2_kg"])<.002 and
            abs(original.get("2023_wholesale_only_annual_saving_eur",0)-
                actual["source_2023_net_grid_wholesale_annual_saving_eur"])<1e-4 and
            original.get("source_solver_proved_annual_wholesale_saving_bounds_eur")==
                actual["source_2023_net_grid_wholesale_solver_saving_interval_eur"] and
            original.get("source_literature_extra_empty_typeI_200bar_vessel_equipment_mass_kg")==
                actual["reference_incremental_empty_vessel_equipment_mass_kg"] and
            original.get("vendor_installed_actual_INCREMENTAL_CAPEX_eur") is None and
            original.get("true_extra_annual_OPEX_and_maintenance_eur") is None and
            original.get("source_2023_wholesale_difference_is_NOT_2026_future_revenue_forecast") is True,
            "original PtXFlex source equipment+H2-2023 financial export disagrees with independent PtXLens")
    return m,cases


@dataclass(frozen=True)
class CashflowScenario:
    life_years:int
    real_discount_rate:float
    source_annual_wholesale_saving_eur:float
    saving_factors:tuple[float,...]
    incremental_annual_opex_eur:tuple[float,...]
    replacement_events_year_eur:tuple[tuple[int,float],...]=()
    terminal_salvage_eur:float=0.
    terminal_decommission_eur:float=0.

    def __post_init__(self):
        require(type(self.life_years) is int and 1<=self.life_years<=60,
                "end-of-year horizon must be integer 1..60 years")
        r=real_number(self.real_discount_rate,"real discount rate",min_value=0)
        require(r<1.0,"illustrative real rate must be <100%")
        real_number(self.source_annual_wholesale_saving_eur,"2023 modelled wholesale saving",min_value=0)
        require(len(self.saving_factors)==self.life_years and
                len(self.incremental_annual_opex_eur)==self.life_years,
                "one scalar cash flow per END of year required (no terminal invisible year)")
        for year,(s,o) in enumerate(zip(self.saving_factors,self.incremental_annual_opex_eur),start=1):
            real_number(s,"nonnegative 2023-repeat factor year "+str(year),min_value=0)
            real_number(o,"nonnegative incremental OPEX year "+str(year),min_value=0)
        require(isinstance(self.replacement_events_year_eur,tuple),
                "replacement schedule must be tuple of (year, expenditure EUR2023)")
        seen=set()
        for item in self.replacement_events_year_eur:
            require(isinstance(item,tuple) and len(item)==2,"invalid replacement event")
            year,amount=item
            require(type(year) is int and 1<=year<=self.life_years and year not in seen,
                    "replacement cannot occur at t0, outside service life, or duplicated at same year")
            seen.add(year)
            real_number(amount,"replacement capital",min_value=0)
        real_number(self.terminal_salvage_eur,"residual/salvage",min_value=0)
        real_number(self.terminal_decommission_eur,"decommission",min_value=0)


def constant_scenario(source_saving_eur,*,years=20,r=0.08,repeat_factor=1.,
                      annual_opex_eur=0.,replacements=(),
                      terminal_salvage_eur=0.,terminal_decommission_eur=0.):
    return CashflowScenario(
        life_years=years,real_discount_rate=r,
        source_annual_wholesale_saving_eur=source_saving_eur,
        saving_factors=(repeat_factor,)*years,
        incremental_annual_opex_eur=(annual_opex_eur,)*years,
        replacement_events_year_eur=tuple(replacements),
        terminal_salvage_eur=terminal_salvage_eur,
        terminal_decommission_eur=terminal_decommission_eur,
    )


def discount_factors(s):
    return tuple((1.+s.real_discount_rate)**(-y)
                 for y in range(1,s.life_years+1))


def pv_components(s):
    factors=discount_factors(s)
    rep=dict(s.replacement_events_year_eur)
    ledger=[]
    for year,df in enumerate(factors,start=1):
        wholesale=s.source_annual_wholesale_saving_eur*s.saving_factors[year-1]
        opex=s.incremental_annual_opex_eur[year-1]
        repl=rep.get(year,0.)
        salvage=s.terminal_salvage_eur if year==s.life_years else 0.
        decom=s.terminal_decommission_eur if year==s.life_years else 0.
        gross=wholesale-opex-repl+salvage-decom
        ledger.append({
            "year_index":year,"discount_factor":df,
            "conditional_replayed_wholesale_saving_eur":wholesale,
            "analyst_hypothetical_incremental_opex_eur":opex,
            "analyst_hypothetical_replacement_eur":repl,
            "analyst_hypothetical_terminal_salvage_eur":salvage,
            "analyst_hypothetical_decommission_eur":decom,
            "total_incremental_end_of_year_cashflow_before_initial_capex_eur":gross,
            "present_value_incremental_end_of_year_cashflow_before_initial_capex_eur":gross*df,
        })
    positive_pv=sum(x["conditional_replayed_wholesale_saving_eur"]*x["discount_factor"] for x in ledger)
    opex_pv=sum(x["analyst_hypothetical_incremental_opex_eur"]*x["discount_factor"] for x in ledger)
    replace_pv=sum(x["analyst_hypothetical_replacement_eur"]*x["discount_factor"] for x in ledger)
    salvage_pv=sum(x["analyst_hypothetical_terminal_salvage_eur"]*x["discount_factor"] for x in ledger)
    decom_pv=sum(x["analyst_hypothetical_decommission_eur"]*x["discount_factor"] for x in ledger)
    ceiling=positive_pv-opex_pv-replace_pv+salvage_pv-decom_pv
    require(abs(ceiling-sum(x["present_value_incremental_end_of_year_cashflow_before_initial_capex_eur"] for x in ledger))<
            max(1.e-6,abs(ceiling)*1.e-11),"independent source cashflow-year PV arithmetic does not close")
    return {
      "pv_source_2023_replay_annual_wholesale_savings_eur":positive_pv,
      "pv_hypothetical_incremental_noncapital_opex_eur":opex_pv,
      "pv_hypothetical_replacement_capital_eur":replace_pv,
      "pv_hypothetical_terminal_salvage_eur":salvage_pv,
      "pv_hypothetical_terminal_decommission_eur":decom_pv,
      "sum_end_of_year_discount_factors_annuity":sum(factors),
      "max_initial_all_in_incremental_capex_at_zero_NPV_eur":ceiling,
      "nonnegative_initial_capex_feasible_if_all_scenario_cashflows_realised":ceiling>=0,
      "cashflow_years":ledger
    }


def npv_at_assumed_installed_capex(s,all_in_initial_capex_eur):
    investment=real_number(all_in_initial_capex_eur,"unverified hypothetical installed capex",min_value=0)
    return pv_components(s)["max_initial_all_in_incremental_capex_at_zero_NPV_eur"]-investment


def break_even_uniform_annual_opex(s,assumed_initial_all_in_capex_eur):
    """Solve for OPEX while keeping every other cashflow unchanged.

    Given s may already contain a nonzero annual OPEX path, add back its PV
    first; the result is the TOTAL flat annual amount that would produce
    zero NPV. Negative thresholds mean even zero additional OPEX cannot
    break even for the assumed CAPEX and other scenario losses.
    """
    investment=real_number(assumed_initial_all_in_capex_eur,"illustrative installed capex",min_value=0)
    v=pv_components(s)
    annuity=v["sum_end_of_year_discount_factors_annuity"]
    require(annuity>0,"invalid discount factor annuity")
    return (v["max_initial_all_in_incremental_capex_at_zero_NPV_eur"]+
            v["pv_hypothetical_incremental_noncapital_opex_eur"]-investment)/annuity


def source_bound_capex_interval(s,annual_source_cost_bound):
    lo,hi=annual_source_cost_bound
    lo=real_number(lo,"HiGHS source 2023 lower saving",min_value=0)
    hi=real_number(hi,"HiGHS source 2023 upper saving",min_value=0)
    require(lo<=s.source_annual_wholesale_saving_eur<=hi and hi-lo<100.,
            "wrong 2023 MIP optimum source-bound or physical service")
    baseline=pv_components(s)
    # Savings factors are explicitly constrained >=0 for monotone interval
    pv_multiplier=sum(m*df for m,df in zip(s.saving_factors,discount_factors(s)))
    rest=baseline["max_initial_all_in_incremental_capex_at_zero_NPV_eur"]-(
        s.source_annual_wholesale_saving_eur*pv_multiplier)
    lower=lo*pv_multiplier+rest
    upper=hi*pv_multiplier+rest
    require(lower<=baseline["max_initial_all_in_incremental_capex_at_zero_NPV_eur"]+1e-7<=upper+1e-7,
            "source lower/upper solver bounds must contain source incumbent CAPEX ceiling")
    return [lower,upper]


def scenario_surface_for_mode(mode,case,grid):
    saving=case["source_2023_net_grid_wholesale_annual_saving_eur"]
    bounds=case["source_2023_net_grid_wholesale_solver_saving_interval_eur"]
    def extract(s,*,label,opex_eur,example_capex=None):
        v=pv_components(s)
        return {
          "mode":mode,"scenario_identifier":label,
          "years":s.life_years,"real_discount_rate":s.real_discount_rate,
          "hypothetical_constant_repeat_factor":s.saving_factors[0]
                if len(set(s.saving_factors))==1 else None,
          "annual_opex_assumed_eur":opex_eur,
          "replacement_events_hypothetical_year_and_eur":[list(q) for q in s.replacement_events_year_eur],
          "terminal_salvage_assumed_eur":s.terminal_salvage_eur,
          "terminal_decommission_assumed_eur":s.terminal_decommission_eur,
          "conditional_capex_ceiling_eur":v["max_initial_all_in_incremental_capex_at_zero_NPV_eur"],
          "conditional_capex_ceiling_solver_bound_eur":source_bound_capex_interval(s,bounds),
          "pv_net_grid_wholesale_savings_eur":v["pv_source_2023_replay_annual_wholesale_savings_eur"],
          "pv_hypothetical_opex_eur":v["pv_hypothetical_incremental_noncapital_opex_eur"],
          "pv_hypothetical_replacements_eur":v["pv_hypothetical_replacement_capital_eur"],
          "conditional_assumed_installed_capex_eur":example_capex,
          "conditional_npv_at_assumed_capex_eur":None if example_capex is None
                        else npv_at_assumed_installed_capex(s,example_capex),
          "missing_actual_station_CAPEX_eur":None,
          "not_original_full_demand_contract_served":True,
          "not_full_hydrogen_LCOH_or_vendor_investment_case":True,
        }
    comparison=[]
    for n in grid["life_years"]:
        for rate in grid["real_discount_rates"]:
            s=constant_scenario(saving,years=n,r=rate,annual_opex_eur=0.)
            comparison.append(extract(s,label="zero_OPEX_no_replacement_OPTIMISTIC_UPPER_ENVELOPE",opex_eur=0.))
    persistence=[]
    for factor in grid["repeat_2023_savings_factors"]:
        for op in grid["constant_annual_incremental_opex_2023_eur"]:
            s=constant_scenario(saving,years=20,r=0.08,repeat_factor=factor,annual_opex_eur=op)
            persistence.append(extract(s,label="future_repeated_source_saving_factor_and_unknown_OPEX_scenarios",opex_eur=op))
    reference=constant_scenario(saving,years=20,r=0.08)
    ref=extract(reference,label="20yr_8pct_2023_replay_ZERO_extra_opex_theoretical_ceiling_not_vendor",opex_eur=0.)
    ref["year_1_to_20_cashflow_ledger"]=pv_components(reference)["cashflow_years"]
    ref["conditional_annual_opex_break_even_at_0_CAPEX_eur"]=break_even_uniform_annual_opex(reference,0.)
    ref["conditional_wholesale_difference_eur_per_kg_matched_hourly_H2"]=(
       saving/case["source_2023_annual_equal_hour_modelled_H2_kg"])
    ref["hardware_reference_ceiling_eur_per_kg_EMPTY_vessel_equipment_if_all_other_COSTS_ZERO"]=(
       ref["conditional_capex_ceiling_eur"]/case["reference_incremental_empty_vessel_equipment_mass_kg"])
    ref["hardware_reference_ceiling_per_kg_is_NOT_market_steel_PRICE"]=True
    zero_opex_replacement=constant_scenario(saving,years=20,r=.08,annual_opex_eur=250000.,
                                             replacements=((10,1000000.),))
    replacement=extract(zero_opex_replacement,label="20yr_8pct_2023_replay_250k_EUR_annual_extra_OPEX_plus_1M_EUR_year10_replacement_HYPOTHETICAL",
                        opex_eur=250000.)
    opex_frontier=[]
    for initial_capex in (0,2000000,5000000,8000000,10000000,12000000,15000000,20000000):
        opex_frontier.append({
            "mode":mode,"scenario_life_years":20,"real_discount_rate":.08,
            "initial_incremental_all_in_capex_hypothetical_eur":initial_capex,
            "max_flat_annual_extra_OPEX_eur_to_zero_NPV":break_even_uniform_annual_opex(reference,initial_capex),
            "negative_opex_ceiling_means_even_zero_extra_OPEX_fails_at_that_capex":True,
            "full_2023_real_replay_is_NOT_forecast":True
        })
    return {
       "source_capacity_semantics":mode,
       "source_2023_modelled_8760h_equal_delivery_hydrogen_kg":case["source_2023_annual_equal_hour_modelled_H2_kg"],
       "source_2023_full_contract_unserved_hydrogen_kg":case["original_full_2023_contract_unserved_H2_kg"],
       "original_F3C_2023_8760hour_target_sha256":case["frozen_8760hour_H2_service_float64_sha256"],
       "source_2023_wholesale_annual_savings_eur":saving,
       "source_2023_wholesale_difference_solver_interval_eur":bounds,
       "source_F2_reference_additional_empty_equipment_mass_kg":case["reference_incremental_empty_vessel_equipment_mass_kg"],
       "future_price_history_annual_repetition_HYPOTHETICAL_not_forecast":True,
       "conditional_20yr_8pct_zero_extra_cost_theoretical_capex_ceiling":ref,
       "conditional_20yr_8pct_cost_and_replacement_sensitivity":replacement,
       "discount_lifetime_zero_extra_COST_OPTIMISTIC_upper_envelope":comparison,
       "annual_opex_vs_installed_capex_20yr_8pct_break_even_frontier":opex_frontier,
       "source_2023_wholesale_persistence_factor_and_opex_sensitivity":persistence,
       "source_actual_manufacturer_capex_and_opex":None,
       "gwp_LCOH_and_true_investment_NPV":None,
       "complete_economic_release_allowed":False
    }


def make_all():
    m,cases=read_verified_inputs()
    grid=m["scenario_grid_analyst_selected_NOT_vendor_estimates"]
    result={
      "schema_version":SCHEMA,
      "programme":"OEM-PTX-2026-01",
      "evidence_date_utc":"2026-11-14",
      "source_year_of_hydrogen_model_weather_and_electricity_price":2023,
      "reference_money_basis":"2023 real EUR under explicitly hypothetical constant-purchasing-power future projection",
      "DCF_zero_time":"before service starts; hypothetical initial extra installed capital",
      "cashflow_time":"end of each hypothetical service year; replacement at end of stated service year; terminal salvage and decommission at year N",
      "DCF_scope":"pre-tax unlevered incremental SOURCE-2023 WHOLESALE GRID settlement frontiers only; not a DOE H2A full aftertax model",
      "illustrative_analyst_parameter_grid_not_real_price_vendor_engineering_forecast":grid,
      "fixed_source_F3C_sha256":F3C_SHA,
      "fixed_source_F2_typeI_200bar_hardware_sha256":F2_SHA,
      "original_2023_E_and_ES_source_8760h_profiles_matched_within_each_mode":True,
      "2023_source_annual_electricity_difference_not_forecast_future_power_prices":True,
      "source_hydrogen_plant_and_2026_supplier_not_real_validated_site":True,
      "two_modes_different_hourly_H2_functional_units_not_a_single_cost_comparison":True,
      "no_original_18250000_kg_H2_full_contract_delivery":True,
      "no_actual_supplier_quote_or_price_or_station_cost":True,
      "annual_2023_historical_repeated_WHOLSALE_savings_model_NOT_reoptimized_for_future_prices":True,
      "scenario_opex_zero_is_THEORETICAL_upper_ceiling_not_a_real_plant_assumption":True,
      "replacement_cost_if_shown_is_analyst_choice_NOT_vendor_quote":True,
      "missing_discounted_tax_financing_depreciation_insurance_and_risk":True,
      "source_body_manufacturer_steel_and_18_other_equip_classes_missing":True,
      "native_full_2026_BAFU_stationary_typeI_GWP":None,
      "complete_hydrogen_whole_plant_LCOH":None,
      "actual_installed_incremental_capex":None,
      "actual_incremental_lifetime_NPV":None,
      "scientific_L3_full_release_PASSED":False,
      "per_distinct_capacity_semantics":{
        mode:scenario_surface_for_mode(mode,cases[mode],grid) for mode in MODES
      }
    }
    for mode,row in result["per_distinct_capacity_semantics"].items():
        anchor=row["conditional_20yr_8pct_zero_extra_cost_theoretical_capex_ceiling"]
        require(anchor["conditional_capex_ceiling_solver_bound_eur"][0]<=
                anchor["conditional_capex_ceiling_eur"]<=
                anchor["conditional_capex_ceiling_solver_bound_eur"][1],
                "source-year MIP interval no longer bounds discounted illustrative result")
        require(row["source_actual_manufacturer_capex_and_opex"] is None and
                row["gwp_LCOH_and_true_investment_NPV"] is None,
                "real plant economics or environmental suitability fabricated")
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    out=Path(a.output)
    if out.exists():raise FileExistsError("never overwrite source-locked L3-A DCF scenario results")
    result=make_all()
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    for mode,x in result["per_distinct_capacity_semantics"].items():
        cap=x["conditional_20yr_8pct_zero_extra_cost_theoretical_capex_ceiling"]
        print(mode,"annual 2023 modelled net wholesale EUR difference",x["source_2023_wholesale_annual_savings_eur"])
        print(mode,"20yr 8pct real repeat 2023 zero-extra-OPEX/replacement max all-in CAPEX EUR",
              cap["conditional_capex_ceiling_eur"],"source MIP EUR bounds",
              cap["conditional_capex_ceiling_solver_bound_eur"])
        print(mode,"20yr 8pct +250k/yr OPEX +1m replacement year10 max all-in CAPEX EUR",
              x["conditional_20yr_8pct_cost_and_replacement_sensitivity"]["conditional_capex_ceiling_eur"])
    print("L3-A conditional mathematical frontiers ONLY. No vendor CAPEX/OPEX, real investment NPV, full LCOH or full native BAFU GWP.")
if __name__=="__main__":main()
