"""L3-F native BAFU:2026 v1.1 foreground-mapping release contract.

Actual BAFU native .zolca database and manufacturer materials are NOT
present in public source results. This tool:
  - source-locks 19 original F2 Type I + BoP line IDs;
  - supplies an explicit same H30 daily H2 per 2022/2024 calendar year
    for manufacturing lifetime allocation, and authenticated original
    full-year operating electricity import/export differences;
  - refuses to infer virgin steel input from 802*2400 kg EMPTY equipment;
  - distinguishes native process UUID, provider product/reference flow,
    exchange direction, unit, geography, fab scrap and true material mass;
  - optionally computes the SHA256 of a LOCAL private user-owned original
    BAFU .zolca compressed archive, but hash/zip integrity alone is NOT
    a native provider UUID query, original BAFU version proof or LCIA.

A JSON questionnaire with all metadata filled does NOT qualify native
BAFU process/production exchange/unit or independently reproduce openLCA.
This gate remains negative until native openLCA source and real OEM
manufacturing inputs are independently interrogated and calculated.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import re
import zipfile
from pathlib import Path

from . import l3e_exogenous_incremental_hardware_lci as hardware
from . import l3e_exogenous_operational_energy_inventory as energy
from .l1_native_manufacturing_unit_gate import audit_manufacturing_functional_unit
from .l3d_bafu_incremental_inventory_gate import NativeInventoryBlocked

ROOT=Path(__file__).resolve().parents[2]
SCHEMA="ptxlens.l3f_h30_2022_2024_original_BAFU2026_v11_native_OEM_and_operations_LCIA_mapping_contract.v1"
OUT_JSON="L3F_H30_2022_2024_BAFU_2026_v11_PROCESS_AND_MATERIAL_MAPPING_NOT_LCIA_v1.json"
OUT_MD="L3F_H30_BAFU_NATIVE_STATIONARY_STORAGE_MAPPING_REQUIREMENTS_NOT_LCIA_v1.md"
UUID_RE=re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89aAbB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$")
SHA_RE=re.compile(r"^[0-9a-f]{64}$")


def build():
    source=hardware.build()
    elect=energy.build()
    ids=source["nineteen_research_equipment_and_evidence_lines"]
    assert len(ids)==19
    assert source["reference_vessel_mass_kg_EMPTY_EQUIPMENT_NOT_virgin_steel"]==1924800.
    assert len(elect["yearly"])==2
    foreground=[]
    for line in ids:
        foreground.append({
            "original_F2_source_BOM_line_id":line["line_id"],
            "physical_scope":line["original_research_item_description"],
            "original_source_requirement_id":line["original_hardware_source_reference_id"],
            "actual_manufacturer_reference_product_id":None,
            "actual_manufacturer_material_grade_spec":None,
            "source_qualifying_independent_OEM_material_receipt_sha256":None,
            "actual_fabricated_material_INPUT_kg_not_empty_equipment":None,
            "actual_manufacturing_process_consumption_and_yield":None,
            "actually_selected_supplier_and_geographical_origin":None,
            "actual_replacement_years_and_quantity":None,
            "actual_recycling_reuse_EOL_process_flow_amounts":None,
            "native_original_BAFU_zolca_file_SHA256":None,
            "native_original_BAFU_database_version_proven":False,
            "native_openLCA_process_UUID":None,
            "native_openLCA_provider_process_UUID":None,
            "native_openLCA_reference_flow_UUID":None,
            "native_openLCA_exchange_unit_id":None,
            "native_openLCA_exchange_denominator":None,
            "native_openLCA_exchange_direction":None,
            "native_openLCA_exchange_amount_in_reference_unit":None,
            "native_openLCA_product_system_link_rerun":False,
            "native_openLCA_LCIA_method_UUID":None,
            "native_openLCA_LCIA_kgCO2e_for_this_manufacturing_line":None,
            "actual_manufacturing_data_authenticated":False,
            "actual_native_provider_process_link_authenticated":False,
            "process_mapping_certified":False,
        })
    return {
        "schema_version":SCHEMA,
        "matched_service_H2_daily_kg":30000.,
        "year_specific_matched_hydrogen_functional_units":[
            {"source_year":x["source_year"],
             "delivered_H2_kg":x["annual_matched_delivered_H2_kg"],
             "H2_hourly_delivery_same_for_both_architectures":True}
            for x in elect["yearly"]
        ],
        "original_2022_2024_independently_replayed_energy_source_Git_blob":
            energy.SOURCE_GIT_BLOB,
        "original_published_F2_pressure_and_equipment_source_Git_blob":
            source["source_F2_2023_bare_vessel_reference_Git_blob"],
        "original_typeI_802_paper_vessel_count":802,
        "source_empty_equipment_1924800kg_NOT_virgin_steel_or_procurement":True,
        "original_native_database_claimed_version":"BAFU:2026 v1.1; NOT independently verified installed original process database",
        "native_dataset_SHA256_if_user_provides_original_ZOLCA":None,
        "native_database_actual_version_verified":False,
        "original_stationary_P_and_ID_and_supplier_material_qualified":False,
        "hourly_relevant_import_export_emission_factors_authenticated":False,
        "country_region_hourly_electricity_mix_and_export_credit_rule_verified":False,
        "separate_year_specific_operational_energy":[
            {"source_year":x["source_year"],
             "delta_annual_grid_import_MWh":x["EplusS_MINUS_E_delta_import_MWh"],
             "delta_annual_grid_export_MWh":x["EplusS_MINUS_E_delta_export_MWh"],
             "delta_annual_net_grid_import_MWh":x["EplusS_MINUS_E_delta_net_grid_import_MWh"],
             "delta_compressor_MWh_ALREADY_PART_OF_system_electric_load":
                x["EplusS_MINUS_E_delta_compressor_MWh_ALREADY_INCLUDED_in_system_load"],
             "CO2e_delta_not_inferable_from_energy_or_prices":True}
            for x in elect["yearly"]
        ],
        "separate_19_manufacturer_and_provider_flow_requirements":foreground,
        "eighteen_other_BoP_equipment_materials_NOT_assumed_zero":True,
        "native_BAFU_supported_method_and_product_system_closure":None,
        "original_native_BAFU_2026_v11_incremental_total_kgCO2e":None,
        "incremental_lifecycle_GWP_kgCO2e_per_kg_delivered_H2":None,
        "environmental_superiority_accepted":False,
        "scientific_v1_0_native_LCA_gate_passed":False,
    }


def fingerprint_local_zolca(path, *, expected_sha256=None):
    """Hash original private archive bytes, no unpacking or source file output."""
    path=Path(path)
    if not path.is_file() or path.is_symlink() or path.suffix.lower()!=".zolca":
        raise NativeInventoryBlocked("original private native archive must be an ordinary .zolca file")
    size=path.stat().st_size
    if size<=0 or size>20*1024**3:
        raise NativeInventoryBlocked("native archive is empty or above screening size cap")
    digest=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b""):
            digest.update(chunk)
    actual=digest.hexdigest()
    if expected_sha256 is not None and (
        not isinstance(expected_sha256,str) or not SHA_RE.fullmatch(expected_sha256) or
        actual!=expected_sha256
    ):
        raise NativeInventoryBlocked("native BAFU source bytes do not match declared SHA256")
    if not zipfile.is_zipfile(path):
        raise NativeInventoryBlocked("original .zolca is not a recognized openLCA ZIP container")
    with zipfile.ZipFile(path) as z:
        count=len(z.infolist())
        if count<1 or count>100000:
            raise NativeInventoryBlocked("native archive entry count malformed")
    return {
        "local_private_original_zolca_SHA256":actual,
        "local_archive_zip_container_integrity_screen":True,
        "archive_members_count_NOT_process_count":count,
        "original_BAFU_2026_v11_version_or_native_process_UUIDs_proven":False,
        "native_openLCA_product_system_material_LCIA_replayed":False,
        "original_private_archive_path_or_database_bytes_in_public_output":False,
    }


def audit_proposed_mapping_structure(candidate):
    """Source/documentary dimensional precheck; NEVER a native LCIA pass."""
    base=build()
    if not isinstance(candidate,dict) or candidate.get("schema_version")!=SCHEMA:
        raise NativeInventoryBlocked("L3-F native mapping schema not source-locked")
    received=candidate.get("separate_19_manufacturer_and_provider_flow_requirements")
    expected=base["separate_19_manufacturer_and_provider_flow_requirements"]
    if not isinstance(received,list) or [x.get("original_F2_source_BOM_line_id") for x in received]!=[
        x["original_F2_source_BOM_line_id"] for x in expected
    ]:
        raise NativeInventoryBlocked("native inventory original 19 F2 BOM line IDs missing/changed")
    missing=[]
    contradictions=[]
    for row in received:
        line=row["original_F2_source_BOM_line_id"]
        mass=row.get("actual_fabricated_material_INPUT_kg_not_empty_equipment")
        sha=row.get("source_qualifying_independent_OEM_material_receipt_sha256")
        if mass is None or type(mass) not in (int,float) or not math.isfinite(mass) or mass<=0:
            missing.append(line+":actual_manufactured_material")
        if type(sha) is not str or not SHA_RE.fullmatch(sha):
            missing.append(line+":qualified_OEM_material_receipt")
        proc=row.get("native_openLCA_process_UUID")
        flow=row.get("native_openLCA_reference_flow_UUID")
        if type(proc) is not str or not UUID_RE.fullmatch(proc) or (
            type(flow) is not str or not UUID_RE.fullmatch(flow)
        ):
            missing.append(line+":native_original_process_and_reference_flow_UUID")
        amount=row.get("native_openLCA_exchange_amount_in_reference_unit")
        unit=row.get("native_openLCA_exchange_denominator")
        if type(amount) not in (int,float) or not math.isfinite(amount) or amount<=0:
            missing.append(line+":native_exchange_quantity")
        if unit in ("kg_h2_nominal_capacity","kg_empty_equipment"):
            contradictions.append(line+":reference_unit_cannot_be_used_as_virgin_steel_input")
        if row.get("process_mapping_certified") is True:
            contradictions.append(line+":manual_claim_of_native_LCIA_without_replay")
        if unit=="kg_steel_input" and type(mass) in (int,float) and math.isfinite(mass) and mass>0:
            checked=audit_manufacturing_functional_unit({
                "provider_id":proc,
                "source_sha256":sha,
                "reference_flow_denominator":unit,
                "reference_flow_amount":amount,
                "manufacturing_process_scope":"stationary_type_i_steel_vessel_manufacturing",
            },required_denominator="kg_steel_input")
            if not checked["passed"]:
                contradictions.extend(line+":unit_gate:"+err for err in checked["findings"])
    return {
        "schema_version":"ptxlens.l3f_original_BAFU_v11_metadata_readiness_NOT_NATIVE_LCIA.v1",
        "original_F2_categories":19,
        "incomplete_source_specific_manufacturer_native_exchange_entries":missing,
        "fundamentally_incompatible_units_or_unsupported_LCIA_claims":contradictions,
        "all_19_required_native_provider_bytes_replayed":False,
        "real_manufacturer_foreground_verified":False,
        "environmental_superiority_authorized":False,
        "full_native_BAFU_LCIA_proven":False,
    }


def markdown(d):
    rows=[
        "# L3-F: original BAFU:2026 v1.1 stationary H2 E vs E+S native mapping, NOT LCIA",
        "",
        "Same source-year 30t/day hourly H2 for E20t and E+S40t; separate "
        "2022 and 2024. All 19 source F2 equipment/BOP categories must use "
        "actual manufactured materials, supplier region, fabrication, "
        "replacement and EOL, and authentic native original BAFU provider "
        "process/flow/unit/LCIA method. 802 × 2400kg source paper-empty "
        "vessel EQUIPMENT is NOT virgin material input.",
        "",
        "| Source F2 foreground line | Original supplier material and fabrication | "
        "Authentic native BAFU process/flow/unit | LCIA |",
        "|---|---|---|---|",
    ]
    for row in d["separate_19_manufacturer_and_provider_flow_requirements"]:
        rows.append(f"| {row['original_F2_source_BOM_line_id']} | UNKNOWN | MISSING | BLOCKED |")
    rows.extend([
        "",
        "Source-year operational differences: **2022 net grid imports E+S−E "
        "positive**, 2024 net grid imports **negative**; compressor MWh "
        "already included in system electricity. Hourly grid impact and "
        "export-credit assumptions are not sourced, so no emissions sign "
        "or magnitude is established.",
        "",
        "The optional local .zolca SHA/ZIP check only identifies archive bytes "
        "and ZIP readability. It is NOT proof of BAFU database version, "
        "supplier-compatible process UUIDs or independently rerun native "
        "openLCA LCIA. No environmental superiority or scientific v1.0.",
        "",
    ])
    return "\n".join(rows)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",type=Path,default=ROOT/"data/results")
    parser.add_argument("--fingerprint-local-zolca",type=Path)
    parser.add_argument("--expected-sha256")
    args=parser.parse_args(argv)
    out=Path(args.output_dir)
    if not out.is_dir() or out.is_symlink():
        raise NativeInventoryBlocked("public results output folder missing")
    report=build()
    paths=[
        (out/OUT_JSON,json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"\n"),
        (out/OUT_MD,markdown(report)),
    ]
    for p,body in paths:
        if p.is_symlink() or (p.exists() and
                             (not p.is_file() or p.read_text(encoding="utf-8")!=body)):
            raise NativeInventoryBlocked("BAFU native mapping immutable public contract differs")
    for p,body in paths:
        if not p.exists():
            with p.open("x",encoding="utf-8",newline="\n") as f:f.write(body)
    print("L3F_SOURCE_LINKED_BAFU2026_V11_19_FOREGROUND_Native_LCIA_BLOCKED")
    if args.fingerprint_local_zolca:
        x=fingerprint_local_zolca(
            args.fingerprint_local_zolca,expected_sha256=args.expected_sha256)
        print("LOCAL_PRIVATE_ZOLCA_SHA256",x["local_private_original_zolca_SHA256"],
              "ZIP entries",x["archive_members_count_NOT_process_count"],
              "native process/LCIA NOT verified, no private bytes/paths emitted")


if __name__=="__main__":
    main()
