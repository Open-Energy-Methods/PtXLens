"""L3-E / L1: foreground hardware and native BAFU scope for H30/W090 E→E+S.

This is NOT an LCA calculator. It source-verifies the original 19-category
Type-I 20→40t incremental 200bar reference-hardware scope and attaches the
identical exogenous 30t/day independently replayed 2022 and 2024 functional
unit. It reports unknown installed quoted costs, steel/manufacturing inputs,
replacement inventories and BAFU v1.1 native exchange links as NULL, NOT 0.

The earlier F2 **2023 source reference** (802 extra hypothetical reference
vessels at 2400kg EMPTY HARDWARE per unit, 1,924,800kg empty equipment) is
a geometric/pressure reference, NOT a 2022/2024 delivered manufacturer bill,
virgin-steel raw-material input, pressure-certified final bank, actual quote,
or lifecycle GWP. Every non-vessel balance-of-plant category is unknown.

Native provider mapping requires an independently authenticated actual
BAFU:2026 v1.1 process, reference product, exchange quantity, unit, geography,
manufacturer-produced material/fabrication mass and full reproducible openLCA
result; a filled JSON questionnaire is not sufficient certification.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from .l3d_bafu_incremental_inventory_gate import (
    inspect_original, PINNED_SOURCE_GIT_BLOB_SHA, verify_future_complete_native_mapping,
)
from .l3e_exogenous_incremental_dcf import (
    load_admitted_source, SOURCE_GIT_BLOB, ROOT, need,
)

SCHEMA="ptxlens.l3e_exogenous_H30_W090_source_F2_19line_incremental_hardware_BAFU_2026_foreground_contract.v1"
OUT_JSON="L3E_H30_W090_INCREMENTAL_STATIONARY_20t_to_40t_HARDWARE_AND_BAFU_FOREGROUND_NOT_LCIA_v1.json"
OUT_MD="L3E_H30_W090_INCREMENTAL_STATIONARY_HARDWARE_AND_BAFU_SCOPE_NOT_LCIA_v1.md"
MODE="max_inventory"
REQUIRED=19
REFERENCE_VESSELS=802
REFERENCE_EMPTY_KG=1924800.


def build():
    economic=load_admitted_source()
    need(set(economic)=={2022,2024} and
         economic[2022]["annual_h2_kg"]==10950000. and
         economic[2024]["annual_h2_kg"]==10980000.,
         "cross-year matched exogenous H2 functional unit changed")
    d=inspect_original()
    need(d.get("schema_version")==
         "ptxlens.f2_l1_bafu_2026_native_incremental_storage_inventory_admission_ledger.v1" and
         d.get("source_F2_hardware_Git_blob_SHA1")==PINNED_SOURCE_GIT_BLOB_SHA and
         d.get("native_BAFU_2026_whole_station_manufacturing_emissions_kgCO2e") is None and
         d.get("manufacturer_actual_installed_system_BOM_and_price_verified") is False,
         "source original F2 hardware or incomplete BAFU evidence falsely certified")
    rows=[r for r in d["ledger"] if r["mode"]==MODE]
    need(len(rows)==REQUIRED and
         len({x["line_id"] for x in rows})==REQUIRED and
         rows[0]["line_id"]=="typeI_200bar_bare_reference_vessels" and
         rows[0]["reference_only_empty_equipment_mass_kg"]==REFERENCE_EMPTY_KG and
         rows[0]["reference_vessel_count_ONLY_not_fabricated_bill_of_materials"]==
            REFERENCE_VESSELS and
         all(x["independent_material_composition_or_manufacturer_mass_kg"] is None
             and x["manufacturer_quotation_eur"] is None and
             x["native_BAFU_2026_dataset_process_UUID"] is None for x in rows),
         "original 19 line source BOM reference or missing-data contract changed")
    scoped=[]
    for r in rows:
        is_vessel=r["index"]==0
        is_maintenance=r["line_id"]=="inspections_fatigue_cycle_testing"
        is_eol=r["line_id"]=="decommission_and_EOL"
        line={
            "line_id":r["line_id"],
            "original_source_scope_category":r["system"],
            "original_hardware_source_reference_id":r["source_reference_id"],
            "original_research_item_description":r["original_scope_description"],
            "per_line_incremental_role":
                ("inspection_recurrent" if is_maintenance else
                 "end_of_life" if is_eol else "installed_incremental_or_replacement"),
            "model_reference_802_vessel_count_ONLY_if_line_is_vessel":
                REFERENCE_VESSELS if is_vessel else None,
            "model_reference_empty_equipment_mass_kg_NOT_steel_input":
                REFERENCE_EMPTY_KG if is_vessel else None,
            "actual_manufacturer_installed_quantity":None,
            "actual_manufacturer_installed_quantity_unit":None,
            "actual_manufacturer_material_grade_or_parts":None,
            "actual_manufactured_material_input_kg":None,
            "actual_material_sourcing_scrap_and_process_yield":None,
            "actual_fabrication_process_and_supplier_geography":None,
            "actual_manufacturer_equipment_empty_mass_kg":None,
            "actual_site_installed_equipment_mass_kg":None,
            "actual_supplier_all_in_initial_cost_eur":None,
            "actual_incremental_yearly_maintenance_OPEX_eur":None,
            "actual_replacement_years_and_manufacturing_quantities":None,
            "actual_decommissioning_processing_and_transport":None,
            "manufacturer_signed_source_revision_document_sha256":None,
            "manufacturer_certified_design_pressure_basis_absolute_or_gauge":None,
            "manufacturer_standards_PED_ATEX_evidence":None,
            "native_BAFU_2026_v11_original_zolca_SHA256":None,
            "native_BAFU_2026_v11_actual_process_UUID":None,
            "native_BAFU_2026_v11_technosphere_exchange_provider_UUID":None,
            "native_BAFU_2026_v11_reference_product_UUID":None,
            "native_BAFU_2026_v11_reference_unit":None,
            "native_BAFU_2026_v11_input_exchange_amount_in_real_reference_unit":None,
            "native_BAFU_2026_v11_process_geography":None,
            "native_BAFU_2026_v11_LCIA_method_UUID":None,
            "native_BAFU_2026_v11_LCIA_GWP_kgCO2e_incremental_manufacturing":None,
            "native_BAFU_2026_v11_LCIA_GWP_kgCO2e_replacements":None,
            "manufacturer_quote_admitted":False,
            "process_material_flow_admitted":False,
            "native_provider_link_independently_verified":False,
            "native_LCIA_computed_and_replayed":False,
            "zero_unknown_material_or_cost_or_LCIA_assumed":False,
        }
        scoped.append(line)
    return {
        "schema_version":SCHEMA,
        "model_hydrogen_functional_unit":
            "exact original 30t/day supplied at each UTC hour by E20t and EplusS40t within each historical year",
        "source_year_hydrogen_normalization":[
            {"year":y,"source_year_UTC_hours":8760 if y==2022 else 8784,
             "delivered_H2_kg":economic[y]["annual_h2_kg"],
             "same_daily_service_for_E20t_and_EplusS40t":True}
            for y in (2022,2024)
        ],
        "physical_storage_model":"stationary Type I H2 20-200 bar(a) original max_inventory capacity semantics; pressure screening NOT certified manufacturer PED",
        "source_2022_2024_independent_same_product_cost_Git_blob":SOURCE_GIT_BLOB,
        "source_F2_2023_bare_vessel_reference_Git_blob":PINNED_SOURCE_GIT_BLOB_SHA,
        "reference_vessel_mass_kg_EMPTY_EQUIPMENT_NOT_virgin_steel":
            REFERENCE_EMPTY_KG,
        "reference_additional_vessel_count_NOT_qualified_site_bank":REFERENCE_VESSELS,
        "reference_incremental_nominal_H2_bank_delta_kg":20000.,
        "actual_supplier_installed_vessel_quantity":None,
        "actual_manufacturer_total_incremental_material_input_kg":None,
        "actual_manufacturer_total_installed_CAPEX_eur":None,
        "actual_added_annual_OPEX_eur":None,
        "actual_replacement_years_and_costs":None,
        "native_BAFU_database_identity_source":"BAFU:2026 v1.1 original openLCA database",
        "native_BAFU_independently_linked_process_and_LCIA_total_GWP_kgCO2e":None,
        "native_matched_2022_annual_H2_lifecycle_GWP_delta_kgCO2e_per_kg":None,
        "native_matched_2024_annual_H2_lifecycle_GWP_delta_kgCO2e_per_kg":None,
        "native_manufacturing_plus_replacement_plus_EOL_total_kgCO2e":None,
        "source_steel_total_virgin_material_kg_may_NOT_be_inferred_from_empty_mass":True,
        "manufacturer_material_and_process_certification_required":True,
        "real_supplier_quote_and_pressure_approval_required":True,
        "native_BAFU_original_provider_activity_and_units_required":True,
        "full_environmental_result_ready":False,
        "project_installed_cost_qualified":False,
        "scientific_v1_0_environmental_release_allowed":False,
        "nineteen_research_equipment_and_evidence_lines":scoped,
    }


def native_LCIA_release_check(document):
    """A matched-service questionnaire cannot certify a real BAFU provider map.

    Source gate expects its original F2/L1 schema, not the new L3-E
    questionnaire schema. Reopen the source and explicitly delegate to
    that independent native-provider proof gate, which currently refuses
    any full LCIA. Do not confuse a schema mismatch with proof of BAFU.
    """
    need(type(document) is dict and document.get("schema_version")==SCHEMA,
         "L3-E source/evidence hardware schema differs")
    source_evidence=inspect_original()
    verify_future_complete_native_mapping(source_evidence)


def markdown(d):
    lines=[
        "# L3-E: source-linked incremental Type I hydrogen storage equipment / BAFU inventory scope",
        "",
        "Additional nominal H2 storage model: E20t to E+S40t, original 20-200 bar(a) "
        "stationary Type I, max_inventory interpretation. Matched H2 service "
        "fixed at 30 t/day (2022: 10,950,000kg; 2024: 10,980,000kg).",
        "",
        "The earlier published F2 2023 pressure-swing reference implies **802 additional "
        "reference cylinders with 1,924,800kg aggregate EMPTY EQUIPMENT mass**. "
        "This is NOT site vendor vessel count, virgin steel manufacturing input, "
        "verified OEM vessel mass, pressure vessel design, fabrication scrap yield, "
        "BAFU reference exchange or lifecycle GWP. BoP masses/quantities are unknown.",
        "",
        "| Foreground reference scope | Equipment quantity evidence | "
        "Actual all-in quoted cost | Native BAFU process/exchange and LCIA |",
        "|---|---|---|---|",
    ]
    for row in d["nineteen_research_equipment_and_evidence_lines"]:
        count=("802 PAPER REFERENCE ONLY" if row[
            "model_reference_802_vessel_count_ONLY_if_line_is_vessel"] is not None
               else "UNKNOWN")
        lines.append(f"| {row['line_id']} | {count} | UNKNOWN | NOT ADMITTED |")
    lines+=["",
        "Other missing controls: manufacturer product geometry/material grade, "
        "certified 20–200bar absolute vs gauge pressure, design temperature, "
        "working volume, PED/ATEX, site supports, compression/cooling/venting, "
        "inspections, replacement life, freight, installation, EOL and quote scope.",
        "",
        "For BAFU:2026 v1.1, each real manufactured foreground item additionally "
        "requires source-verified original native provider process UUID, exact "
        "reference product/unit and exchange coefficient, actual source BOM "
        "material/fabrication/waste flows, region, replacement and EOL links, "
        "a selected native LCIA method and independently rerun openLCA results. "
        "A source-verified questionnaire is still NOT a native LCIA.",
        "",
        "No current manufacturing impact, kgCO2e/kg delivered hydrogen, "
        "investment price, real-site viability or scientific v1.0 is asserted.",
        "",
    ]
    return "\n".join(lines)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",type=Path,default=ROOT/"data/results")
    a=parser.parse_args(argv)
    output=Path(a.output_dir)
    need(output.is_dir() and not output.is_symlink(),
         "expected immutable project public research output directory")
    d=build()
    targets=[
        (output/OUT_JSON,json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+"\n"),
        (output/OUT_MD,markdown(d)),
    ]
    for path,body in targets:
        need(not path.is_symlink() and
             (not path.exists() or (path.is_file() and
              path.read_text(encoding="utf-8")==body)),
             "previous source-linked foreground report differs; prevent overwrite")
    for path,body in targets:
        if not path.exists():
            with path.open("x",encoding="utf-8",newline="\n") as f:
                f.write(body)
    print("L3E_EXOGENOUS_SOURCE_H30_TWO_YEAR_TYPEI_19_LINE_INCREMENTAL_SCOPE_COMPLETE",
          "802 bare reference vessels / 1924800 kg EMPTY EQUIPMENT only",
          "supplier installed CAPEX unknown; native BAFU LCA blocked")
    print("EVIDENCE_MANIFEST_CREATED_NOT_NATIVE_LCIA_OR_SITE_QUOTE")


if __name__=="__main__":
    main()
