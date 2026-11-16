"""Source-registered 8,760-hour *modelled* H2 shortage timing, no 2023 raw wind/price."""
import hashlib
import json
import math
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]/"data/results"
EXPECTED={
  "max_inventory":"9acefa605c878e19f369f57cd94519fc9dd926beda284135529b7d89ce31208e",
  "usable_service":"9c66837c105e5c17e2fbdceb50250a2ea7940ac0a2a321a08ffec8cf81622999",
}
ORIGINAL_E="069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051"
ORIGINAL_ES="cd4101fe62c3f1b8aa2d7508d3651d2fee40d2bafe6d5b87e40d5f4d055070f9"

@pytest.mark.parametrize("mode",["max_inventory","usable_service"])
def test_independent_registered_2023_hourly_shortage_sequence(mode):
    p=ROOT/f"F3_2023_original_E_sparse_H2_backup_need_{mode}.json"
    raw=p.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==EXPECTED[mode]
    x=json.loads(raw)
    assert x["schema_version"]=="ptxflex.f3_2023_sparse_modelled_backup_hourly_need.v1"
    assert x["capacity_semantics"]==mode
    assert x["source_model_E_zip_sha256"]==ORIGINAL_E
    assert x["source_model_E_plus_S_zip_sha256"]==ORIGINAL_ES
    assert x["source_8760_hourly_count"]==8760
    assert x["source_hour_index_is_zero_based_and_not_fabricated_date_time"]
    assert x["zero_kg_h_at_all_hours_not_listed"]
    assert x["modelled_need_not_actual_hydrogen_supplier_delivery"]
    assert x["source_2026_network_not_observed_2023_H2_supply"]
    assert not x["actual_supplier_capacity_and_quality_pressure_checked"]
    assert not x["full_LCA_TEA_qualified"]
    assert x["external_supply_kgCO2e_per_kg"] is None
    assert x["external_supply_EUR_per_kg"] is None
    rows=x["positive_H2_topup_needed_kg_by_0_based_source_hour"]
    assert len(rows)==x["positive_hours"]
    indexes=[r["hour_index_0_based"] for r in rows]
    assert indexes==sorted(set(indexes))
    assert all(0<=i<8760 for i in indexes)
    assert all(r["additional_modelled_H2_kg"]>0 for r in rows)
    a=[0.]*8760
    for r in rows:a[r["hour_index_0_based"]]=r["additional_modelled_H2_kg"]
    assert math.isclose(sum(a),x["modelled_additional_annual_topup_for_feasible_incumbent_kg"],abs_tol=.002)
    assert math.isclose(max(a),x["source_incumbent_peak_kg_h"],abs_tol=.002)
    assert math.isclose(max(sum(a[i:i+24]) for i in range(8737)),x["source_incumbent_max_rolling_24h_kg"],abs_tol=.002)
    indicator=[n>0 for n in a]
    starts=sum(1 for i,yes in enumerate(indicator) if yes and (i==0 or not indicator[i-1]))
    assert starts==x["event_count"]
    assert sum(indicator)==x["positive_hours"]
    source=json.loads((ROOT/f"F3_2023_original_E_source_hypothetical_backup_{mode}.json").read_text())
    assert abs(sum(a)-source["single_incumbent_hypothetical_topup_annual_kg"])<.002
    assert x["source_registered_stageB_derived_summary_sha256"]==(
      "c65fda894ef4b30e09339ad88a3972625af78c17802fd0cb9a2fc25d3205882f"
      if mode=="max_inventory" else
      "d893c6388f14d276b2ef5d4bff4b6c8057dd252067f307f83b9baafcfa1e5308"
    )
