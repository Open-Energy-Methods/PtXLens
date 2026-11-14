"""F3-D: independently gate 8 full-year ORIGINAL 2023 source-derived hourly wind/
price re-optimizations in PtXLens and carry ONLY certified matched-H2 2023
WHOLESALE electricity differences into conditional L3-A DCF scenarios.

No 2022/2024 new historical market data, no future forecast. For -10%
source wind, lack of an accepted MILP incumbent is NOT a proof of
mathematical infeasibility, nor evidence of ES economic preference.
All 8 source JSON SHA values frozen from actual successful PtXFlex GitHub
Actions original ZIP/StageA source full 8760h pair reoptimizations.
"""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import math

from .f3c_common_service_bridge import compare_all_modes
from .l3a_source_wholesale_dcf import constant_scenario,pv_components,source_bound_capex_interval,read_verified_inputs

ROOT=Path(__file__).resolve().parents[2]
SCHEMA="ptxlens.f3d_eight_source_2023_price_wind_counterfactuals_verified_numerical_operating_response.v1"
F3D_SCHEMA="ptxflex.f3d_2023_source_hourly_joint_price_wind_paired_equalH2_counterfactual_stress.v1"
MODE_SHAS={
 "max_inventory":"8e0d55994c7fe5f1abd952771a1b169336893d12698147fb3a93cb61a4ee7a16",
 "usable_service":"6a30baf00ddb065cd906dedd711db7cbf67504c50b4fda5809c5dfd29b23fa87"
}
ORIGINAL_STAGEA={
 "max_inventory":"6731bdaeeaa01a531f577150815dcf6638c15d21bc0ccee5e9ac0fa748ffe3c8",
 "usable_service":"18dec140df7cab63dd9cae8836e3f23fd2dcfb0370acd48db0e36e6af81813cd"
}
SOURCE_FILES={
 "max_inventory":{
   "price_circular_168h":"20d594047a5729bf2c64b7dc4f3c36e97520bfb0ed35e559f4ce16bf84d3f265",
   "price_centered_spread_150":"81e562f6032e1602537e922adc217c307f214a435d0e65c1b0a538f925a08d01",
   "wind_090_multiplier":"9eae6f2deb45d940019d549878f4ad8a27bd61c59a391f702ad1998e93c53b99",
   "wind_110_multiplier":"6c6608bfb6cfb1a18523c6ca7cacd728d1cf350624458f0cd74d9ed8aacd2610",
 },
 "usable_service":{
   "price_circular_168h":"5a621e8384c2e4f1c29f71bba09f7444d4368456f0a5a95042caef3f7593c6ea",
   "price_centered_spread_150":"68723ac550b4a1a093ec7172d7981f5d1782e5223ea6f262b32d83699a065810",
   "wind_090_multiplier":"ff25a1fc99392e6997751ee8a3d82e2a9bc35a100348bd1fd68e2774ed030295",
   "wind_110_multiplier":"2325ecb23bf572ec8628720f6b865b8c85007adad44832ec0e54f0c868ce3dd6",
 }
}
SCENARIOS=("price_circular_168h","price_centered_spread_150","wind_090_multiplier","wind_110_multiplier")
MAIN_SRC_E="069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051"
MAIN_SRC_ES="cd4101fe62c3f1b8aa2d7508d3651d2fee40d2bafe6d5b87e40d5f4d055070f9"


class UnqualifiedCounterfactualEconomicFinding(ValueError):pass

def require(ok,message):
    if not ok:raise UnqualifiedCounterfactualEconomicFinding(message)


def source_one(mode,scenario):
    require(mode in SOURCE_FILES and scenario in SOURCE_FILES[mode],
            "unregistered source scenario or H2 capacity interpretation")
    path=ROOT/"data/results"/f"F3_D_2023_{mode}_{scenario}_COUNTERFACTUAL_NOT_other_observed_year.json"
    raw=path.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==SOURCE_FILES[mode][scenario],
            "authentic original 2023 PtXFlex F3D E/E+S optimization source SHA changed")
    x=json.loads(raw)
    require(x.get("schema_version")==F3D_SCHEMA and x.get("source_observed_year")==2023 and
            x.get("scenario_id")==scenario and x.get("capacity_semantics")==mode and
            x.get("original_source_E_archive_SHA256")==MAIN_SRC_E and
            x.get("original_source_ES_archive_SHA256")==MAIN_SRC_ES and
            x.get("original_source_StageA_archive_SHA256")==ORIGINAL_STAGEA[mode] and
            x.get("original_2023_hourly_E_feasible_common_H2_target_SHA256")==MODE_SHAS[mode],
            "original 2023 source H2 service/scenario attribution invalid")
    require(x.get("counterfactual_not_an_independently_verified_historical_weather_or_market_year") is True and
            x.get("source_stageA_shortage_constructive_not_globally_minimal") is True and
            x.get("actual_new_2022_or_2024_observed_pairing") is False and
            x.get("same_source_2023_h2_product_service_and_market_wind_for_E_ES") is True and
            x.get("source_full_original_2023_industrial_contract_kg")==18250000 and
            x.get("original_full_contract_H2_still_unserved_kg")>1900000 and
            x.get("manufacturer_fully_installed_20t_incremental_storage_CAPEX_eur") is None and
            x.get("actual_incremental_non_grid_opex_eur") is None and
            x.get("matched_native_BAFU_GWP_per_kg_H2") is None and
            x.get("whole_plant_economic_GWP_and_v1_0_release_PASSED") is False,
            "counterfactual 2023 full-v1 project, real 2024 market or station quote incorrectly claimed")
    p=x.get("source_2023_input_price_and_wind_provenance")
    require(isinstance(p,dict) and
            all(len(p.get(k,""))==64 for k in (
              "source_price_2023_float64_sha256",
              "source_wind_2023_float64_sha256",
              "scenario_price_float64_sha256",
              "scenario_wind_float64_sha256"
            )) and p.get("market_price_2023_redistributed") is False and
            p.get("is_alternative_observed_price_or_wind_year") is False,
            "raw source market price redistributed or source 8760h arrays not hash-proven")
    require(x["transformation_method"]["id"]==scenario and
            x["transformation_method"]["weather_year_as_actual_other_year"] is False,
            "scenario was relabelled as a real new year")
    certified=x.get("both_H2_source_cases_certified_MIP_gap_le_1e6") is True
    for case in ("E","E_plus_S"):
        c=x[case]
        if certified:
            require(c.get("solver_outcome")=="CERTIFIED_HIGHS_RELATIVE_GAP_LE_1E6" and
                    c.get("source_2023_hourly_H2_target_proven_feasible_under_this_wind_stress") is True and
                    c.get("source_TypeI_screened_200bar_pressure_OK") is True and
                    0<=c.get("maximum_independent_hourly_residual",999)<2e-4 and
                    math.isclose(c["modelled_H2_delivered_kg"],x["source_same_hourly_modelled_H2_year_kg"],abs_tol=.002) and
                    c.get("no_actual_2023_vendor_or_dynamically_qualified_compressor") is True,
                    "independently source-certified 8760h E and ES solver status/physical control inconsistent")
        else:
            require(c.get("solver_outcome") in ("NO_ACCEPTED_INCUMBENT_OR_FAILED_UNKNOWN","FEASIBLE_BUT_UNCERTIFIED","CERTIFIED_HIGHS_RELATIVE_GAP_LE_1E6"),
                    "uncertified solution must not be called physical infeasibility")
    if certified:
        estimate=x["paired_modelled_incremental_EplusS_wholesale_saving_eur2023_COUNTERFACTUAL_not_forecast"]
        low,high=x["paired_modelled_source_HiGHS_error_saving_bounds_eur2023"]
        require(all(isinstance(v,(int,float)) and math.isfinite(v) for v in (estimate,low,high)) and
                low<=estimate<=high and high-low<100 and
                math.isclose(estimate,x["E"]["cost_modelled_counterfactual_eur2023"]-
                x["E_plus_S"]["cost_modelled_counterfactual_eur2023"],abs_tol=.001),
                "source paired E minus E+S price objective or global optimum-bound invalid")
    else:
        require(x.get("paired_modelled_incremental_EplusS_wholesale_saving_eur2023_COUNTERFACTUAL_not_forecast") is None and
                x.get("paired_modelled_source_HiGHS_error_saving_bounds_eur2023") is None,
                "must not compare unequal or uncertified case costs or label infeasibility proven")
    return x


def synthesize_independent_comparison():
    source=compare_all_modes()
    _,finance_cases=read_verified_inputs()
    require(source.get("source_year")==2023 and source["l1_l2_l3_v1_0_RELEASE_PASSED"] is False,
            "independent 2023 F3C source replay and L3 release mismatch")
    rows=[]
    for mode in ("max_inventory","usable_service"):
        baseline=source["modes"][mode]
        require(baseline["reference_common_hourly_H2_float64_sha256"]==MODE_SHAS[mode] and
                finance_cases[mode]["frozen_8760hour_H2_service_float64_sha256"]==MODE_SHAS[mode],
                "original F3C original H2 baseline does not match 2023 historical stress")
        reference=baseline["EplusS_2023_wholesale_saving_eur"]
        assert reference>1e6
        for scenario in SCENARIOS:
            x=source_one(mode,scenario)
            require(abs(x["source_same_hourly_modelled_H2_year_kg"]-
                        baseline["reference_common_annual_modelled_service_kg"])<.002,
                    "modified 2023 price/wind scenario changed common hourly H2 service annual volume")
            ok=x["both_H2_source_cases_certified_MIP_gap_le_1e6"]
            estimated=x["paired_modelled_incremental_EplusS_wholesale_saving_eur2023_COUNTERFACTUAL_not_forecast"]
            dcf=None
            if ok:
                require(estimated is not None and estimated>=0,
                        "certified stress may be negative; if this fires remove monotonicity assumption and preserve actual sign")
                s=constant_scenario(estimated,years=20,r=.08,repeat_factor=1,annual_opex_eur=0)
                cost=pv_components(s)
                dcf=cost["max_initial_all_in_incremental_capex_at_zero_NPV_eur"]
                interval=source_bound_capex_interval(s,x["paired_modelled_source_HiGHS_error_saving_bounds_eur2023"])
                require(interval[0]<=dcf<=interval[1] and dcf>0,
                        "2023 transformed source MIP cost bounds not captured in conditional capital frontier")
            else:
                interval=None
                require(estimated is None,"unknown optimization result cannot propagate into threshold")
            rows.append({
                "source_capacity_semantics":mode,
                "source_2023_counterfactual_stress_id":scenario,
                "original_2023_F3C_reference_wholesale_EplusS_saving_eur":reference,
                "source_2023_counterfactual_wholesale_EplusS_saving_eur":estimated,
                "source_2023_counterfactual_source_solver_saving_interval_eur":
                      x["paired_modelled_source_HiGHS_error_saving_bounds_eur2023"],
                "difference_from_original_source2023_EplusS_wholesale_saving_eur":
                      None if estimated is None else estimated-reference,
                "relative_source_benefit_to_original_source2023":
                      None if estimated is None else estimated/reference,
                "conditional_20y_8pct_no_extra_cost_C0_max_eur_2023_basis":dcf,
                "conditional_20y_8pct_no_extra_cost_C0_minmax_due_ONLY_to_solver_gap_eur":interval,
                "future_2023_model_difference_repeats_each_year_NOT_forecast":True,
                "historical_source_file_sha256":SOURCE_FILES[mode][scenario],
                "signed_full_2023_hourly_H2_service_sha256":MODE_SHAS[mode],
                "both_cases_solver_optimality_certified_to_1e6":ok,
                "undetermined_is_not_mathematical_infeasibility":not ok,
                "both_E_ES_met_same_hourly_H2_target_if_certified":True if ok else None,
                "source_year":2023,
                "independent_new_market_and_wind_year":False,
                "full_2023_original_industrial_demand_satisfied":False,
                "manufacturer_CAPEX_EUR_or_site_LCOH_GWP":None,
            })
    require(len(rows)==8 and sum(row["both_cases_solver_optimality_certified_to_1e6"] for row in rows)==6,
            "F3D original 2023 4 stress×2 source mode solver certificate matrix changed, manual independent review required")
    require(sum(row["undetermined_is_not_mathematical_infeasibility"] for row in rows)==2,
            "missing -10% wind inconclusive cannot be relabelled as economic loss or physical infeasibility")
    return {
      "schema_version":SCHEMA,
      "programme":"OEM-PTX-2026-01",
      "original_observed_weather_and_market_year":2023,
      "zero_independently_observed_new_2022_2024_price_wind_pairs_retrieved":True,
      "price_wind_counterfactuals_NOT_observed_new_years":True,
      "source_valid_original_2023_weekly_price_phase_change_and_spread_stress":True,
      "source_wind_multiplier_090_110_does_not_physically_recalculate_ERA5_turbine_powers":True,
      "source_target_constructive_feasible_not_global_maximum":True,
      "full_2023_18p25mkg_industrial_contract_satisfied":False,
      "source_2023_E_ES_2023_real_grid_wholesale_only_not_full_TEA_or_GWP":True,
      "certified_matched_source_year_scenarios_count":6,
      "unknown_result_short_wind_source_scenarios_count":2,
      "market_robustness_therefore_NOT_a_predictive_confidence_interval":True,
      "future_F3D_external_years_still_blocked":True,
      "manufacturer_installed_extra_20t_typeI_storage_cost_eur":None,
      "native_BAFU2026_v11_exact_matched_source_LCIA_kgCO2e":None,
      "full_true_hydrogen_LCOH_and_plant_preference":None,
      "scientific_v1_full_release_passed":False,
      "rows":rows
    }
