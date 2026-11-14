"""Native-original BAFU v1.1 source-evidence parser negative and positive unit tests.

Hermetic TSV is fabricated ONLY to test parsing. Without original protected
135,424,513-byte source with exact SHA, NO native validation can pass.
"""
import csv
import json
from pathlib import Path

import pytest

import ptxlens.l3b_bafu_original_native_v11_reconcile as m
from ptxlens.bafu_real_screen import PROCESSES


def synthetic_private_native_table(tmp_path,*,found=True):
    path=tmp_path/"SYNTHETIC_BAFU_v11_process_reference_NOT_REAL.tsv"
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,delimiter="\t",fieldnames=m.HEADERS)
        w.writeheader()
        for alias in ("stainless_18_8","aluminium_primary","copper",
                      "grid_nl_high_voltage","h2_high_pressure_tank"):
            uuid,name,geo,unit=PROCESSES[alias]
            w.writerow({
                "schema_version":m.NATIVE_SCHEMA,
                "original_zolca_SHA256":m.NATIVE_SHA,
                "process_UUID":uuid,
                "native_process_found":"true" if found else "false",
                "native_process_name":name if found else "NULL",
                "quantitative_flow_UUID":uuid if found else "NULL",
                "quantitative_flow_name":name if found else "NULL",
                "quantitative_ref_unit":unit if found else "NULL",
                "quantitative_ref_flow_type":"PRODUCT_FLOW" if found else "NULL",
            })
    return path


def test_hermetic_native_reference_export_parses_but_is_not_source_admission(tmp_path):
    path=synthetic_private_native_table(tmp_path)
    records=m.parse_private_native_table(path)
    assert len(records)==5
    assert records[PROCESSES["stainless_18_8"][0]]["quantitative_ref_unit"]=="kg"
    assert records[PROCESSES["grid_nl_high_voltage"][0]]["quantitative_ref_unit"]=="MJ"
    assert all(r["native_process_found"]=="true" for r in records.values())


def test_synthetically_missing_native_process_does_not_gain_fake_reference_flow(tmp_path):
    path=synthetic_private_native_table(tmp_path,found=False)
    records=m.parse_private_native_table(path)
    assert all(r["quantitative_flow_UUID"]=="NULL" for r in records.values())


def test_native_waste_reference_does_not_convert_to_material_product_flow(tmp_path):
    path=synthetic_private_native_table(tmp_path)
    content=path.read_text()
    path.write_text(content.replace("PRODUCT_FLOW","WASTE_FLOW",1))
    records=m.parse_private_native_table(path)
    assert any(x["quantitative_ref_flow_type"]=="WASTE_FLOW" for x in records.values())
    # Syntactically valid source metadata is only a candidate; native
    # product-system suitability still needs crosswalk role and source review.


def test_original_source_absent_is_nonnegotiable_even_if_fake_table_claims_valid_SHA(tmp_path):
    fakecross=tmp_path/"FAKE_OGD.json"
    fakecross.write_text(json.dumps({"schema_version":"fake"}))
    tsv=synthetic_private_native_table(tmp_path)
    with pytest.raises(m.BafuCrosswalkEvidenceError,match="EXACT original"):
        m.reconcile(fakecross,tmp_path/"DOES_NOT_EXIST.zolca",tsv)


def test_forged_native_process_reference_unit_or_source_sha_fails(tmp_path):
    tsv=synthetic_private_native_table(tmp_path)
    raw=tsv.read_text()
    tsv.write_text(raw.replace(m.NATIVE_SHA,"0"*63+"1"))
    with pytest.raises(m.BafuCrosswalkEvidenceError,match="invalid native v1.1 SHA"):
        m.parse_private_native_table(tsv)


def test_invalid_duplicate_uuid_and_spurious_flow_for_absent_process_fail(tmp_path):
    tsv=synthetic_private_native_table(tmp_path)
    text=tsv.read_text()
    tsv.write_text(text+text.splitlines(keepends=True)[1])
    with pytest.raises(m.BafuCrosswalkEvidenceError,match="duplicate"):
        m.parse_private_native_table(tsv)
    tsv=synthetic_private_native_table(tmp_path,found=False)
    text=tsv.read_text()
    first=PROCESSES["stainless_18_8"][0]
    tsv.write_text(text.replace("false\tNULL\tNULL\tNULL\tNULL",
                                f"false\tNULL\t{first}\tNULL\tNULL",1))
    with pytest.raises(m.BafuCrosswalkEvidenceError,match="missing native provider"):
        m.parse_private_native_table(tsv)


def test_refuse_native_v1_itself_as_original_v11_license_source(tmp_path):
    tsv=synthetic_private_native_table(tmp_path)
    source=tmp_path/"SYNTHETIC_2026_v1.1.zolca"
    source.write_bytes(b"NOT ORIGINAL")
    with pytest.raises(m.BafuCrosswalkEvidenceError,match="EXACT original"):
        m.reconcile(tmp_path/"dummy.json",source,tsv)
