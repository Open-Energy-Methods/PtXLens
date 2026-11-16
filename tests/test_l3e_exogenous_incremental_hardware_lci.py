"""L3-E F2-linked Type I 19-line hardware and native BAFU NULL evidence gates.

Uses real original F2 2023 research *reference* Git blob and published
exogenous H30 2022/2024 source cost report, no invented OEM, BOM or GWP.
"""
import json

import pytest

from ptxlens import l3e_exogenous_incremental_hardware_lci as m
from ptxlens.l3d_bafu_incremental_inventory_gate import NativeInventoryBlocked
from ptxlens.l3e_exogenous_incremental_dcf import MatchedStorageDCFError


def test_real_source_BOM_19_lines_and_exogenous_service_source_locked():
    d=m.build()
    assert d["schema_version"]==m.SCHEMA
    rows=d["nineteen_research_equipment_and_evidence_lines"]
    assert len(rows)==19
    assert len({x["line_id"] for x in rows})==19
    assert d["source_F2_2023_bare_vessel_reference_Git_blob"]==\
           m.PINNED_SOURCE_GIT_BLOB_SHA
    assert d["source_2022_2024_independent_same_product_cost_Git_blob"]==\
           m.SOURCE_GIT_BLOB
    assert d["model_hydrogen_functional_unit"].startswith(
        "exact original 30t/day")
    service=d["source_year_hydrogen_normalization"]
    assert [s["source_year_UTC_hours"] for s in service]==[8760,8784]
    assert [s["delivered_H2_kg"] for s in service]==[10950000.,10980000.]


def test_original_802_reference_is_EMPTY_equipment_mass_not_virgin_steel_kg():
    d=m.build()
    assert d["reference_additional_vessel_count_NOT_qualified_site_bank"]==802
    assert d["reference_vessel_mass_kg_EMPTY_EQUIPMENT_NOT_virgin_steel"]==1924800
    vessel=d["nineteen_research_equipment_and_evidence_lines"][0]
    assert vessel["model_reference_802_vessel_count_ONLY_if_line_is_vessel"]==802
    assert vessel["model_reference_empty_equipment_mass_kg_NOT_steel_input"]==1924800
    assert vessel["actual_manufactured_material_input_kg"] is None
    assert vessel["actual_manufacturer_installed_quantity"] is None
    assert vessel["native_BAFU_2026_v11_input_exchange_amount_in_real_reference_unit"] is None


def test_all_unknown_18_other_BoP_lines_remain_NULL_not_zero():
    d=m.build()
    rows=d["nineteen_research_equipment_and_evidence_lines"]
    for line in rows:
        assert line["actual_manufacturer_installed_quantity"] is None
        assert line["actual_manufacturer_equipment_empty_mass_kg"] is None
        assert line["actual_supplier_all_in_initial_cost_eur"] is None
        assert line["actual_incremental_yearly_maintenance_OPEX_eur"] is None
        assert line["actual_replacement_years_and_manufacturing_quantities"] is None
        assert line["actual_manufactured_material_input_kg"] is None
        assert line["actual_site_installed_equipment_mass_kg"] is None
        assert line["native_BAFU_2026_v11_actual_process_UUID"] is None
        assert line["native_BAFU_2026_v11_technosphere_exchange_provider_UUID"] is None
        assert line["native_BAFU_2026_v11_LCIA_GWP_kgCO2e_incremental_manufacturing"] is None
        assert line["native_LCIA_computed_and_replayed"] is False
        assert line["zero_unknown_material_or_cost_or_LCIA_assumed"] is False
    assert all(r["model_reference_empty_equipment_mass_kg_NOT_steel_input"] is None
               for r in rows[1:])


def test_annual_manufacturing_and_replacement_impact_must_remain_unknown():
    d=m.build()
    assert d["actual_manufacturer_total_incremental_material_input_kg"] is None
    assert d["native_manufacturing_plus_replacement_plus_EOL_total_kgCO2e"] is None
    assert d["native_matched_2022_annual_H2_lifecycle_GWP_delta_kgCO2e_per_kg"] is None
    assert d["native_matched_2024_annual_H2_lifecycle_GWP_delta_kgCO2e_per_kg"] is None
    assert d["scientific_v1_0_environmental_release_allowed"] is False


def test_attempt_to_promote_filled_declarative_foreground_to_native_lcia_is_refused():
    d=m.build()
    with pytest.raises(NativeInventoryBlocked,match="not implemented"):
        m.native_LCIA_release_check(d)
    with pytest.raises(MatchedStorageDCFError):
        m.native_LCIA_release_check({"schema_version":"other"})


def test_public_source_only_scope_markdown_has_explicit_unknowns_and_valid_lines():
    d=m.build()
    out=m.markdown(d)
    assert out.count("UNKNOWN")>=19
    assert "EMPTY EQUIPMENT" in out
    assert "NOT" in out
    assert "20-200" in out
    assert "native" in out.lower()
    assert "typeI_200bar_bare_reference_vessels" in out
    assert "inspections_fatigue_cycle_testing" in out
    assert "decommission_and_EOL" in out
