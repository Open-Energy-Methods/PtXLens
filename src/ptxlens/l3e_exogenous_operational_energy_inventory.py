"""L3-E matched exogenous H30/W090 hourly source-replayed ANNUAL energy inventory.

Reconstructs E20t/E+S40t annual signed import and export flows from the two
already independently reviewed original-source INTEGER dispatch public scalar
receipts, source Git blob pinned. Derives net grid electricity, compressor
electrical use (SUBSET OF system electric load, NOT additional grid energy),
and same-service kWh/kg increments.

Environmental scientific pitfall:
2022 E+S SAVES 3.2816m source EUR although its net grid energy increases
~900 MWh, because wholesale price chronology and storage dispatch matter.
2024 net import decreases ~881 MWh. Neither energy arithmetic proves GHG
improvement: full time-matched electricity-mix/marginal emission inventory,
real export credit rules and the actual BAFU original-v1.1 manufacturing,
BoP/replacement/EOL inventories do not yet exist. NO GWP is emitted.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

from .l3e_exogenous_incremental_dcf import (
    ROOT, SOURCE_GIT_BLOB, load_admitted_source, need, number
)

SCHEMA="ptxlens.l3e_exogenous_H30_W090_replayed_source_year_annual_electricity_inventory_NOT_LCIA.v1"
SOURCE_SCHEMA="ptxlens.f3d_exogenous_H30_W090_both_integer_primal_independently_replayed.v1"
BLOBS={
    2022:"0ef8966342b516d94ee6b7ce6223cb8fe6a535b0",
    2024:"c702bf79f826fc28def0e60a5d2c0537241961ac",
}
OUT_JSON="L3E_H30_W090_2022_2024_SOURCE_ANNUAL_GRID_AND_COMPRESSOR_INVENTORY_NOT_LCIA_v1.json"
OUT_MD="L3E_H30_W090_2022_2024_SOURCE_ENERGY_AND_EMISSIONS_LIMITS_v1.md"


def sha_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()


def source_file(y):
    return ROOT/"data/results"/(
        f"F3D_EXOGENOUS_{y}_max_inventory_H30_W090_BOTH_INTEGER_INDEPENDENT_REPLAY_v1.json"
    )


def load_year(year,matched):
    need(type(year) is int and year in BLOBS,
         "unexpected source historical year requested")
    p=source_file(year)
    need(p.is_file() and not p.is_symlink(),
         "independently reviewed source-year E/ES integer energy receipt absent")
    raw=p.read_bytes()
    need(sha_blob(raw)==BLOBS[year],
         "original independent source year hourly energy receipt Git blob changed")
    d=json.loads(raw.decode("utf-8"))
    hours=8760 if year==2022 else 8784
    h2=1250.*hours
    need(d.get("schema_version")==SOURCE_SCHEMA and
         d.get("source_year")==year and
         d.get("source_year_UTC_hours")==hours and
         d.get("capacity_semantics")=="max_inventory" and
         d.get("matched_exogenous_hydrogen_service_tonnes_day")==30. and
         abs(number(d.get("matched_exogenous_service_annual_H2_kg"),"H2 annual")-h2)<.005 and
         d.get("E_and_ES_fully_independent_primal_mass_electricity_EOS_market_replay") is True and
         d.get("original_hourly_provider_arrays_or_solver_witnesses_in_public") is False and
         d.get("actual_site_or_manufacturer_or_BAFU_LCIA_or_scientific_v1_0_certified") is False,
         "source full-year independent integer H30 electric replay is not valid")
    data=d.get("case_results",{})
    need(type(data) is dict and set(data)=={"E","E_plus_S"},
         "source pair of independently replayed E/E+S annual dispatch missing")
    ledger={}
    for case in ("E","E_plus_S"):
        c=data[case]
        need(c.get("status")==
             "INDEPENDENT_ORIGINAL_FULL_YEAR_INTEGER_PRIMAL_H2_ELECTRIC_EOS_REPLAY_PASSED" and
             c.get("original_private_hourly_H2_wind_price_primal_vectors_NOT_in_public") is True and
             c.get("independent_integer_cost_dual_tree_proof") is False and
             abs(number(c.get("independent_annual_delivered_H2_kg"),"case H2")-h2)<.005,
             "independent original model case energy/hydrogen qualification changed")
        imports=number(c.get("independent_annual_grid_import_MWh"),"grid import MWh",minimum=0.)
        exports=number(c.get("independent_annual_grid_export_MWh"),"grid export MWh",minimum=0.)
        compressor=number(c.get("independent_annual_compression_MWh"),"compressor MWh",minimum=0.)
        cost=number(c.get("source_modelled_nominal_original_year_wholesale_eur"),"source cost")
        need(abs(cost-(matched["source_annual_saving_eur"]+
             data["E_plus_S"]["source_modelled_nominal_original_year_wholesale_eur"]
             if case=="E" else cost))<.05,
             "source original published wholesale price/historical economy changed")
        ledger[case]={
            "original_E_or_ES_hardware":case,
            "modelled_annual_grid_import_MWh":imports,
            "modelled_annual_grid_export_MWh":exports,
            "modelled_annual_signed_NET_grid_import_MWh":imports-exports,
            "modelled_annual_compressor_electricity_MWh_WITHIN_system_load":compressor,
            "modelled_annual_signed_wholesale_electricity_settlement_nominal_year_EUR":cost,
            "modelled_annual_import_kWh_per_kg_H2":1000.*imports/h2,
            "modelled_annual_export_kWh_per_kg_H2":1000.*exports/h2,
            "modelled_annual_signed_net_import_kWh_per_kg_H2":1000.*(imports-exports)/h2,
            "modelled_compressor_kWh_per_kg_H2_WITHIN_system_load":1000.*compressor/h2,
            "actual_metered_site_electricity_data":False,
        }
    e=ledger["E"]
    s=ledger["E_plus_S"]
    def dlt(field):
        return s[field]-e[field]
    return {
        "source_year":year,"source_year_UTC_hours":hours,
        "annual_matched_delivered_H2_kg":h2,
        "year_specific_original_integer_replay_Git_blob_SHA1":BLOBS[year],
        "cases":ledger,
        "EplusS_MINUS_E_delta_import_MWh":dlt("modelled_annual_grid_import_MWh"),
        "EplusS_MINUS_E_delta_export_MWh":dlt("modelled_annual_grid_export_MWh"),
        "EplusS_MINUS_E_delta_net_grid_import_MWh":
            dlt("modelled_annual_signed_NET_grid_import_MWh"),
        "EplusS_MINUS_E_delta_net_grid_import_kWh_per_kg_delivered_H2":
            1000.*dlt("modelled_annual_signed_NET_grid_import_MWh")/h2,
        "EplusS_MINUS_E_delta_compressor_MWh_ALREADY_INCLUDED_in_system_load":
            dlt("modelled_annual_compressor_electricity_MWh_WITHIN_system_load"),
        "modelled_year_specific_wholesale_E_MINUS_ES_saving_EUR":
            matched["source_annual_saving_eur"],
        "net_grid_electricity_NOT_same_as_net_signed_wholesale_EUR":True,
        "time_matched_grid_marginal_LCIA_or_export_credit_factors_available":False,
        "grid_energy_delta_implies_CO2e_sign":None,
        "native_BAFU_v11_foreground_manufacturing_plus_replacements_GWP_kgCO2e":None,
        "environmental_superiority_certified":False,
    }


def build():
    original=load_admitted_source()
    ledgers=[load_year(year,original[year]) for year in (2022,2024)]
    return {
        "schema_version":SCHEMA,
        "source_verified_H30_W090_2022_2024_cross_year_Git_blob_SHA1":
            SOURCE_GIT_BLOB,
        "functional_unit":"1 kg H2 delivered by both original architectures at identical hourly source-year offtake, 30t/day",
        "source_years":[2022,2024],
        "yearly":ledgers,
        "annual_electricity_Net_import_is_import_minus_export":True,
        "compressor_MWh_is_electrical_load_SUBSET_NOT_added_to_grid_consumption":True,
        "net_wholesale_savings_are_NOT_same_as_energy_savings":True,
        "missing_hourly_time_matched_energy_grid_emission_factors":True,
        "missing_reproducible_export_credit_accounting_and_real_grid_contract":True,
        "missing_complete_native_BAFU_v11_manufacturing_BoP_replacements_EOL":True,
        "lifecycle_incremental_kgCO2e_per_kg_delivered_H2":None,
        "claim_of_environmentally_superior_storage_allowed":False,
        "scientific_v1_0_LCA_gate_passed":False,
        "public_original_hourly_8784_8760_source_price_wind_primal_vectors":False,
    }


def markdown(d):
    years=d["yearly"]
    def f(y,key):
        return y[key]
    rows=[
        "# L3-E H30/W090: independently replayed source-year energy inventory, NOT LCIA",
        "",
        "Original annual E20t/E+S40t integer model at identical 30t/day H2 "
        "and 90% original modelled wind ELECTRIC power, separate 2022 and "
        "2024 price+wind chronologies.",
        "",
        "| E+S minus E increment (MWh/year) | 2022 | 2024 |",
        "|---|---:|---:|",
    ]
    for label,key in (
        ("Gross grid import", "EplusS_MINUS_E_delta_import_MWh"),
        ("Gross grid export", "EplusS_MINUS_E_delta_export_MWh"),
        ("Signed net grid import (imports - exports)",
         "EplusS_MINUS_E_delta_net_grid_import_MWh"),
        ("Compressor electricity, INSIDE grid/system load",
         "EplusS_MINUS_E_delta_compressor_MWh_ALREADY_INCLUDED_in_system_load"),
    ):
        rows.append(f"| {label} | {f(years[0],key):+,.3f} | {f(years[1],key):+,.3f} |")
    rows.extend([
        "",
        "In 2022 E+S has an independently replayed wholesale electricity "
        "saving EVEN THOUGH net grid electricity increases. In 2024 net grid "
        "electricity decreases. This is not a contradiction: hourly electricity "
        "prices, exports and temporal dispatch determine signed WHOLESALE cost.",
        "",
        "**Do not double count compressor electricity**: compressor MWh is a "
        "component of original unit/grid electricity balances, not an "
        "additional energy purchase on top of gross grid import.",
        "",
        "Net annual import or price is NOT an emissions factor. Real GWP requires "
        "hourly relevant provider/location-specific emission profiles, justified "
        "import/export treatment and time matching; full source BAFU:2026 "
        "v1.1 manufacturing inputs, replacements/BoP/EOL and actual site "
        "equipment data are still absent. No CO2e outcome or environmental "
        "preference is demonstrated.",
        "",
    ])
    return "\n".join(rows)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir",type=Path,default=ROOT/"data/results")
    args=p.parse_args(argv)
    out=Path(args.output_dir)
    need(out.is_dir() and not out.is_symlink(),
         "public results directory missing or symlinked")
    doc=build()
    data=[
        (out/OUT_JSON,json.dumps(doc,indent=2,sort_keys=True,allow_nan=False)+"\n"),
        (out/OUT_MD,markdown(doc)),
    ]
    for path,body in data:
        need(not path.is_symlink() and
             (not path.exists() or (path.is_file() and
              path.read_text(encoding="utf-8")==body)),
             "published source-year annual electricity inventory differs")
    for path,body in data:
        if not path.exists():
            with path.open("x",encoding="utf-8",newline="\n") as f:
                f.write(body)
    print("L3E_PUBLISHED_SOURCE_YEAR_EXOGENOUS_GRID_IMPORT_EXPORT_COMPRESSOR_ENERGY_INVENTORY_REPLAY",
          "2022 net import rises/2024 net import falls; no native LCIA, do not infer climate benefit")


if __name__=="__main__":
    main()
