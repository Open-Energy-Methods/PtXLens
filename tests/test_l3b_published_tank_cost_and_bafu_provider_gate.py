"""L3-B source-referenced 2024 nominal 200bar(g) tank-only IJHE cost vs
2023 real EUR DCF and native BAFU v1.1 30bar PEM-only stop.
Neither supplier quote, installed BoP, nor source 2023 matched hour full GWP.
"""
import json
import pytest
import ptxlens.l3b_published_tank_cost_and_bafu_provider_gate as m


def test_source_paper_nominal_200bar_gauge_2024_eur_and_2023_price_year_not_interchangeable():
    meta,f2,l3,bafu=m.load_source()
    source=meta["original_reference"]
    assert source["source_pressure_basis"].startswith("200bar GAUGE")
    assert source["source_nominal_tank_capacity_h2_kg_per_vessel"]==26
    assert source["specific_cost_eur_per_kg_h2_rated_nominal"]==222
    assert source["reported_empty_vessel_kg"]==2400
    assert source["harmonized_cost_price_year"]==2024
    assert source["actual_supplier_quoted_price_eur"] is None
    assert not source["actual_vendor_nominal_200bar_absolute_313K_validated"]
    assert meta["cost_interpretation"]["price_2024_to_real_2023_currency_year_conversion_factor"] is None
    assert meta["cost_interpretation"]["direct_comparison_of_2024_paper_cost_with_2023_discount_ceiling_without_deflator_forbidden"]
    assert l3["true_project_incremental_NPV_eur"] is None


@pytest.mark.parametrize("mode,count,kg,euro_2024",[
    ("max_inventory",802,1924800,4629144),
    ("usable_service",902,2164800,5206344),
])
def test_discrete_nominal_reference_vessel_tank_only_2024_eur_but_not_vendor_PRICE_or_npv(
    mode,count,kg,euro_2024):
    x=m.evaluate_cost_source_boundaries()
    assert x["schema_version"]==m.SCHEMA
    assert x["source_200bar_reference_paper_rating_is_gauge_while_F3_model_is_absolute"] is True
    assert x["source_eur_reference_year"]==2024
    assert x["original_hourly_modelled_economic_source_year"]==2023
    assert x["price_year_conversion_unprovided_and_not_inferred"] is True
    assert not x["actual_full_manufacturer_BOM_quote_and_economic_preference_allowed"]
    a=x["modes"][mode]
    assert a["F2_E20t_to_ES40t_additional_1p8m3_200bar_reference_empty_vessels_count"]==count
    assert a["source_paper_nominal_H2_capacity_kg_on_added_reference_vessels"]==26*count
    assert a["source_paper_nominal_empty_equipment_mass_kg_not_raw_steel"]==kg
    assert a["source_literature_tank_only_2024_EUR"]==euro_2024
    assert a["source_literature_2024_EUR_per_kg_H2_nominal_capacity"]==222
    assert a["source_literature_tank_cost_proven_vendor_quoted_eur"] is None
    assert not a["source_reference_paper_bare_cost_includes_all_18_other_BOP_plant_scope_classes"]
    assert a["installed_source_2024_extra_compressor_and_cooler_and_rack_cost_EUR"] is None
    assert a["real_2024_to_2023_currency_year_factor"] is None
    assert a["manufacturer_actual_all_in_incremental_CAPEX_EUR"] is None
    assert a["manufacturer_actual_annual_OPEX_EUR"] is None
    assert a["2023_true_investment_NPV_and_LCOH_EUR"] is None


def test_real_bafu_v11_native_source_PEM_30bar_exists_but_incompatible_full_storage_GWP():
    x=m.evaluate_cost_source_boundaries()
    assert x["BAFU_2026_v11_native_30bar_PEM_source_archive_sha256"]=="e63b7e7ef5cde04bfe1176a783a55b5f72e2b73f42c36632b6150af39d348c4c"
    assert x["BAFU_v1_vehicle_composite_per_kg_H2_capacity_not_steel_mass_provider_UUID"]==m.V1_COMPOSITE_TANK
    assert x["actual_complete_2023_H2_same_hour_BAFU_v11_GWP_per_kg"] is None
    rows=x["BAFU_native_reference_2023_original_E_and_ES_not_matched_H2_service"]
    assert len(rows)==2
    assert rows[0]["case"]=="E" and rows[1]["case"]=="E_plus_S"
    assert rows[0]["gwp_per_kg_at_30bar_PEM_H2"]==pytest.approx(6.148174395784)
    assert rows[1]["gwp_per_kg_at_30bar_PEM_H2"]==pytest.approx(6.0765526538929)
    assert rows[0]["modelled_annual_H2_kg"]!=rows[1]["modelled_annual_H2_kg"]


@pytest.mark.parametrize("mutate",[
  lambda d:d["original_reference"].update(specific_cost_eur_per_kg_h2_rated_nominal=1.),
  lambda d:d["original_reference"].update(harmonized_cost_price_year=2023),
  lambda d:d["original_reference"].update(actual_supplier_quoted_price_eur=4629144),
  lambda d:d["original_reference"].update(source_pressure_basis="200bar ABSOLUTE"),
  lambda d:d["cost_interpretation"].update(price_2024_to_real_2023_currency_year_conversion_factor=1),
  lambda d:d["native_BAFU_2026_v11_original"].update(native_compatible_F2_typeI_sourced_steel_material_process_uuid="not_source_verified"),
  lambda d:d.update(source_does_not_permit_full_v1_0_release=False),
])
def test_gwp_carbon_source_and_non_quote_assertion_fabrication_rejected(tmp_path,monkeypatch,mutate):
    d=json.loads(m.REGISTER.read_text())
    mutate(d)
    p=tmp_path/"source_manifest.json";p.write_text(json.dumps(d))
    monkeypatch.setattr(m,"REGISTER",p)
    with pytest.raises(m.InvalidSupplierOrLCAQualification):
        m.load_source()


def test_source_tank_per_vessel_2024_eur_is_not_manufacturer_full_CAPEX_2023():
    data=m.evaluate_cost_source_boundaries()
    for mode,row in data["modes"].items():
        assert row["source_literature_tank_only_2024_EUR"]>4e6
        assert row["source_2023_L3_A_20y8pct_ZERO_OPEX_hypothetical_installed_CAPEX_ceiling_EUR2023"]>10e6
        assert row["paper_2024_tank_cost_vs_L3A_2023_breakeven_comparable_without_price_year_and_scope_adjustment"] is False
        assert row["source_only_not_a_vendor_quote_nor_full_LCA"] is True
