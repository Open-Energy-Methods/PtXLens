"""Regression checks against real native source-identified results, not calculated substitutes."""
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/"data/results/BAFU2026_v11_native_E_ES_2023_verified_summary.json"
REGISTER=ROOT/"data/source_registry/pynexus_wp5_2023.json"

def test_actual_source_hashes_and_hydrogen_capacity():
    d=json.loads(RESULTS.read_text())
    r=json.loads(REGISTER.read_text())
    assert d["native_method"]["exact_impact_category"]=="IPCC 2021 GWP 100"
    assert d["source"]["bafu_native_edition"]=="BAFU:2026 v1.1"
    assert d["source"]["source_raw_dataset_distributed"] is False
    assert d["historical_2023_original_scenarios"][0]["source_archive_sha256"]==r["base"]["archive_sha256"]
    assert d["historical_2023_original_scenarios"][1]["source_archive_sha256"]==r["storage"]["archive_sha256"]
    assert r["base"]["storage_kg"]==20000 and r["storage"]["storage_kg"]==40000
    assert d["scenario_model_changes"]["additional_e_plus_s_capacity_kg_h2"]==20000

def test_real_native_GWP_and_independent_source_reference():
    d=json.loads(RESULTS.read_text())
    ref=d["native_reference_CH"]
    assert math.isclose(ref["gwp100_kgco2e_per_kg_h2"],5.541965561665505,abs_tol=1e-12)
    assert ref["unlinked_product_inputs"]==ref["unlinked_waste_outputs"]==0
    cases={v["id"]:v for v in d["historical_2023_original_scenarios"]}
    assert cases["E"]["native_gwp100_kgco2e_per_kg_model_delivered_h2"]==6.148174395784
    assert cases["E_plus_S"]["native_gwp100_kgco2e_per_kg_model_delivered_h2"]==6.0765526538929
    for item in cases.values():
        assert item["native_linked_processes"]==4240
        assert item["native_links"]==52123
        assert item["unlinked_product_inputs"]==item["unlinked_waste_outputs"]==0
        assert abs(item["native_gwp100_kgco2e_per_kg_model_delivered_h2"]-item["independent_corrected_BAFU_v1_source_factor_kgco2e_per_kg_h2"])<2e-8

def test_research_claims_exclude_unmodelled_storage():
    d=json.loads(RESULTS.read_text())
    c=d["scientific_claims"]
    assert c["E_native_LCIA_executed"] and c["E_plus_S_native_LCIA_executed"]
    assert c["full_2023_nl_E_vs_ES_matched_service_comparison_completed"] is False
    assert c["e_plus_s_added_storage_compression_and_losses_included"] is False
    assert c["published_GWP_per_kg_may_not_establish_ES_superiority"] is True
