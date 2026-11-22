"""L3-G: fail-closed paired PtXFlex/PtXLens research release qualification.

Only the eight L3-F public-safe, exactly reconstructed files are admitted.
This module NEVER authenticates site/vendor records, re-runs original MILPs,
runs openLCA, assigns a manufacturer's bank, or authorizes scientific v1.0.
No external source archive, confidential vendor document, or private path is
read. The manifest contains relative paths and cryptographic fingerprints.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import l3f_publication_admission as l3f

SCHEMA = "ptxlens.l3g_paired_research_evidence_release_gate.v1"
OUT_JSON = "L3G_PTXFLEX_PTXLENS_CROSS_REPO_CLAIM_EVIDENCE_GATE_NOT_SCIENTIFIC_V1_v1.json"
OUT_MD = "L3G_PTXFLEX_PTXLENS_SCIENTIFIC_RELEASE_READINESS_NOT_V1_v1.md"


class L3GReleaseError(ValueError):
    """The paired public research claims are not admissible."""


def need(ok: bool, message: str) -> None:
    if not ok:
        raise L3GReleaseError("L3-G research release qualification: " + message)


def models_from_reconstructed(values: dict) -> dict:
    """Decode only the four known JSON artifacts from L3-F."""
    return {
        "thermal": json.loads(values[("PtXFlex", l3f.thermal.OUT_JSON)]),
        "site": json.loads(values[("PtXFlex", l3f.site.OUT_JSON)]),
        "cost": json.loads(values[("PtXLens", l3f.costs.OUT_JSON)]),
        "bafu": json.loads(values[("PtXLens", l3f.bafu.OUT_JSON)]),
    }


def cross_validate(models: dict) -> dict:
    """Independent semantic consistency of source, capacity, service, 19 BOM rows.

    This is in addition to byte-for-byte L3-F reconstruction, NOT a substitute.
    All site-specific, verified hardware and environmental claims remain blocked.
    """
    need(type(models) is dict and
         set(models) == {"thermal", "site", "cost", "bafu"},
         "four source JSON models required")
    t, s, c, b = (models[x] for x in ("thermal", "site", "cost", "bafu"))
    origin = t["origin"]
    source_blob = origin["original_F2_source_git_blob_sha1"]
    need(source_blob == s["original_published_2023_F2_TypeI_19item_Git_blob_sha1"] ==
         c["original_typeI_pressure_BOM_Git_blob_sha1"] ==
         b["original_published_F2_pressure_and_equipment_source_Git_blob"],
         "original F2 git source reference differs between research repos")
    need(origin["capacity_semantics"] == s["storage_cap_semantics"] == "max_inventory" and
         t["interpretation_gross_inventory_vs_withdrawable_usable_separated"] is True and
         c["source_F2_incremental_20t_gross_not_20t_usable"] is True,
         "gross MAX inventory confused with withdrawable storage")
    gross = origin["extra_gross_H2_at_maximum_kg"]
    usable = origin["original_pressure_swing_extra_withdrawable_H2_kg"]
    need(gross == s["original_F2_extra_gross_H2_max_inventory_kg"] == 20000. and
         usable == s["original_F2_extra_pressure_swing_usable_H2_kg"] ==
         17784.924849614785 and usable < gross,
         "gross and pressure-swing usable capacities changed or conflated")
    need(t["original_study_2022_2024_source_h2_per_hour_kg"] == 1250. and
         s["model_hydrogen_2022_2024_daily_H30_tonnes"] == 30. and
         c["matched_2022_2024_H2_daily_tonnes"] == 30. and
         b["matched_service_H2_daily_kg"] == 30000.,
         "source-year functional H2 delivery differs across repos")
    units = b["year_specific_matched_hydrogen_functional_units"]
    need(type(units) is list and len(units) == 2 and
         [(x["source_year"], x["delivered_H2_kg"],
           x["H2_hourly_delivery_same_for_both_architectures"]) for x in units] ==
         [(2022, 10950000., True), (2024, 10980000., True)],
         "source-year leap-day annual matched service absent or changed")
    economics = c["source_year_conditional_cost_limits"]
    need(set(economics) == {"2022", "2024"} and
         all(economics[str(y)]["separate_source_year_nominal_EUR"] == y and
             economics[str(y)]["original_independently_replayed_wholesale_saving_eur"] > 0 and
             economics[str(y)]["daily_source_H2_service_tonnes"] == 30.
             for y in (2022, 2024)),
         "separate historical year economic evidence cannot be combined")
    ids = origin["original_19_component_scope_ids"]
    need(type(ids) is list and len(ids) == len(set(ids)) == 19 and
         ids == [x["line_id"] for x in s["original_19_equipment_qualification_lines"]] ==
         [x["original_F2_line_id"] for x in c["nineteen_site_verified_supplier_installed_scope_lines"]] ==
         [x["original_F2_source_BOM_line_id"] for x in
          b["separate_19_manufacturer_and_provider_flow_requirements"]],
         "original 19 F2 BOM/PED/OEM/BAFU categories do not match")
    need(len(s["engineering_domains_to_review"]) == 13 and
         len({x["domain"] for x in s["engineering_domains_to_review"]}) == 13,
         "13 site safety/engineering qualification domains incomplete")
    need(len(t["scenarios"]) == 3 and
         t["thermal_endpoints_are_hypothetical"] is True and
         all(x["engineering_temperature_bounds_measured"] is False and
             x["actual_OEM_vessel_count"] is None and
             x["pressure_design_certified_under_EU_PED"] is False
             for x in t["scenarios"]),
         "thermal SCREEN falsely labelled as actual design")
    need(s["site_pressure_design_engineering_qualified"] is False and
         s["OEM_and_supplier_all_in_installed_cost_admitted"] is False and
         all(x["actual_qualified_installed_quantity"] is None and
             x["supplier_provenance_independently_verified"] is False
             for x in s["original_19_equipment_qualification_lines"]),
         "actual OEM/PED hardware prematurely certified")
    need(c["all_in_actual_installed_incremental_CAPEX_eur"] is None and
         c["site_project_commercial_NPV_authorized"] is False and
         all(x["incremental_real_supplier_initial_CAPEX_EUR"] is None and
             x["real_supplier_price_can_be_used_in_NPV"] is False
             for x in c["nineteen_site_verified_supplier_installed_scope_lines"]),
         "hypothetical CAPEX threshold turned into real installed NPV")
    need(b["source_empty_equipment_1924800kg_NOT_virgin_steel_or_procurement"] is True and
         b["original_native_BAFU_2026_v11_incremental_total_kgCO2e"] is None and
         b["incremental_lifecycle_GWP_kgCO2e_per_kg_delivered_H2"] is None and
         b["environmental_superiority_accepted"] is False and
         b["scientific_v1_0_native_LCA_gate_passed"] is False and
         all(x["actual_fabricated_material_INPUT_kg_not_empty_equipment"] is None and
             x["native_openLCA_product_system_link_rerun"] is False
             for x in b["separate_19_manufacturer_and_provider_flow_requirements"]),
         "reference vessel equipment mass misused as native steel/LCIA")
    grid = b["separate_year_specific_operational_energy"]
    need([(x["source_year"], x["CO2e_delta_not_inferable_from_energy_or_prices"])
          for x in grid] == [(2022, True), (2024, True)] and
         grid[0]["delta_annual_net_grid_import_MWh"] > 0 and
         grid[1]["delta_annual_net_grid_import_MWh"] < 0,
         "grid import sign or carbon-accounting scope silently changed")
    return {
        "original_F2_reference_git_blob_sha1": source_blob,
        "declared_storage_mode": "max_inventory",
        "incremental_gross_MAX_H2_kg": gross,
        "incremental_reference_pressure_swing_usable_H2_kg": usable,
        "matched_delivery_kg_per_hour": 1250.,
        "independent_historical_case_years": [2022, 2024],
        "source_year_annual_matched_service_kg": {
            "2022": 10950000., "2024": 10980000.
        },
        "physical_reference_supplier_BOM_categories": len(ids),
        "engineering_documentary_domains": 13,
        "hypothetical_thermal_screens": 3,
        "actual_site_or_manufacturer_certification": False,
        "actual_installed_cost_or_NPV_authorized": False,
        "native_BAFU_LCIA_reproduced": False,
    }


def _claim(cid: str, statement: str, scope: str, references: list[str]) -> dict:
    return {
        "id": cid, "claim": statement, "admissible_scope": scope,
        "evidence_relative_paths": references,
    }


def audit(*, lens_results: Path, flex_results: Path) -> dict:
    """L3-F exact-source eight-file audit followed by paired semantic audit."""
    evidence = l3f.audit(lens_results=lens_results, flex_results=flex_results)
    checked = cross_validate(models_from_reconstructed(l3f.reconstruct()))
    rows = evidence["exactly_eight_public_safe_research_reports"]
    names = {row["repo"] + "/" + row["relative_path"] for row in rows}

    def ref(repo: str, filename: str) -> str:
        key = repo + "/data/results/" + filename
        need(key in names, "claim lacks byte-rebuilt supporting public file: " + key)
        return key

    therm = ref("PtXFlex", l3f.thermal.OUT_JSON)
    site = ref("PtXFlex", l3f.site.OUT_JSON)
    cost = ref("PtXLens", l3f.costs.OUT_JSON)
    bafu = ref("PtXLens", l3f.bafu.OUT_JSON)
    allowed = [
        _claim("R01", "Same modelled 30t/day H2 in both architectures in each year",
               "independently replayed source-year research model; 2022 and 2024 never merged",
               [cost, bafu]),
        _claim("R02", "Original F2 additional MAX inventory 20,000 kg and distinct "
               "pressure-swing reference usable 17,784.925 kg",
               "source-locked paper reference, NOT guaranteed site deliverability",
               [therm, site]),
        _claim("R03", "Three real-gas hydrogen endpoint FREE-volume sensitivity screens",
               "analyst temperature endpoints, NOT validated transient bank design",
               [therm]),
        _claim("R04", "Separate positive 2022-like/2024-like model wholesale savings "
               "and hypothetical zero-NPV incremental CAPEX ceilings",
               "conditional historical source-price repetition; NOT actual investment NPV",
               [cost]),
        _claim("R05", "Source-year signed grid-import differences are reported",
               "electricity inventory only; NOT lifecycle carbon or climate superiority",
               [bafu]),
        _claim("R06", "Original F2 BOM coverage consistent across 19 cost, PED and "
               "native BAFU foreground categories",
               "evidence requirements only; not actual manufactured material inventory",
               [site, cost, bafu]),
    ]
    blocked = [
        _claim("B01", "Selected OEM bank quantities, materials, and PED/site safety approval",
               "blocked: independent manufacturer and engineering evidence missing",
               [therm, site]),
        _claim("B02", "Actual installed project CAPEX/OPEX/replacements and investable NPV",
               "blocked: authenticated signed OEM quotes and site contracts missing",
               [cost, site]),
        _claim("B03", "Native BAFU:2026 v1.1 product system manufacturing/replacement/EOL LCIA",
               "blocked: native process/provider flows, real material masses and rerun absent",
               [bafu]),
        _claim("B04", "Lifecycle GHG benefit or environmental superiority",
               "blocked: native manufacturing LCIA and matched-hourly operational impact missing",
               [bafu]),
        _claim("B05", "Unqualified general scientific v1.0 and plant-operational validity",
               "blocked: external experimental validation and B01-B04 remain unresolved",
               [therm, site, cost, bafu]),
    ]
    need(len(allowed) == 6 and len(blocked) == 5,
         "claim ledger rows changed without audit")
    return {
        "schema_version": SCHEMA,
        "decision": "L3G_SOURCE_RESEARCH_EVIDENCE_ADMISSIBLE_FULL_SCIENTIFIC_V1_BLOCKED",
        "source_L3F_exact_rebuild_schema": evidence["schema_version"],
        "exact_original_source_rebuilt_report_count": len(rows),
        "public_artifact_fingerprints_only": rows,
        "cross_repository_semantic_contract": checked,
        "permitted_scoped_research_claims": allowed,
        "blocked_unsupported_project_and_v1_claims": blocked,
        "gates": {
            "eight_public_source_rebuilds": True,
            "matched_source_2022_2024_service_and_research_scope": True,
            "cross_repository_F2_cost_native_material_consistency": True,
            "authenticated_OEM_and_PED_design": False,
            "quoted_installed_CAPEX_and_project_NPV": False,
            "native_BAFU_2026_v11_LCIA": False,
            "experimentally_validated_station_operation": False,
            "unqualified_scientific_v1_0_release": False,
        },
        "original_hourly_MILP_rerun_by_L3G": False,
        "original_private_source_or_vendor_archive_processed": False,
        "any_git_staging_commit_or_push_performed": False,
    }


def markdown(manifest: dict) -> str:
    lines = [
        "# L3-G cross-repository PtX research release qualification (NOT scientific v1.0)",
        "",
        "Eight L3-F public-source research records were regenerated byte-for-byte "
        "and checked across PtXFlex and PtXLens. This admits ONLY carefully "
        "qualified claims about source-year research modelling, not industrial "
        "engineering, financial, or environmental certification.",
        "",
        "## Scoped public claims", "",
        "| Claim | Admissible, qualified statement |",
        "|---|---|",
    ]
    for row in manifest["permitted_scoped_research_claims"]:
        lines.append("| " + row["id"] + " | " + row["claim"] +
                     " — " + row["admissible_scope"] + " |")
    lines += ["", "## Evidence still blocking scientific v1.0", "",
              "| Gate | Why blocked |", "|---|---|"]
    for row in manifest["blocked_unsupported_project_and_v1_claims"]:
        lines.append("| " + row["id"] + " | " + row["admissible_scope"] + " |")
    lines += [
        "", "The historical 2022 and 2024 price/supply runs are separate "
        "counterfactuals, **not** a forecast or probability distribution. "
        "The pressure-screened 200/20 bar values are **absolute**, not "
        "manufacturer-certified PED MAWP. The original reference 802 × "
        "2400 kg is empty equipment, **not** virgin steel production mass. "
        "No BAFU native LCIA, supplier quotation, authenticated station "
        "design or project NPV has been accepted.",
        "",
        "This report contains only relative filenames and SHA-256 digests of "
        "source-rebuilt **public** files. It neither uploads nor inspects "
        "private originals, archives, models or original hourly witnesses.",
        "",
        "**Release decision: research claim ledger reproducible; "
        "unqualified scientific v1.0 BLOCKED.**",
        "",
    ]
    return "\n".join(lines)


def publish_local(manifest: dict, *, output_dir: Path, verify_only: bool) -> None:
    output_dir = Path(output_dir)
    need(output_dir.is_dir() and not output_dir.is_symlink(),
         "public output directory missing or symlinked")
    outputs = [
        (output_dir / OUT_JSON, json.dumps(
            manifest, sort_keys=True, indent=2, allow_nan=False) + "\n"),
        (output_dir / OUT_MD, markdown(manifest)),
    ]
    for path, body in outputs:
        need(not path.is_symlink() and
             (not path.exists() or
              (path.is_file() and path.read_bytes() == body.encode("utf-8"))),
             "existing release report differs (refusing overwrite): " + path.name)
        need(not verify_only or path.is_file(),
             "verify-only requires previously created report: " + path.name)
    if not verify_only:
        for path, body in outputs:
            if not path.exists():
                with path.open("x", encoding="utf-8", newline="\n") as f:
                    f.write(body)


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--lens-results", type=Path, required=True)
    p.add_argument("--flex-results", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--verify-only", action="store_true")
    a = p.parse_args(argv)
    manifest = audit(lens_results=a.lens_results, flex_results=a.flex_results)
    publish_local(manifest, output_dir=a.output_dir, verify_only=a.verify_only)
    print(manifest["decision"])
    print("Eight exact-source L3-F artifacts, 19 BOM lines, 13 site domains, "
          "six scoped public claims, five blocked scientific/industrial claims")
    print("No private data, git publication, original MILP, OEM/PED, native BAFU "
          "LCIA or actual investment approval was performed")


if __name__ == "__main__":
    main()
