"""L3-A figures are reproducible actual vector plots, not decorative snapshots.

Verify original CI figure hashes and source provenance in Git. With optional
matplotlib installed, recompute twice and require byte-for-byte stable SVG.
Checks fail if assumptions, plot labels or source/year notes are removed.
"""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest


ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"research/L3_A_2023_reproducible_sensitivity_figure_SHA_register_v1.json"


def test_source_generated_vector_charts_frozen_and_original_economic_source_claims():
    d=json.loads(REGISTRY.read_text())
    assert d["schema_version"]=="ptxlens.l3a_2023_source_locked_economic_sensitivity_svg_vector_figures.v1"
    assert d["data_source_year"]==2023
    assert d["source_f3c_sha256"]=="dddd07d5c0a3d4f276e80af44e28cf3cfdbc93421107fb5d9e39843a0d1d90e2"
    assert d["full_research_sensitivity_json_sha256"]=="142a1eac14b946c8b491a92991ab9b6cd21dd3dd0b5f9c0018b43666cd9165ba"
    assert d["fixed_svg_hashsalt"]=="OEM-PTX-2026-01-L3A-2023-source"
    assert d["matplotlib_version"]=="3.11.2"
    assert d["numpy_version"]=="2.5.4"
    assert d["same_real_service_duty_within_mode_only"]
    assert not d["actual_vendor_lifetime_project_DCF_calculated"]
    assert not d["complete_GWP_LCOH_or_full_2023_h2_contract"]
    assert set(d["figure_svg_files"])=={"discount_lifetime","opex_capex","max_inventory","usable_service"}
    for key,figure in d["figure_svg_files"].items():
        path=ROOT/figure["path"]
        assert path.is_file()
        raw=path.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==figure["sha256"],key
        root=ET.fromstring(raw)
        assert root.tag.endswith("svg")
        assert len(raw)>10000
        assert b"2023" in raw
        assert b"source" in raw.lower()
        assert b"CAPEX" in raw or b"OPEX" in raw


def test_matplotlib_native_svg_generation_repeats_same_output_and_reconciles_with_source_run(tmp_path):
    pytest.importorskip("matplotlib")
    pytest.importorskip("numpy")
    from ptxlens.l3a_sensitivity_figures import generate
    x=generate(tmp_path/"a")
    y=generate(tmp_path/"b")
    d=json.loads(REGISTRY.read_text())["figure_svg_files"]
    assert x["schema_version"]==y["schema_version"]
    assert not x["actual_h2_storage_capex_OPEX_and_LCOH_available"]
    for key in d:
        assert x["charts"][key]["svg_sha256"]==y["charts"][key]["svg_sha256"]
        assert x["charts"][key]["svg_sha256"]==d[key]["sha256"]
