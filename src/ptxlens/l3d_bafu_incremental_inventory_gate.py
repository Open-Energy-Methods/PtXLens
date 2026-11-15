"""Native BAFU 2026 F2/L1 stationary Type I storage inventory readiness audit.

Reads the 2023 F2 19-category source-locked equipment scope (peer-reviewed
empty vessel equipment mass only), NEVER silently substitutes virgin steel
kg or provider flow UUID or publishes an invented kgCO2e/kWh result.

This produces a machine-readable *negative admission ledger* and a verified
future evidence contract, not a native BAFU inventory or impact assessment.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

SOURCE=Path(__file__).resolve().parents[2]/"data/results/F2_L1_2023_source_incremental_20t_to_40t_stationary_typeI_200bar_BOM_SCOPE_NOT_complete_native_LCI.json"
PINNED_SOURCE_GIT_BLOB_SHA="424a8f738cb9caa2d05c1ec5c22cbf6cdd601b82"
SCHEMA="ptxlens.f2_l1_bafu_2026_native_incremental_storage_inventory_admission_ledger.v1"
EXPECTED_COUNT={"max_inventory":802,"usable_service":902}
EXPECTED_EMPTY_MASS_KG={"max_inventory":1924800.,"usable_service":2164800.}

class NativeInventoryBlocked(ValueError):
    pass

def check(ok,reason):
    if not ok:
        raise NativeInventoryBlocked("Native BAFU readiness: "+reason)

def source_git_blob(raw):
    raw=raw.replace(b"\r\n",b"\n")
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def inspect_original(source_path=SOURCE):
    path=Path(source_path)
    check(path.is_file(),"registered original equipment BOM source missing")
    raw=path.read_bytes()
    check(source_git_blob(raw)==PINNED_SOURCE_GIT_BLOB_SHA,
          "source equipment BOM Git blob drift: provenance revision required")
    data=json.loads(raw.decode("utf-8"))
    check(data.get("full_project_LCA_TE_A_allowed") is False and
          set(data.get("modes",{}))==set(EXPECTED_COUNT),
          "source F2 LCA/TEA full-project scope falsely established")
    ledger=[]
    for mode in ("max_inventory","usable_service"):
        case=data["modes"][mode]
        check(case.get("capacity_semantics")==mode and
              case.get("BAFU2026_v11_standalone_typeI_native_LCI_created") is False and
              case.get("complete_manufacturer_warrantied_typeI_bank_BOM") is False and
              case.get("complete_stationary_steel_content_kg") is None and
              case.get("complete_source_fabrication_and_installed_mass_kg") is None,
              "source hardware and native BAFU readiness falsely established")
        scope=case.get("incremental_only_research_sensitivity",{})
        check(scope.get("net_additional_published_reference_vessel_count")==EXPECTED_COUNT[mode] and
              scope.get("net_additional_published_empty_vessel_equipment_mass_kg")==EXPECTED_EMPTY_MASS_KG[mode] and
              scope.get("source_vessel_mass_is_NOT_virgin_steel_input_kg") is True and
              scope.get("incremental_BOP_material_manufacturing_mass_kg") is None and
              scope.get("incremental_installed_storage_CAPEX_eur") is None and
              scope.get("incremental_native_BAFU_storage_CO2e_kg") is None,
              "published reference vessel mass wrongly treated as material/impact/economic cost")
        bom=case.get("required_incremental_system_foreground_BOM",[])
        check(type(bom) is list and len(bom)==19,
              "19 foreground physical system-category record not complete")
        seen=set()
        for index,item in enumerate(bom):
            name=item.get("line_id")
            check(type(name) is str and len(name)>4 and name not in seen and
                  item.get("manufacturer_quote_eur") is None and
                  item.get("not_coupled_as_complete_native_BAFU_inventory") is True,
                  "missing unique original BOM line or unsupported vendor/native LCI evidence")
            seen.add(name)
            if index==0:
                check(name=="typeI_200bar_bare_reference_vessels" and
                      item.get("quantity")==EXPECTED_COUNT[mode] and
                      item.get("empty_mass_kg")==EXPECTED_EMPTY_MASS_KG[mode] and
                      item.get("raw_virgin_steel_mass_kg") is None and
                      item.get("empty_vessel_reference_per_unit_kg")==2400,
                      "vessel reference equipment cannot be counted as native virgin steel")
            else:
                check(item.get("quantity") is None and item.get("empty_mass_kg") is None,
                      "source unknown BoP quantity must remain unknown (not zero)")
            ledger.append({
                "mode":mode,"index":index,"line_id":name,
                "system":item.get("system"),"source_reference_id":item.get("source_ref_id"),
                "original_scope_description":item.get("item_scope"),
                "reference_only_empty_equipment_mass_kg":
                    item.get("empty_mass_kg") if index==0 else None,
                "reference_vessel_count_ONLY_not_fabricated_bill_of_materials":
                    item.get("quantity") if index==0 else None,
                "independent_material_composition_or_manufacturer_mass_kg":None,
                "fabrication_process_and_scrap_yield":None,
                "native_BAFU_2026_dataset_process_UUID":None,
                "native_BAFU_2026_provider_activity_UUID":None,
                "native_BAFU_2026_reference_product_UUID":None,
                "native_BAFU_2026_reference_unit":None,
                "native_BAFU_2026_geography_and_vintage":None,
                "native_BAFU_2026_exchange_coefficient":None,
                "manufacturer_quotation_eur":None,
                "measured_or_verified_incremental_LCIA_GWP_kgCO2e":None,
                "native_mapping_status":"BLOCKED_UNTIL_MATERIAL_MANUFACTURING_AND_NATIVE_BAFU_MATCH",
                "zero_impact_assumed":False,
            })
    check(len(ledger)==38 and
          len({item["line_id"] for item in ledger})==19,
          "both storage interpretations must share 19 unique source BOM scope lines")
    return {
        "schema_version":SCHEMA,
        "source_F2_hardware_Git_blob_SHA1":PINNED_SOURCE_GIT_BLOB_SHA,
        "source_BAFU_version":"BAFU:2026 v1.1 native openLCA, not substituted ecoinvent or vehicle composite tank",
        "model_capacity_semantics_separately":[
            "max_inventory","usable_service"],
        "gross_reference_802_extra_empty_TypeI_vessels_kg":1924800,
        "usable_reference_902_extra_empty_TypeI_vessels_kg":2164800,
        "this_empty_equipment_mass_is_NOT_virgin_steel_consumption":True,
        "19_source_BOM_categories_times_2_modes":38,
        "source_known_equipment_mass_but_complete_native_LCI":False,
        "manufacturer_actual_installed_system_BOM_and_price_verified":False,
        "native_BAFU_2026_v11_all_38_foreground_links_connected":False,
        "native_BAFU_2026_whole_station_manufacturing_emissions_kgCO2e":None,
        "modelled_incremental_H2_operational_electricity_LCIA_GWP_kgCO2e":None,
        "avoided_2022_2024_kgCO2e_or_full_hydrogen_product_comparison":None,
        "native_BAFU_LCIA_critical_path":[
            "Verify manufacturer design basis, pressure gauge/absolute rating and site functional unit",
            "Obtain complete material grade, composition, reference vessel part fabrication/yield and BoP quantities",
            "Identify actual native BAFU:2026 v1.1 openLCA dataset/process UUIDs, providers, reference flows and units",
            "Check geographically appropriate market electricity and manufacturing, transports, replacements and end of life",
            "Map every foreground flow with defensible manufacturing exchange quantity, source and units",
            "Select exact existing BAFU-supported LCIA method IDs, normalization and uncertainty, run native openLCA calculations",
            "Compare E vs E+S under IDENTICAL hourly H2 delivery target per source year/mode; peer check primary provider/LCIA",
        ],
        "ledger":ledger,
        "full_installed_H2_storage_life_cycle_GWP_or_CCAPEX_certified":False,
        "scientific_v1_0_release_allowed":False,
    }

def verify_future_complete_native_mapping(ledger):
    """Do NOT infer native data integrity from a populated JSON mapping.

    A future implementation must reopen an exact, independently SHA-verified
    licensed .zolca database and query real native process/provider UUIDs,
    reference-product units, openLCA product system links and LCIA results.
    Current metadata cannot prove any of those external facts. Always refuse
    v1 certification until a separate native-provider replay implementation
    is executed and independently validated.
    """
    check(type(ledger) is dict and ledger.get("schema_version")==SCHEMA,
          "unknown source version")
    raise NativeInventoryBlocked(
        "Native BAFU:2026 v1.1 database process/provider/reference exchange "
        "replay and independent LCIA result verification are not implemented; "
        "even fully populated declarative JSON alone cannot certify native LCA"
    )


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,required=True,
                   help="public NO-NATIVE-LCIA readiness ledger (never original .zolca)")
    args=p.parse_args(argv)
    record=inspect_original()
    path=args.output
    check(path.parent.is_dir(),"must specify existing output directory")
    body=json.dumps(record,sort_keys=True,indent=2,allow_nan=False)+"\n"
    check(not path.exists() or (path.is_file() and path.read_text(encoding="utf-8")==body),
          "existing immutable native-BOM negative ledger differs")
    if not path.exists():
        with path.open("x",encoding="utf-8",newline="\n") as f:f.write(body)
    print("BAFU_2026_NATIVE_STATIONARY_TYPEI_LCI_NOT_READY 38 BOM rows; "
          "2 reference equipment masses only; 0 native links verified; whole-plant LCIA BLOCKED")

if __name__=="__main__":
    main()
