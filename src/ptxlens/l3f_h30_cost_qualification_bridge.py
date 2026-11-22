"""L3-F source-locked qualified-CAPEX readiness and 2022/24 H30 frontier bridge.

Reuses original independently replayed 2022/24 matched-H2 E/E+S wholesale
cost source and existing *conditional* L3-E DCF. Separately crosswalks
the source-F2 original 19 equipment/BoP item cost roles to the unpriced,
public-safe PtXFlex OEM intake and prospective site qualification.

A source-locked, reproducible zero-NPV CAPEX threshold is not an
authenticated OEM-installed equipment price. No real paid quote, cost
currency conversion, life, maintenance, finance or site commissioning is
invented, and no inflated 2024/2022 EUR conversion is implied.

When a private ledger is supplied, perform an integrity/coverage
precheck only; private evidence must remain outside Git. Even 19 filled
signed-SHA entries do not establish original supplier authenticity,
quote scope/site compatibility, procurement entitlement or native BAFU.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from . import l3e_exogenous_incremental_dcf as dcf
from ptxflex import f2l3e_exogenous_vendor_cost_intake as vendor
from ptxflex import f2l3f_stationary_site_evidence_gate as site

ROOT=Path(__file__).resolve().parents[2]
SCHEMA="ptxlens.l3f_H30_2022_2024_19_equipment_evidence_to_conditional_zero_NPV_crosswalk.v1"
OUT_JSON="L3F_H30_2022_2024_19_EQUIPMENT_COST_EVIDENCE_TO_DCF_GATE_NOT_PROJECT_NPV_v1.json"
OUT_MD="L3F_H30_INCREMENTAL_INSTALLED_COST_2022_2024_EVIDENCE_BRIDGE_NOT_NPV_v1.md"


def build():
    source=dcf.load_admitted_source()
    base=vendor.make()
    contract=site.make_contract()
    original=base["nineteen_required_supplier_and_site_intake_lines"]
    physical=contract["original_19_equipment_qualification_lines"]
    dcf.need(len(original)==19 and
             [x["line_id"] for x in original]==[x["line_id"] for x in physical] and
             source[2022]["annual_h2_kg"]==10950000. and
             source[2024]["annual_h2_kg"]==10980000.,
             "19-line original supplier/physical source or matched H30 functional service changed")
    lines=[]
    for vendor_line,physical_line in zip(original,physical):
        cost_role=vendor_line["cost_role"]
        category=vendor_line["line_id"]
        lines.append({
            "original_F2_line_id":category,
            "original_source_reference_id":vendor_line["original_requirement_source"],
            "accounting_role_for_supplier_comparison":cost_role,
            "incremental_real_supplier_initial_CAPEX_EUR":None,
            "incremental_real_supplier_annual_OPEX_EUR":None,
            "incremental_real_supplier_replacement_schedule_EUR":None,
            "incremental_real_supplier_EOL_liability_EUR":None,
            "actual_supplier_price_year_and_currency":None,
            "actual_original_quote_receipt_SHA256":None,
            "actual_site_installed_quantity_and_pressure_design_proven":False,
            "actual_manufacturer_pressure_qualification_proven":False,
            "original_source_quote_audited_bytes_and_scope":False,
            "original_source_equipment_material_BOQ_verified":False,
            "real_supplier_price_can_be_used_in_NPV":False,
            "original_802_pressure_vessel_count_is_ONLY_paper_reference":
                category=="typeI_200bar_bare_reference_vessels",
        })
    examples={}
    for y in (2022,2024):
        model=source[y]
        scenarios={}
        for repeat in (0.50,0.75,1.):
            assumed=dcf.Scenario(
                horizon_years=20,real_discount_rate=.08,
                historical_saving_repeat_fraction=repeat,
                added_annual_opex_year_eur=250000.,
                replacements=((10,1000000.),)
            )
            v=dcf.frontier(model["source_annual_saving_eur"],
                           model["source_solver_only_lower_eur"],
                           model["source_solver_only_upper_eur"],assumed)
            scenarios[f"{repeat:.2f}"]={
                "hypothetical_annual_source_wholesale_saving_fraction":repeat,
                "assumed_annual_extra_OPEX_year_eur":250000.,
                "assumed_END_year_10_replacement_year_eur":1000000.,
                "zero_NPV_maximum_incremental_all_in_CAPEX_year_eur":
                    v["hypothetical_extra_all_in_installed_CAPEX_zero_NPV_ceiling_year_eur"],
                "source_MIP_numerical_bounds_only_not_market_uncertainty":
                    v["hypothetical_extra_all_in_CAPEX_solver_numerical_lower_upper_year_eur"],
                "verified_manufacturer_OEM_all_in_installed_price_EUR":None,
                "verified_vendor_price_below_capex_ceiling":None,
                "actual_investment_profitable":None,
            }
        examples[str(y)]={
            "separate_source_year_nominal_EUR":y,
            "original_independently_replayed_wholesale_saving_eur":
                model["source_annual_saving_eur"],
            "daily_source_H2_service_tonnes":30.,
            "conditional_discount_assumption":"20y, 8% REAL, annual OPEX 250k, 1m replacement END year10; scenario source money NOT forecast",
            "repeat_fraction_sensitivity":scenarios,
        }
    return {
        "schema_version":SCHEMA,
        "original_2022_2024_matched_service_source_Git_blob":
            dcf.SOURCE_GIT_BLOB,
        "original_typeI_pressure_BOM_Git_blob_sha1":vendor.SOURCE_GIT_BLOB,
        "original_supplier_intake_schema":vendor.SCHEMA,
        "original_site_P_and_ID_PED_duty_intake_schema":site.SCHEMA,
        "source_F2_incremental_20t_gross_not_20t_usable":True,
        "matched_2022_2024_H2_daily_tonnes":30.,
        "non_matching_source_year_EUR_must_not_be_averaged_or_exchanged":True,
        "source_year_conditional_cost_limits":examples,
        "nineteen_site_verified_supplier_installed_scope_lines":lines,
        "all_in_actual_installed_incremental_CAPEX_eur":None,
        "actual_additional_annual_operational_cost_eur":None,
        "actual_site_specific_replacements_and_EOL_cost_schedule":None,
        "independent_signed_OEM_provenance_and_quote_scope_verification":False,
        "source_energy_market_savings_can_be_licensed_or_contractually_realized":False,
        "real_site_price_comparability_price_year_tax_and_currency_verified":False,
        "native_BAFU_2026_v11_manufacturing_LCIA_and_replacement_total":None,
        "site_project_commercial_NPV_authorized":False,
        "scientific_v1_0_cost_and_safety_release_qualified":False,
    }


def review_private_supplier_ledger_without_project_approval(ledger):
    """Documentary status only. Real private original byte receipts are external."""
    reviewed=vendor.review_private_ledger(ledger)
    return {
        "source_supplier_ledger_precheck":reviewed,
        "all_required_private_supplier_original_documents_authenticated":
            False,
        "can_compare_actual_verified_2022_2024_all_in_costs_against_DCF":False,
        "price_year_and_supplier_contractual_rights_verified":False,
        "site_pressure_equipment_conformity_qualified":False,
        "actual_financial_return_inferable":False,
    }


def markdown(d):
    lines=[
        "# L3-F: conditional 2022/2024 extra H2 storage zero-NPV thresholds versus UNKNOWN real OEM CAPEX",
        "",
        "This is a crosswalk between source-locked whole-year 30t/day original H2 "
        "replayed net WHOLESALE ELECTRICITY model savings and 19 original Type I "
        "equipment cost categories. Vendor prices, actually installed quantities, "
        "replacements and service life are NOT included.",
        "",
        "20y, 8% REAL, assumed incremental annual OPEX EUR250k, extra END-year10 "
        "replacement EUR1m; all numbers in each separate source-year's "
        "hypothetical constant-EUR purchasing-power assumption. "
        "Never average historical 2022 and 2024 EUR as future probabilities.",
        "",
        "| Annual assumed fraction of one year's original power-saving repeated | 2022-like max upfront CAPEX EUR | 2024-like max upfront CAPEX EUR |",
        "|---|---:|---:|",
    ]
    a=d["source_year_conditional_cost_limits"]
    for k in ("0.50","0.75","1.00"):
        v22=a["2022"]["repeat_fraction_sensitivity"][k][
            "zero_NPV_maximum_incremental_all_in_CAPEX_year_eur"]
        v24=a["2024"]["repeat_fraction_sensitivity"][k][
            "zero_NPV_maximum_incremental_all_in_CAPEX_year_eur"]
        lines.append(f"| {k} | {v22:,.2f} | {v24:,.2f} |")
    lines.extend([
        "",
        "All **19** published original Type I vessel/structure/manifold/safety/"
        "compressor/thermal/civil/maintenance/EOL cost roles require separately "
        "signed and authenticated manufacturer and site quotations, with "
        "consistent price year, tax/currency, double-count exclusion and "
        "replacement schedule. None are accepted now.",
        "",
        "A positive mathematical CAPEX ceiling does not prove that the "
        "additional 20t MAX-inventory configuration can be procured for "
        "that price, that it meets stationary PED, that annual savings "
        "will repeat or be contractually realized, or that environmental "
        "impact is lower.",
        "",
    ])
    return "\n".join(lines)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",type=Path,default=ROOT/"data/results")
    a=parser.parse_args(argv)
    out=Path(a.output_dir)
    dcf.need(out.is_dir() and not out.is_symlink(),"original source public output unavailable")
    d=build()
    items=[
        (out/OUT_JSON,json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+"\n"),
        (out/OUT_MD,markdown(d)),
    ]
    for p,body in items:
        dcf.need(not p.is_symlink() and
                 (not p.exists() or
                  (p.is_file() and p.read_text(encoding="utf-8")==body)),
                 "source verified financial/vendor crosswalk output differs")
    for p,body in items:
        if not p.exists():
            with p.open("x",encoding="utf-8",newline="\n") as f:f.write(body)
    print("L3F_H30_ORIGINAL_2022_2024_CONDITIONAL_CAPEX_AND_19_OEM_EVIDENCE_CROSSWALK_COMPLETE",
          "real vendor installed prices NULL, actual NPV NOT certified")


if __name__=="__main__":
    main()
