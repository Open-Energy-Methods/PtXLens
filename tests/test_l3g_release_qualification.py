"""L3-G paired-source scientific release: positive, tamper, and false-claim tests."""
import copy
import json

import pytest

from ptxlens import l3f_publication_admission as l3f
from ptxlens import l3g_release_qualification as m


def staged(tmp_path):
    lens = tmp_path / "PtXLens" / "data" / "results"
    flex = tmp_path / "PtXFlex" / "data" / "results"
    lens.mkdir(parents=True)
    flex.mkdir(parents=True)
    for (repo, name), body in l3f.reconstruct().items():
        path = (flex if repo == "PtXFlex" else lens) / name
        path.write_text(body, encoding="utf-8", newline="\n")
    return lens, flex


def models():
    return m.models_from_reconstructed(l3f.reconstruct())


def test_paired_semantics_source_ids_annual_service_and_blocked_claims(tmp_path):
    lens, flex = staged(tmp_path)
    report = m.audit(lens_results=lens, flex_results=flex)
    consistency = report["cross_repository_semantic_contract"]
    assert consistency["incremental_gross_MAX_H2_kg"] == 20000.
    assert consistency["incremental_reference_pressure_swing_usable_H2_kg"] == pytest.approx(17784.924849614785)
    assert consistency["source_year_annual_matched_service_kg"] == {
        "2022": 10950000., "2024": 10980000.
    }
    assert consistency["physical_reference_supplier_BOM_categories"] == 19
    assert consistency["engineering_documentary_domains"] == 13
    assert report["exact_original_source_rebuilt_report_count"] == 8
    assert len(report["permitted_scoped_research_claims"]) == 6
    assert len(report["blocked_unsupported_project_and_v1_claims"]) == 5
    assert all(not report["gates"][key] for key in (
        "authenticated_OEM_and_PED_design",
        "quoted_installed_CAPEX_and_project_NPV",
        "native_BAFU_2026_v11_LCIA",
        "experimentally_validated_station_operation",
        "unqualified_scientific_v1_0_release",
    ))
    payload = json.dumps(report)
    assert "PtX_PRIVATE_RESEARCH" not in payload
    assert '"original_private_source_or_vendor_archive_processed": false' in payload
    assert "C:\\Users" not in payload


@pytest.mark.parametrize("case", [
    "F2_blob", "capacity_semantics", "conflate_usable",
    "annual_service", "year_order", "cost_year_mixed",
    "missing_site_category", "reordered_lca_category",
    "lost_ped_domain", "site_false_approval", "vendor_fake_cost",
    "oem_fake_count", "bafu_fake_material", "bafu_fake_lcia",
    "grid_sign", "carbon_inferred",
])
def test_negative_cross_repo_inconsistencies_fail_closed(case):
    x = copy.deepcopy(models())
    t, s, c, b = [x[k] for k in ("thermal", "site", "cost", "bafu")]
    if case == "F2_blob":
        c["original_typeI_pressure_BOM_Git_blob_sha1"] = "a" * 40
    elif case == "capacity_semantics":
        s["storage_cap_semantics"] = "usable_service"
    elif case == "conflate_usable":
        t["origin"]["original_pressure_swing_extra_withdrawable_H2_kg"] = 20000.
    elif case == "annual_service":
        b["year_specific_matched_hydrogen_functional_units"][1]["delivered_H2_kg"] = 10950000.
    elif case == "year_order":
        b["year_specific_matched_hydrogen_functional_units"].reverse()
    elif case == "cost_year_mixed":
        c["source_year_conditional_cost_limits"]["2024"]["separate_source_year_nominal_EUR"] = 2022
    elif case == "missing_site_category":
        s["original_19_equipment_qualification_lines"].pop()
    elif case == "reordered_lca_category":
        b["separate_19_manufacturer_and_provider_flow_requirements"].reverse()
    elif case == "lost_ped_domain":
        s["engineering_domains_to_review"].pop()
    elif case == "site_false_approval":
        s["site_pressure_design_engineering_qualified"] = True
    elif case == "vendor_fake_cost":
        c["all_in_actual_installed_incremental_CAPEX_eur"] = 999999.
    elif case == "oem_fake_count":
        t["scenarios"][0]["actual_OEM_vessel_count"] = 802
    elif case == "bafu_fake_material":
        b["separate_19_manufacturer_and_provider_flow_requirements"][0][
            "actual_fabricated_material_INPUT_kg_not_empty_equipment"] = 1924800.
    elif case == "bafu_fake_lcia":
        b["original_native_BAFU_2026_v11_incremental_total_kgCO2e"] = -1.
    elif case == "grid_sign":
        b["separate_year_specific_operational_energy"][0][
            "delta_annual_net_grid_import_MWh"] = -1.
    elif case == "carbon_inferred":
        b["separate_year_specific_operational_energy"][0][
            "CO2e_delta_not_inferable_from_energy_or_prices"] = False
    with pytest.raises(m.L3GReleaseError):
        m.cross_validate(x)


def test_mutated_approved_bytes_rejected_even_if_document_looks_valid(tmp_path):
    lens, flex = staged(tmp_path)
    path = lens / l3f.costs.OUT_JSON
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("source_year", "source_yeAr", 1), encoding="utf-8")
    with pytest.raises(l3f.L3FAdmissionError):
        m.audit(lens_results=lens, flex_results=flex)


def test_missing_report_rejected(tmp_path):
    lens, flex = staged(tmp_path)
    (flex / l3f.thermal.OUT_MD).unlink()
    with pytest.raises(l3f.L3FAdmissionError):
        m.audit(lens_results=lens, flex_results=flex)


def test_immutable_two_report_publishing_and_verify_only(tmp_path):
    lens, flex = staged(tmp_path)
    manifest = m.audit(lens_results=lens, flex_results=flex)
    with pytest.raises(m.L3GReleaseError, match="verify-only"):
        m.publish_local(manifest, output_dir=lens, verify_only=True)
    m.publish_local(manifest, output_dir=lens, verify_only=False)
    m.publish_local(manifest, output_dir=lens, verify_only=True)
    assert (lens / m.OUT_JSON).read_bytes().endswith(b"\n")
    assert b"\r" not in (lens / m.OUT_JSON).read_bytes()
    assert (lens / m.OUT_MD).read_text(encoding="utf-8").endswith("\n")
    assert "scientific v1.0 BLOCKED" in (lens / m.OUT_MD).read_text(encoding="utf-8")
    (lens / m.OUT_MD).write_text("SIMULATED TAMPERING", encoding="utf-8")
    with pytest.raises(m.L3GReleaseError, match="refusing overwrite"):
        m.publish_local(manifest, output_dir=lens, verify_only=False)


def test_no_generated_artifact_if_source_missing(tmp_path):
    lens, flex = staged(tmp_path)
    (flex / l3f.site.OUT_JSON).unlink()
    with pytest.raises(l3f.L3FAdmissionError):
        m.audit(lens_results=lens, flex_results=flex)
    assert not (lens / m.OUT_JSON).exists()
    assert not (lens / m.OUT_MD).exists()


def test_release_manifest_paths_are_relative_and_digests_are_source_exact(tmp_path):
    lens, flex = staged(tmp_path)
    report = m.audit(lens_results=lens, flex_results=flex)
    rows = report["public_artifact_fingerprints_only"]
    assert len(rows) == 8
    assert all(x["relative_path"].startswith("data/results/") and
               len(x["SHA256_exact_original_source_rebuilt"]) == 64
               for x in rows)
    assert report["any_git_staging_commit_or_push_performed"] is False
    assert report["original_hourly_MILP_rerun_by_L3G"] is False
