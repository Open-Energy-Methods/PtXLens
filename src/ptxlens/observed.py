"""Audit *observed-price* frozen PyNEXUS WP5 ZIPs, not earlier synthetic-price demo.

All calculations use original hourly Stage B records and independently check
the upstream recorded summary and its SHA256 statements. No solver re-run and
no claim of validated grid-carbon, plant economics, or real hydrogen production.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import zipfile

# GitHub archived artifacts recovered 2026-11-13, before 2026-12-24 expiry.
KNOWN_SHA256 = {
    "E": "069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051",
    "E+S": "cd4101fe62c3f1b8aa2d7508d3651d2fee40d2bafe6d5b87e40d5f4d055070f9",
}
SOURCE_RUN = "https://github.com/abhijith-sivaprasadan/PyNEXUS/actions/runs/40229852457"
COLS = ("timestep", "wind_available_mw", "curtailment_mw",
        "power_optimized_mw", "electricity_price", "h2_produced_kg_h",
        "h2_demand_kg_h", "demand_slack_kg_h",
        "grid_import_mw", "grid_export_mw", "online_status")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def close(x, y, label, atol=1e-5):
    if not math.isclose(x, y, abs_tol=atol, rel_tol=1e-9):
        raise ValueError(f"independent {label} mismatch: {x!r} vs {y!r}")


def load_archive(path: str | Path):
    """Fail closed if the archive is not one of two audited 2023 WP5 cases."""
    raw = Path(path).read_bytes()
    digest = sha(raw)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if "manifest.json" not in z.namelist():
            raise ValueError("missing manifest")
        manifest = json.loads(z.read("manifest.json"))
        if manifest.get("full_year") is not True or manifest.get("hours") != 8760:
            raise ValueError("not a certified 8760-hour WP5 archive")
        if manifest.get("cost_claim") != "NONE_GRID_SETTLEMENT_ONLY":
            raise ValueError("unrecognized economic provenance")
        if manifest.get("price_kind") != "PROCESSED_ENTSOE_2023_NL_DAY_AHEAD_NOT_INVOICE":
            raise ValueError("requires original observed Dutch day-ahead price input")
        case_dirs = sorted({f.split("/")[0] for f in z.namelist() if f.endswith("/record.json")})
        if len(case_dirs) != 1 or case_dirs[0] not in KNOWN_SHA256:
            raise ValueError("expected named E or E+S archive")
        scenario = case_dirs[0]
        if digest != KNOWN_SHA256[scenario]:
            raise ValueError("archive bytes not equal to pinned reviewed artifact")
        record = json.loads(z.read(scenario + "/record.json"))
        if record.get("scenario") != scenario or record.get("status") != "VERIFIED_TWO_STAGE_SOLVE":
            raise ValueError("unexpected scenario or result state")
        if record.get("price_kind") != manifest["price_kind"]:
            raise ValueError("price provenance conflict")
        if record.get("price_csv_sha256") != manifest.get("price_csv_sha256"):
            raise ValueError("scenario/manifest price SHA conflict")
        for stage in ("stage_a.csv", "stage_b.csv"):
            data = z.read(scenario + "/" + stage)
            if sha(data) != record["dispatch_hashes"][stage]:
                raise ValueError(f"source {stage} hash mismatch")
        config_data = z.read(scenario + "/config.yaml")
        if sha(config_data) != record["config_sha256"]:
            raise ValueError("source configuration hash mismatch")
        if any(v is not True for v in record.get("verification_b", {}).values()):
            raise ValueError("not all registered stage B verification flags passed")
        if record.get("solver_b", {}).get("termination_condition") != "optimal":
            raise ValueError("Stage B not recorded optimal")
        data = z.read(scenario + "/stage_b.csv")
        reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig")))
        if not set(COLS).issubset(reader.fieldnames or []):
            raise ValueError("Stage B schema missing required columns")
        rows = list(reader)
        if len(rows) != 8760 or any(int(r["timestep"]) != i for i,r in enumerate(rows)):
            raise ValueError("missing, duplicate or nonsequential timestep")
        summary = _recompute(rows, record)
        summary.update({
            "schema_version": "ptxlens.pynexus_wp5_observed.v0.1",
            "source": "PyNEXUS frozen 2023 WP5, processed ENTSO-E NL A44",
            "source_run_url": SOURCE_RUN,
            "archive_sha256": digest, "stage_b_sha256": sha(data),
            "price_csv_sha256": record["price_csv_sha256"],
            "historical_hour0_alignment": manifest.get("hourly_alignment_assumption"),
            "source_restriction": "2023 computational model output; not actual plant telemetry",
            "cost_restriction": "wholesale net settlement only, not hydrogen cost/LCOH",
        })
        return summary


def _recompute(rows, record):
    totals = {
        "annual_delivered_h2_kg":0.0, "annual_unserved_h2_kg":0.0,
        "annual_produced_h2_kg":0.0, "annual_demand_h2_kg":0.0,
        "annual_electrolyser_input_mwh":0.0, "annual_wind_consumed_mwh":0.0,
        "annual_grid_import_mwh":0.0, "annual_grid_export_mwh":0.0,
        "annual_net_wholesale_settlement_eur":0.0, "online_hours":0,
        "annual_curtailment_mwh":0.0, "annual_wind_available_mwh":0.0,
    }
    hourly_prices = []
    for r in rows:
        v = {k: float(r[k]) for k in COLS}
        if not all(math.isfinite(value) for value in v.values()):
            raise ValueError("nonfinite source hourly value")
        if any(v[k] < -1e-8 for k in COLS if k not in ("electricity_price",)):
            raise ValueError("negative source flow")
        if v["grid_import_mw"] > 1e-6 and v["grid_export_mw"] > 1e-6:
            raise ValueError("simultaneous grid purchase/sale")
        close(v["wind_available_mw"] + v["grid_import_mw"] -
              v["grid_export_mw"] - v["curtailment_mw"],
              v["power_optimized_mw"], "electricity-balance", atol=1e-4)
        close(v["h2_produced_kg_h"],
              v["power_optimized_mw"] * record["metrics"]["linearized_h2_kg_per_mwh"],
              "hydrogen-conversion", atol=1e-4)
        demand, shortfall = v["h2_demand_kg_h"], v["demand_slack_kg_h"]
        if shortfall > demand + 1e-5:
            raise ValueError("unserved demand exceeds demand")
        totals["annual_delivered_h2_kg"] += demand-shortfall
        totals["annual_unserved_h2_kg"] += shortfall
        totals["annual_demand_h2_kg"] += demand
        totals["annual_produced_h2_kg"] += v["h2_produced_kg_h"]
        totals["annual_electrolyser_input_mwh"] += v["power_optimized_mw"]
        totals["annual_grid_import_mwh"] += v["grid_import_mw"]
        totals["annual_grid_export_mwh"] += v["grid_export_mw"]
        totals["annual_curtailment_mwh"] += v["curtailment_mw"]
        totals["annual_wind_available_mwh"] += v["wind_available_mw"]
        totals["annual_wind_consumed_mwh"] += (
            v["wind_available_mw"]-v["curtailment_mw"]-v["grid_export_mw"])
        totals["annual_net_wholesale_settlement_eur"] += (
            v["grid_import_mw"]-v["grid_export_mw"])*v["electricity_price"]
        totals["online_hours"] += int(v["online_status"])
        hourly_prices.append(v["electricity_price"])
    m = record["metrics"]
    for key, metric in (
        ("annual_produced_h2_kg","h2_produced_kg"),
        ("annual_unserved_h2_kg","stage_b_shortfall_kg"),
        ("annual_demand_h2_kg","demand_h2_kg"),
        ("annual_grid_import_mwh","grid_import_mwh"),
        ("annual_grid_export_mwh","grid_export_mwh"),
        ("annual_electrolyser_input_mwh","electrolyser_input_mwh"),
        ("annual_net_wholesale_settlement_eur","stage_b_grid_settlement_eur_OBSERVED_PRICE_INPUT")
    ):
        close(totals[key],m[metric],key,atol=1e-3)
    totals["scenario"] = record["scenario"]
    totals["electrolyser_capacity_mw"] = m["electrolyser_capacity_mw"]
    totals["storage_capacity_kg"] = m["storage_capacity_kg"]
    totals["first_price_eur_mwh"] = hourly_prices[0]
    totals["last_price_eur_mwh"] = hourly_prices[-1]
    totals["price_series_sha256"] = sha(json.dumps(hourly_prices, separators=(",",":")).encode())
    return totals


def compare_archives(e, es):
    a, b = load_archive(e), load_archive(es)
    if a["scenario"] != "E" or b["scenario"] != "E+S":
        raise ValueError("must compare E to E+S")
    if a["price_series_sha256"] != b["price_series_sha256"]:
        raise ValueError("prices or hourly alignment differ")
    if a["electrolyser_capacity_mw"] != b["electrolyser_capacity_mw"]:
        raise ValueError("different electrolyser installed capacity")
    return {
        "schema_version":"ptxlens.pynexus_observed_comparison.v0.1",
        "E":a, "E_plus_S":b,
        "delta_delivered_h2_kg":b["annual_delivered_h2_kg"]-a["annual_delivered_h2_kg"],
        "delta_net_wholesale_settlement_eur":(
            b["annual_net_wholesale_settlement_eur"]-a["annual_net_wholesale_settlement_eur"]),
        "comparison_limit":"different H2 delivered; NOT matched-service or standalone LCOH",
    }
