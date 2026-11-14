"""L3-B peer-reviewed 2024 tank-only cost and native BAFU v1.1 LCI gates.

Two source-backed facts can be quantified WITHOUT making a vendor quote:
(1) Ademollo et al. IJHE (2026), Table 2: nominal 200bar(g) Type I
    1.8m3, 26 kg H2/vessel, 2400kg empty, 222 EUR2024 per kg nominal H2;
    all reference equipment costs are 2024-harmonized literature estimates.
(2) BAFU v1.1 native 2023 Dutch scenario 30bar PEM reference has an actual
    executed source fingerprint, but DOES NOT include incremental storage
    manufacturing nor MATCHED every-hour E vs ES source H2 service.

No company has quoted the actual installation, service pressure, grade,
BoP mass or EUR. BAFU v1 automotive composite H2 tank process unit 'kg'
represents PER KG HYDROGEN CAPACITY, not kg empty Type I steel equipment.
Never silently estimate the unpriced installation, 2024-to-2023 deflator,
full GWP/LCOH, compressor mass/cost, or actual financial viability.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REGISTER=ROOT/"research/L3_B_2024_PEER_REVIEWED_TYPEI_200BAR_TANK_COST_NOT_VENDOR_AND_BAFU_V11_GAP_v1.json"
F2=ROOT/"data/results/F2_L1_2023_source_incremental_20t_to_40t_stationary_typeI_200bar_BOM_SCOPE_NOT_complete_native_LCI.json"
L3=ROOT/"data/results/L3_A_2023_same_service_2023_wholesale_DCF_break_even_summary_NOT_final_project.json"
BAFU=ROOT/"data/results/BAFU2026_v11_native_E_ES_2023_verified_summary.json"
SCHEMA="ptxlens.l3b_2024_paper_tank_reference_2023_source_l3a_GWP_provider_STOP.v1"
F2_SHA="1315d1181b9d1eab6d3368425c9571dbe295c3360935d2972403bf3c60e2dc47"
L3_SHA="89a10d1f10b5317f335fd4db042b7133cccc849ec8174a847fa000b9b9a58de3"
V1_COMPOSITE_TANK="b4739ad2-aa38-368d-8ada-63f5417c8b55"


class InvalidSupplierOrLCAQualification(ValueError): pass


def require(ok,reason):
    if not ok:raise InvalidSupplierOrLCAQualification(reason)


def source_bytes(path,sha=None):
    raw=Path(path).read_bytes()
    if sha is not None:
        require(hashlib.sha256(raw).hexdigest()==sha,"source original equipment or real EUR2023 economic evidence SHA mismatch")
    return json.loads(raw)


def load_source():
    manifest=source_bytes(REGISTER)
    require(manifest.get("schema_version")==
            "oem.ptx.l3b_l1_native_2024_literature_typeI_capex_supplier_quote_and_bafu_gate.v1" and
            manifest.get("evidence_source_class")==
            "PEER_REVIEWED_2024_HARMONIZED_LITERATURE_COST_NOT_MANUFACTURER_QUOTE" and
            manifest.get("source_does_not_permit_full_v1_0_release") is True,
            "non-peer-reviewed price or fake manufacturer quote")
    paper=manifest["original_reference"]
    require(paper["doi"]=="10.1016/j.ijhydene.2025.152849" and
            paper["source_nominal_tank_capacity_h2_kg_per_vessel"]==26 and
            paper["specific_cost_eur_per_kg_h2_rated_nominal"]==222 and
            paper["reported_empty_vessel_kg"]==2400 and
            paper["harmonized_cost_price_year"]==2024 and
            paper["source_pressure_basis"].startswith("200bar GAUGE") and
            paper["actual_supplier_quoted_price_eur"] is None and
            paper["actual_vendor_nominal_200bar_absolute_313K_validated"] is False and
            paper["report_wide_costs_harmonized_2024_values"] is True,
            "paper source currency year, geometry, gauge-vs-absolute or real-vendor status changed")
    costs=manifest["cost_interpretation"]
    require(costs["per_vessel_literature_reference_cost_eur2024"]==26*222 and
            costs["gross_F2_additional_reference_vessels"]==802 and
            costs["usable_F2_additional_reference_vessels"]==902 and
            costs["price_2024_to_real_2023_currency_year_conversion_factor"] is None and
            costs["direct_comparison_of_2024_paper_cost_with_2023_discount_ceiling_without_deflator_forbidden"] is True and
            costs["existing_E_compressor_may_be_reused_or_have_incremental_train_cost_unknown"] is True,
            "unverified incremental compressor cost or 2024/2023 price-year conversion")
    src=source_bytes(F2,F2_SHA)
    l3=source_bytes(L3,L3_SHA)
    native=source_bytes(BAFU)
    bafum=manifest["native_BAFU_2026_v11_original"]
    require(native["schema_version"]=="ptxlens.bafu_2026_v1_1_nl_2023_native_gwp100_v1" and
            native["source"]["bafu_native_original_zolca_sha256"]==
                bafum["source_database_original_zolca_sha256"] and
            native["native_method"]["name"]=="IPCC 2021" and
            native["native_method"]["exact_impact_category"]=="IPCC 2021 GWP 100" and
            native["native_method"]["functional_unit"]=="1 kg H2 at original BAFU 30bar PEM reference gate" and
            native["scenario_model_changes"]["additional_e_plus_s_tank_material_equipment_included"] is False and
            native["scientific_claims"]["full_2023_nl_E_vs_ES_matched_service_comparison_completed"] is False and
            native["scientific_claims"]["E_native_LCIA_executed"] is True and
            native["scientific_claims"]["E_plus_S_native_LCIA_executed"] is True,
            "native v1.1 PEM reference 2023 H2 technology and boundary mismatch")
    require(bafum["native_compatible_F2_typeI_sourced_steel_material_process_uuid"] is None and
            bafum["native_compatible_F2_manufacturing_raw_alloy_mass_from_actual_OEM"] is None and
            bafum["native_compatible_BOP_compressor_civil_maintenance_provider_map"] is None and
            bafum["source_BAFU_v1_vehicle_composite_tank_UUID_inadmissible"]==V1_COMPOSITE_TANK and
            bafum["can_calculate_genuine_incremental_2023_matched_service_BAFU_GWP"] is False,
            "vehicle-composite tank per kg H2 incorrectly mapped to per kg raw steel")
    return manifest,src,l3,native


def evaluate_cost_source_boundaries():
    meta,f2,l3,bafu=load_source()
    p=meta["original_reference"]
    result={}
    for mode in ("max_inventory","usable_service"):
        r=f2["modes"][mode]
        n=r["incremental_only_research_sensitivity"]["net_additional_published_reference_vessel_count"]
        source_empty=r["incremental_only_research_sensitivity"]["net_additional_published_empty_vessel_equipment_mass_kg"]
        require(n==meta["cost_interpretation"]["gross_F2_additional_reference_vessels" if mode=="max_inventory" else "usable_F2_additional_reference_vessels"] and
                source_empty==n*2400 and
                r["commercial_manufacturer_candidate"]["stationary_module_empty_mass_kg"] is None and
                r["complete_manufacturer_warrantied_typeI_bank_BOM"] is False,
                "source 200bar Type I reference quantity was replaced by vendor 330bar or 210bar component")
        source_cost=n*p["source_nominal_tank_capacity_h2_kg_per_vessel"]*p["specific_cost_eur_per_kg_h2_rated_nominal"]
        scenario=l3["source_F3C_modes"][mode]
        require(scenario["additional_literature_empty_vessel_equipment_kg_NOT_steel_foreground"]==source_empty and
                scenario["zero_extra_cost_CAPEX_ceiling_implies_no_real_storage_design"] is True,
                "L3-A 2023 original reference empty vessel mass or economic source scope mismatch")
        require(l3["true_project_incremental_NPV_eur"] is None and
                l3["complete_LCOH_eur_per_kg_H2"] is None and
                scenario["zero_extra_cost_CAPEX_ceiling_implies_no_real_storage_design"] is True,
                "L3-A reported conditional 2023 EUR ceiling mistaken for observed project investment")
        result[mode]={
          "source_capacity_semantics":mode,
          "source_2023_modelled_same_H2_annual_wholesale_benefit_eur":
             scenario["2023_wholesale_annual_saving_eur_not_a_forecast"],
          "source_published_2024_journal_nominal_pressure_class_bar_GAUGE":200,
          "source_F3_pressure_model_max_bar_ABSOLUTE":200,
          "source_literature_reference_26kg_per_vessel_at_nominal_pressure_class":True,
          "F2_E20t_to_ES40t_additional_1p8m3_200bar_reference_empty_vessels_count":n,
          "source_paper_nominal_H2_capacity_kg_on_added_reference_vessels":26*n,
          "source_paper_nominal_empty_equipment_mass_kg_not_raw_steel":source_empty,
          "source_literature_tank_only_2024_EUR":source_cost,
          "source_literature_2024_EUR_per_kg_H2_nominal_capacity":222,
          "source_literature_tank_cost_proven_vendor_quoted_eur":None,
          "source_reference_paper_bare_cost_includes_all_18_other_BOP_plant_scope_classes":False,
          "installed_source_2024_extra_compressor_and_cooler_and_rack_cost_EUR":None,
          "real_2024_to_2023_currency_year_factor":None,
          "source_2023_L3_A_20y8pct_ZERO_OPEX_hypothetical_installed_CAPEX_ceiling_EUR2023":
            scenario["no_extra_cost_hypothetical_capex_ceiling_eur"],
          "paper_2024_tank_cost_vs_L3A_2023_breakeven_comparable_without_price_year_and_scope_adjustment":False,
          "manufacturer_actual_all_in_incremental_CAPEX_EUR":None,
          "manufacturer_actual_annual_OPEX_EUR":None,
          "matched_native_2026_BAFU_v11_added_TypeI_storage_LCI_kgCO2e":None,
          "2023_true_investment_NPV_and_LCOH_EUR":None,
          "source_only_not_a_vendor_quote_nor_full_LCA":True
        }
    return {
      "schema_version":SCHEMA,"programme":"OEM-PTX-2026-01",
      "paper_DOI":p["doi"],"source_eur_reference_year":2024,
      "original_hourly_modelled_economic_source_year":2023,
      "source_200bar_reference_paper_rating_is_gauge_while_F3_model_is_absolute":True,
      "price_year_conversion_unprovided_and_not_inferred":True,
      "no_supplier_quote_or_real_safety_conformity_or_steel_fabrication_footprint":True,
      "source_F2_SHA256":F2_SHA,"source_L3A_economic_SHA256":L3_SHA,
      "BAFU_2026_v11_native_30bar_PEM_source_archive_sha256":
          bafu["source"]["bafu_native_original_zolca_sha256"],
      "BAFU_native_reference_2023_original_E_and_ES_not_matched_H2_service":
          [dict(case=x["id"],gwp_per_kg_at_30bar_PEM_H2=x["native_gwp100_kgco2e_per_kg_model_delivered_h2"],
                modelled_annual_H2_kg=x["modelled_2023_delivered_h2_kg"])
           for x in bafu["historical_2023_original_scenarios"]],
      "BAFU_v1_vehicle_composite_per_kg_H2_capacity_not_steel_mass_provider_UUID":V1_COMPOSITE_TANK,
      "actual_complete_2023_H2_same_hour_BAFU_v11_GWP_per_kg":None,
      "actual_full_manufacturer_BOM_quote_and_economic_preference_allowed":False,
      "modes":result
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    args=p.parse_args()
    out=Path(args.output)
    if out.exists():raise FileExistsError("do not overwrite immutable paper/nested BAFU cost boundary evidence")
    report=evaluate_cost_source_boundaries()
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    for m,r in report["modes"].items():
        print(m,"IJHE source nominal 200bar(g) tank only 2024-EUR paper cost",r["source_literature_tank_only_2024_EUR"],
              "NOT actual vendor installed quote or comparable to 2023 real-EUR DCF without deflator.")
    print("Native BAFU2026 v1.1 original 30bar PEM reference exists, but new stationary 200bar tank and matched-hour H2 full native LCA NOT EXECUTED.")
if __name__=="__main__":main()
