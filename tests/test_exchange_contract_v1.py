"""Scientific contract regression: real verified E/E+S examples and *test-only* tampering.

We never use synthetic values in reported LCA/engineering results. Mutations in
these tests are exclusively rejection tests; no results are published from them.
"""
import copy
import json
from pathlib import Path

import pytest
from ptxlens.exchange_contract import (
    ScientificContractError, comparable_pair, schema, validate_exchange,
)

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"contracts/examples/h2-E-2023-scoped-native-evidence.json"
ES=ROOT/"contracts/examples/h2-EplusS-2023-scoped-native-evidence.json"


def example(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_canonical_shared_schema_is_valid_2020_12_and_explicit():
    sc=schema()
    assert sc["$schema"].endswith("2020-12/schema")
    assert sc["properties"]["schema_version"]["const"]=="oem.ptx.exchange.v1.0"
    assert sc["properties"]["impact"]["$ref"]=="#/$defs/impact"


@pytest.mark.parametrize("path",[E,ES])
def test_real_native_lca_examples_are_valid_but_not_full_or_matched(path):
    d=validate_exchange(example(path))
    assert d["source"]["source_kind"]=="observed_weather_market_plus_modelled_hydrogen"
    assert d["source"]["hour_count"]==8760
    assert d["claims"]["native_lca_executed"]
    assert not d["claims"]["matched_service_comparison_eligible"]
    assert d["storage"]["empty_equipment_mass_kg"] is None
    assert d["impact"]["incremental_h2_storage_equipment_included"] is False
    assert d["impact"]["impact_status"]=="scoped_native_lcia"


def test_original_unequal_service_cannot_be_called_matched_comparison():
    with pytest.raises(ScientificContractError,match="not explicitly validated for equal operating H2 service"):
        comparable_pair(example(E),example(ES))


def test_original_source_input_price_and_weather_demand_hashes_must_be_pinned():
    for field in ("market_price_input_sha256","wind_available_input_sha256","hourly_demand_input_sha256"):
        d=example(E)
        d["source"][field]="f"*64
        with pytest.raises(ScientificContractError,match="price/weather/demand series SHA mismatch"):
            validate_exchange(d)


def test_operational_and_environmental_comparison_have_separate_gates():
    a=example(E)
    b=example(ES)
    assert a["claims"]["matched_operational_service_verified"] is False
    assert b["claims"]["matched_operational_service_verified"] is False
    for domain in ("operational","environmental"):
        with pytest.raises(ScientificContractError,match="not explicitly validated for equal operating H2 service"):
            comparable_pair(a,b,domain=domain)


def test_source_sha_tampering_is_rejected():
    d=example(E)
    d["source"]["original_source_archive_sha256"]="0"*64
    with pytest.raises(ScientificContractError,match="source archive SHA mismatch"):
        validate_exchange(d)


def test_tank_hydrogen_capacity_is_not_physical_tank_mass():
    d=example(E)
    d["storage"]["empty_equipment_mass_kg"]=20000
    with pytest.raises(ScientificContractError,match="cannot declare a tank equipment mass"):
        validate_exchange(d)


def test_partial_pressure_specification_is_not_a_valid_vessel_design():
    d=example(E)
    d["storage"]["minimum_pressure_bar"]=30
    with pytest.raises(ScientificContractError,match="pressure bounds must both"):
        validate_exchange(d)


def test_scoped_native_GWP_is_not_full_life_cycle_comparison():
    d=example(ES)
    d["impact"]["full_plant_boundary"]=True
    with pytest.raises(ScientificContractError,match="full boundary cannot be a partial"):
        validate_exchange(d)


def test_openlca_method_category_must_match_exactly():
    d=example(E)
    d["impact"]["category"]="AGWP 100"
    with pytest.raises(ScientificContractError,match="exact native IPCC"):
        validate_exchange(d)


def test_method_only_versus_full_DCF_cost_claim():
    d=example(E)
    d["economics"]["full_levelized_cost_per_delivered_kg"]=1.558
    with pytest.raises(ScientificContractError,match="capital/partial cost"):
        validate_exchange(d)


def test_no_external_plant_validation_from_modelled_hydrogen():
    d=example(E)
    d["claims"]["industrial_validation"]=True
    with pytest.raises(ScientificContractError,match="modelled"):
        validate_exchange(d)


def test_full_hydrogen_service_without_service_profile_prohibited():
    d=example(E)
    d["claims"]["matched_service_comparison_eligible"]=True
    with pytest.raises(ScientificContractError,match="unknown storage equipment"):
        validate_exchange(d)


def test_methanol_requires_actual_CO2_input_and_product_gate():
    d=example(E)
    d["scenario_id"]="MeOH_baseline"
    d["research_question"]="CO2_to_methanol"
    d["functional_unit"]["product"]="CH3OH"
    with pytest.raises(ScientificContractError,match="nonzero specified product and CO2 feed"):
        validate_exchange(d)


def test_no_public_comparative_superiority_from_unreviewed_result():
    d=example(E)
    d["claims"]["comparative_superiority_claim"]=True
    with pytest.raises(ScientificContractError,match="comparative environmental superiority"):
        validate_exchange(d)
