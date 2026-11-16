import hashlib
import json
from pathlib import Path

import pytest
from ptxlens.core import crf, assess, inventory
from ptxlens.pynexus import inspect_verified_artifact

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "illustrative.json"

@pytest.fixture
def case():
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))

def test_crf():
    assert crf(0,20) == pytest.approx(.05)
    assert crf(.07,20) == pytest.approx(.0943929257)

def test_cost_and_carbon_independent_arithmetic(case):
    result = assess(case)
    annual_h2 = 84 * 2190
    assert result["annual_delivered_h2_kg"] == annual_h2
    c = result["cost_eur_per_year"]
    cap = (1200000 + 100000 / 1.07**10) * crf(.07,20)
    assert c["annualized_capital_eur"] == pytest.approx(cap)
    assert c["wholesale_grid_settlement_eur"] == pytest.approx((60 - 2.5)*2190)
    assert c["declared_wind_value_eur"] == pytest.approx(2.5*35*2190)
    g = result["gwp_kgco2e_per_year"]
    assert g["electricity_factor_kgco2e"] == pytest.approx((15 + 400 + 7.5 + 150 + 15)*2190)
    assert g["annualized_embodied_kgco2e"] == 5500
    assert result["screening_gwp_kgco2e_per_kg_delivered"] == pytest.approx(sum(g.values())/annual_h2)

def test_staging_is_not_lcia(case):
    x = inventory(case)
    assert "NOT calculated in openLCA" in x["status"]
    assert x["reference_product"]["amount"] == 84*2190

@pytest.mark.parametrize("field,value", [
    ("wind_mwh", -1), ("grid_import_mwh", -1), ("grid_gwp_kgco2e_mwh", -1),
    ("h2_delivered_kg", -1), ("grid_price_eur_mwh", float("nan")),
])
def test_invalid_physics_fails_closed(case, field, value):
    case["hours"][0][field] = value
    with pytest.raises(ValueError):
        assess(case)

def test_missing_evidence_and_wrong_year_fail_closed(case):
    case["evidence"]["kind"] = "pynexus_frozen"
    with pytest.raises(ValueError):
        assess(case)
    case = json.loads(EXAMPLE.read_text())
    case["metadata"]["annualization_factor"] = 1
    with pytest.raises(ValueError):
        assess(case)

def test_dual_grid_flow_rejected(case):
    case["hours"][0]["grid_import_mwh"] = 1
    case["hours"][0]["grid_export_mwh"] = 1
    with pytest.raises(ValueError):
        assess(case)

def test_zero_delivered_rejected(case):
    for x in case["hours"]:
        x["h2_delivered_kg"] = 0
    with pytest.raises(ValueError, match="zero delivered"):
        assess(case)

def test_source_file_integrity_gate(tmp_path):
    csv = tmp_path / "dispatch.csv"
    csv.write_text("hour,h2\n0,1\n1,2\n", encoding="utf-8")
    meta = tmp_path / "run_manifest.json"
    meta.write_text(json.dumps({"verified": True, "snapshots": 2,
        "dispatch_sha256": hashlib.sha256(csv.read_bytes()).hexdigest()}))
    assert inspect_verified_artifact(csv, meta)["rows"] == 2
    csv.write_text(csv.read_text() + "2,3\n")
    with pytest.raises(ValueError):
        inspect_verified_artifact(csv, meta)
