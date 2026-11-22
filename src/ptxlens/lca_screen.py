"""Audited 2023 *electricity-supply* life-cycle GWP screen (NOT full H2 LCA).

Original PyNEXUS WP5 source ZIP hashes and 8,760 hourly model outputs are
validated by observed.load_archive before any footprint is produced.
The two GWP factors are actual published 2023 national default / UNECE
offshore-wind LCA values, NOT invented or API-derived hourly emissions.
"""
from __future__ import annotations

import csv
import io
import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
import zipfile

from .observed import compare_archives, load_archive

SOURCES = {
    "grid_2023": {
        "url": "https://co2emissiefactoren.nl/factoren/2023/11/52/elektriciteit-stroom-onbekend-gridmix/",
        "publisher": "Rijkswaterstaat / Stichting Stimular, Dutch CO2 Emissiefactoren",
        "year": 2023,
        "production_kg_co2e_per_kwh": 0.290,
        "fuel_chain_kg_co2e_per_kwh": 0.047,
        "infrastructure_kg_co2e_per_kwh": 0.007,
        "method": "2023 national average location-based electricity-factor proxy; NOT marginal, not hourly, not 100% process-provider inventory",
    },
    "wind_offshore": {
        "url": "https://unece.org/sed/documents/2021/10/reports/life-cycle-assessment-electricity-generation-options",
        "supporting_url": "https://wiki.unece.org/download/attachments/271089909/A-LCA-20-05e_infrastructure%20emissions_ICCT.pdf?api=v2",
        "publisher": "UNECE 2021 LCA of electricity generation options; EU28 offshore-wind literature benchmark",
        "year": 2021,
        "lifecycle_kg_co2e_per_kwh": 0.0142,
        "method": "LCA generation factor; not a time-dependent actual North Sea turbine LCI",
    },
}
GRID_OPERATIONAL = SOURCES["grid_2023"]["production_kg_co2e_per_kwh"]
GRID_UPSTREAM = SOURCES["grid_2023"]["fuel_chain_kg_co2e_per_kwh"]
GRID_INFRA = SOURCES["grid_2023"]["infrastructure_kg_co2e_per_kwh"]
WIND_LIFECYCLE = SOURCES["wind_offshore"]["lifecycle_kg_co2e_per_kwh"]


def _closed(x, y, label, tol=2e-4):
    if not math.isclose(x, y, rel_tol=1e-9, abs_tol=tol):
        raise ValueError(f"{label} identity failed: {x} != {y}")


def _lines(archive, scenario):
    with zipfile.ZipFile(archive) as archive_zip:
        csv_bytes = archive_zip.read(scenario + "/stage_b.csv")
        return list(csv.DictReader(io.StringIO(csv_bytes.decode("utf-8-sig"))))


def assess_observed_electricity_lifecycle(archive, *, hourly_contributions=False):
    """Screen energy-input supply-chain GWP, attributed to modeled H2 delivered.

    Includes NL grid production+upstream fuel, grid infrastructure and fully
    life-cycled offshore wind generation. Explicitly excludes electrolyser
    stacks/BoP, storage, water, compression, H2 delivery and EOL. The results
    are NOT a complete cradle-to-gate GWP or product-system LCIA.
    """
    source = load_archive(archive)  # verifies original ZIP, stage hashes and economics
    scenario = source["scenario"]
    rows = _lines(archive, scenario)
    if len(rows) != 8760:
        raise ValueError("must have 8760 original hourly dispatch rows")
    totals = {
        "grid_generation_kgco2e": 0.0,
        "grid_upstream_fuels_kgco2e": 0.0,
        "grid_generation_infrastructure_kgco2e": 0.0,
        "offshore_wind_full_lifecycle_kgco2e": 0.0,
        "grid_consumed_mwh": 0.0,
        "wind_consumed_mwh": 0.0,
        "hydrogen_delivered_kg": 0.0,
    }
    series = []
    start = datetime(2023, 1, 1, tzinfo=timezone.utc)
    for index, row in enumerate(rows):
        if int(row["timestep"]) != index:
            raise ValueError("missing/duplicated original hourly index")
        def v(key):
            num = float(row[key])
            if not math.isfinite(num):
                raise ValueError(f"nonfinite source hourly {key}")
            return num
        wind_available = v("wind_available_mw")
        curtailed = v("curtailment_mw")
        export = v("grid_export_mw")
        imported = v("grid_import_mw")
        elec = v("power_optimized_mw")
        demand = v("h2_demand_kg_h")
        unmet = v("demand_slack_kg_h")
        wind_to_electrolysis = wind_available - curtailed - export
        delivered = demand - unmet
        if min(wind_to_electrolysis, imported, delivered, elec) < -1e-6:
            raise ValueError("negative consumed flow; export source allocation ambiguous")
        if imported > 1e-6 and export > 1e-6:
            raise ValueError("simultaneous import/export not supported")
        _closed(imported + wind_to_electrolysis, elec, "energy allocation",tol=2e-4)
        components = {
            "grid_generation_kgco2e": 1000 * imported * GRID_OPERATIONAL,
            "grid_upstream_fuels_kgco2e": 1000 * imported * GRID_UPSTREAM,
            "grid_generation_infrastructure_kgco2e": 1000 * imported * GRID_INFRA,
            "offshore_wind_full_lifecycle_kgco2e": 1000 * wind_to_electrolysis * WIND_LIFECYCLE,
        }
        for name, amount in components.items():
            totals[name] += amount
        totals["grid_consumed_mwh"] += imported
        totals["wind_consumed_mwh"] += wind_to_electrolysis
        totals["hydrogen_delivered_kg"] += delivered
        if hourly_contributions:
            series.append({
                "timestamp_assumed_utc": (start + timedelta(hours=index)).isoformat().replace("+00:00","Z"),
                "hour_index_source": index,
                "grid_import_mwh": imported,
                "offshore_wind_allocated_to_electrolyser_mwh": wind_to_electrolysis,
                "h2_delivered_kg": delivered,
                **components,
            })
    _closed(totals["grid_consumed_mwh"],source["annual_grid_import_mwh"],"total grid")
    _closed(totals["wind_consumed_mwh"],source["annual_wind_consumed_mwh"],"total wind")
    _closed(totals["hydrogen_delivered_kg"],source["annual_delivered_h2_kg"],"total delivery")
    _closed(totals["grid_consumed_mwh"]+totals["wind_consumed_mwh"],
            source["annual_electrolyser_input_mwh"],"annual energy")
    components = {k: v for k,v in totals.items() if k.endswith("_kgco2e")}
    emissions = sum(components.values())
    without_grid_infra = emissions - components["grid_generation_infrastructure_kgco2e"]
    result = {
        "schema_version": "ptxlens.electricity_supply_gwp_2023.v0.1",
        "scenario":scenario,
        "source_archive_sha256":source["archive_sha256"],
        "stage_b_sha256":source["stage_b_sha256"],
        "source_year":2023,
        "source_type":"observed ERA5 wind + observed 2023 NL A44 electricity prices; simulated PyNEXUS H2 dispatch",
        "claim_level":"published-factor electricity-supply GWP screening; NOT full product LCA or actual openLCA LCIA",
        "functional_unit":"1 kg MODELLED delivered H2; delivery purity and pressure not assessed",
        "hourly_time_alignment_warning":"source timestep index aligned to UTC 2023 by archive assumption; not revalidated against ERA5 original time-coordinate",
        "functional_unit_denominator_kg_h2":totals["hydrogen_delivered_kg"],
        "energy_mwh": {
            "grid_import_for_electrolysis":totals["grid_consumed_mwh"],
            "offshore_wind_for_electrolysis":totals["wind_consumed_mwh"],
        },
        "gwp_kgco2e_by_source_category":components,
        "reported_energy_supply_kgco2e":emissions,
        "gwp_kgco2e_per_kg_modelled_h2_delivered":emissions/totals["hydrogen_delivered_kg"],
        "sensitivity_excluding_grid_infrastructure_kgco2e_per_kg_h2":(
            without_grid_infra/totals["hydrogen_delivered_kg"]),
        "sources":SOURCES,
        "allocation":"grid imports assigned to electrolyser; onsite wind to electrolyser=wind available minus curtailed minus electricity exported; no avoided-export GWP credit",
        "temporal_resolution_of_gwp_factors":"ANNUAL/REFERENCE factors constant in all 8760 hours; do not label hourly marginal emissions",
        "known_exclusions":[
            "electrolyser stack and balance of plant manufacturing and end-of-life",
            "electrolyser replacements/degradation and refrigerants",
            "hydrogen storage tank, hydrogen pipeline, compression and final delivery pressure/purity",
            "water supply, purification and waste-treatment chain",
            "transmission/distribution losses not included in cited delivered grid factor",
            "hourly marginal or market-based grid carbon, contractual renewable certificate issues",
            "CO2/GHG process inventory and compatible LCIA method inside an openLCA product system",
        ],
        "comparability_warning":"E and E+S deliver different hydrogen quantities; intensity differences cannot by themselves establish superior matched-service impact",
    }
    if hourly_contributions:
        result["hourly_contributions"] = series
    return result


def compare_e_and_es(e_zip, es_zip):
    """Source-verified comparison and conditional descriptive differences."""
    audit = compare_archives(e_zip, es_zip)  # verifies matching observed price series
    a = assess_observed_electricity_lifecycle(e_zip)
    b = assess_observed_electricity_lifecycle(es_zip)
    a_int = a["gwp_kgco2e_per_kg_modelled_h2_delivered"]
    b_int = b["gwp_kgco2e_per_kg_modelled_h2_delivered"]
    return {
        "schema_version":"ptxlens.electricity_supply_2023_comparison.v0.1",
        "comparison":"2023 NL observed-input, modelled delivery, published annual GWP factors",
        "E":a,"E_plus_S":b,
        "delta_gwp_kgco2e":b["reported_energy_supply_kgco2e"]-a["reported_energy_supply_kgco2e"],
        "delta_intensity_kgco2e_per_kg_h2":b_int-a_int,
        "delta_modelled_h2_delivered_kg":audit["delta_delivered_h2_kg"],
        "matched_hydrogen_service":False,
        "status":"real-source electricity-supply GWP screening ONLY; NOT comparative product LCA",
    }


def write_results(e_zip, es_zip, output_json, hourly_dir=None):
    path=Path(output_json)
    if path.exists():
        raise FileExistsError("refusing to overwrite independently recorded research output")
    result=compare_e_and_es(e_zip,es_zip)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result, indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
    if hourly_dir is not None:
        dest=Path(hourly_dir)
        if dest.exists():
            raise FileExistsError("refusing to overwrite hourly report folder")
        dest.mkdir(parents=True)
        for arc,case in ((e_zip,"E"),(es_zip,"E_plus_S")):
            raw=assess_observed_electricity_lifecycle(arc,hourly_contributions=True)
            with (dest/f"{case}_hourly_components.csv").open("w",newline="",encoding="utf-8") as f:
                writer=csv.DictWriter(f,fieldnames=raw["hourly_contributions"][0].keys())
                writer.writeheader()
                writer.writerows(raw["hourly_contributions"])
    return result
