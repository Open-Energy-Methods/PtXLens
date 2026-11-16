"""Scientific guardrail tests: never fabricate missing BAFU manufacturing burdens."""
from ptxlens.bafu_real_screen import (
    PROCESSES, ACCEPTED_MATERIAL_BY_SOURCE_DESCRIPTION, UNRESOLVED_STACK_REASONS,
)

def test_BAFU_2026_reference_ids_are_explicit_and_unique():
    ids=[x[0] for x in PROCESSES.values()]
    assert len(ids)==len(set(ids))
    assert "grid_nl_high_voltage" in PROCESSES
    assert PROCESSES["grid_nl_high_voltage"][2]=="NL"
    assert PROCESSES["offshore_wind_legacy_2mw"][1].startswith("xx ")
    assert PROCESSES["hydrogen_pem_30bar_ch"][3]=="kg"
    assert PROCESSES["water_nl_deionized"][2:] == ("NL","kg")

def test_only_technologically_comparable_stack_materials_have_source_mapping():
    assert len(ACCEPTED_MATERIAL_BY_SOURCE_DESCRIPTION)==4
    assert len(UNRESOLVED_STACK_REASONS)==4
    assert "market for titanium" in UNRESOLVED_STACK_REASONS
    assert "activated carbon production, granular from hard coal" in UNRESOLVED_STACK_REASONS
    assert "nafion (sulfonyl fluoride)" in UNRESOLVED_STACK_REASONS
    assert "market for platinum group metal concentrate, Iridium" in UNRESOLVED_STACK_REASONS

def test_real_BAFU_factors_preserve_original_megajoule_unit():
    assert PROCESSES["grid_nl_high_voltage"][3]=="MJ"
    assert PROCESSES["offshore_wind_legacy_2mw"][3]=="MJ"
    assert PROCESSES["aluminium_primary"][3]=="kg"
    assert PROCESSES["platinum"][3]=="kg"
