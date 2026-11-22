"""Hermetic regression of BAFU OGD v1 -> stationary Type I native v1.1 candidate crosswalk.

All catalogue fixtures are fabricated process *names* and UUIDs to exercise
the contract, explicitly NOT actual BAFU datasets or environmental factors.
"""
import csv
import hashlib
import json

import pytest

from ptxlens.bafu_candidates import FIELDS
from ptxlens.bafu_real_screen import PROCESSES
import ptxlens.l3b_bafu_ogd_native_crosswalk as m


def fake_catalogue(tmp_path):
    path=tmp_path/"SYNTHETIC_BAFU_v1_like_catalogue.csv"
    manifest=tmp_path/"SYNTHETIC_source_manifest.json"
    with path.open("w",newline="",encoding="utf-8") as stream:
        w=csv.DictWriter(stream,fieldnames=FIELDS)
        w.writeheader()
        original={
            **{v[0]:v for v in PROCESSES.values()},
        }
        for i in range(11947):
            uid=f"{i:08x}-1111-4222-8333-{i:012x}"
            name=f"TEST ONLY — synthetic process {i}"
            loc="RER";unit="kg"
            if i==0:
                name="Steel, low-alloyed, at plant"
            if i==1:
                name="Sheet rolling, chromium steel"
            if i==2:
                name="Concrete, normal, at plant"
            if i==3:
                name="Transport, freight, lorry 16-32 t";unit="t*km"
            if i==4:
                name="Steel scrap recycling"
            if i==5:
                name="Electricity, medium voltage, at grid";unit="MJ"
            w.writerow({
                "uuid":uid,"processName":name,"location":loc,
                "referenceUnit":unit,"version":m.VERSION,
                "impactMethod":m.METHOD,"impactCategory":m.CATEGORY,
                "impactCategoryUnit":"kg CO2-eq","value":"99",
                "isSingleScore":"False","category":"TEST_ONLY",
                "lastDatasetUpdateYear":"2026","sourceStudy":"SYNTHETIC",
                "sourceStudyAuthor":"TEST_ONLY",
            })
        # Replace the LAST five rows with registered, source-specified UUIDs,
        # preserving exactly 11,947 unique synthetic catalogue identities.
    with path.open(newline="",encoding="utf-8") as stream:
        rows=list(csv.DictReader(stream))
    keys=list(PROCESSES.keys())
    for i,alias in enumerate((*m.FINGERPRINTS,m.DISALLOWED_ALIAS)):
        uid,name,loc,unit=PROCESSES[alias]
        rows[-(i+1)].update(uuid=uid,processName=name,location=loc,referenceUnit=unit)
    with path.open("w",newline="",encoding="utf-8") as stream:
        w=csv.DictWriter(stream,fieldnames=FIELDS)
        w.writeheader();w.writerows(rows)
    manifest.write_text(json.dumps({
      "schema_version":"ptxlens.bafu_2026_complete_gwp100_source_manifest.v0.2",
      "database_version":m.VERSION,
      "impact_method":m.METHOD,
      "impact_category":m.CATEGORY,
      "all_16_hex_partitions_covered":True,
      "uuid_partitions_attempted":"0123456789abcdef",
      "endpoint":m.SOURCE,
      "confirmed_native_openlca_product_system_completeness":False,
      "provider_records":11947,
      "catalogue_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
    }))
    return path,manifest


@pytest.mark.parametrize("mode,n",[("max_inventory",802),("usable_service",902)])
def test_all_19_original_stationary_classes_have_traceable_but_unapproved_candidates(tmp_path,mode,n):
    catalogue,manifest=fake_catalogue(tmp_path)
    r=m.crosswalk(mode,catalogue,manifest)
    assert r["schema_version"]==m.SCHEMA
    assert r["source_reference_additional_vessels_model_not_vendor"]==n
    assert r["source_official_catalogue_process_count"]==11947
    assert r["native_v11_flow_tech_and_provider_mapping_approved_count"]==0
    assert r["original_licensed_BAFU_v11_actually_imported_or_read_for_this_crosswalk"] is False
    assert r["unresolved_nonzero_foreground_classes_count"]==19
    assert {x["foreground_equipment_class"] for x in r["foreground_equipment"]}==m.EXPECTED_DOC_BOM
    assert r["full_GWP100_or_LCOH_or_investment_releasable"] is False
    for row in r["foreground_equipment"]:
        assert row["native_BAFU_v11_approved_supplier_process_uuid"] is None
        assert row["manufacturer_raw_alloy_kg_by_grade"] is None
        assert row["unknown_material_or_process_burden_not_zero"] is True
    for group,info in r["public_v1_groups"].items():
        assert len(info["possibly_relevant_processes_not_native_approved"])<=8
        assert not any(x["uuid"]==m.FORBIDDEN_BAFU_VEHICLE_PROCESS
                       for x in info["possibly_relevant_processes_not_native_approved"])


def test_actual_known_source_v1_stainless_copper_aluminium_grid_appear_only_as_candidates(tmp_path):
    c,mf=fake_catalogue(tmp_path)
    x=m.crosswalk("max_inventory",c,mf)
    for group,alias in (("stainless_steel","stainless_18_8"),
                        ("copper","copper"),
                        ("aluminium","aluminium_primary"),
                        ("electricity","grid_nl_high_voltage")):
        matches=x["public_v1_groups"][group]["possibly_relevant_processes_not_native_approved"]
        assert any(row["uuid"]==PROCESSES[alias][0] for row in matches)
        assert all(row["native_v11_quantitative_reference_verified"] is False for row in matches)


def test_tampered_official_csv_fails_before_any_crosswalk(tmp_path):
    c,mf=fake_catalogue(tmp_path)
    c.write_text(c.read_text()+"INJECTED")
    with pytest.raises(m.BafuCrosswalkEvidenceError,match="SHA256"):
        m.crosswalk("max_inventory",c,mf)


def test_inconsistent_original_process_identity_fails_even_with_new_hash(tmp_path):
    c,mf=fake_catalogue(tmp_path)
    original=c.read_text()
    c.write_text(original.replace("Chromium steel 18/8, at plant","Steel, generic, at plant"))
    data=json.loads(mf.read_text())
    data["catalogue_sha256"]=hashlib.sha256(c.read_bytes()).hexdigest()
    mf.write_text(json.dumps(data))
    with pytest.raises(m.BafuCrosswalkEvidenceError,match="process UUID"):
        m.crosswalk("usable_service",c,mf)


def test_fake_v11_version_or_partial_catalogue_fails_closed(tmp_path):
    c,mf=fake_catalogue(tmp_path)
    data=json.loads(mf.read_text())
    data["database_version"]="BAFU:2026 v1.1"
    mf.write_text(json.dumps(data))
    with pytest.raises(m.BafuCrosswalkEvidenceError,match="original complete"):
        m.crosswalk("max_inventory",c,mf)


def test_manifest_do_not_derive_fabrication_material_mass_from_reference_vessel(tmp_path):
    c,mf=fake_catalogue(tmp_path)
    x=m.crosswalk("usable_service",c,mf)
    tank=next(z for z in x["foreground_equipment"] if
              z["foreground_equipment_class"]=="typeI_200bar_bare_reference_vessels")
    assert tank["published_reference_incremental_vessel_count_NOT_actual_supplier_order"]==902
    assert tank["installed_subcomponent_quantity"] is None
    assert tank["manufacturer_raw_alloy_kg_by_grade"] is None
    assert tank["native_BAFU_v11_approved_supplier_process_uuid"] is None
