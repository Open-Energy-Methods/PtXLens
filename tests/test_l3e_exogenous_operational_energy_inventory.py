"""L3-E original annual energy inventory vs CO2 inference safety tests.

Real test fixtures are the PUBLIC already independently verified E20t/E+S40t
2022/2024 original-model full-year integer-replay scalar JSON records;
never read private provider-hourly prices/wind or original solver witnesses.
"""
import json

import pytest

from ptxlens import l3e_exogenous_operational_energy_inventory as m


def test_source_verified_both_years_annual_operational_energy_inventory():
    d=m.build()
    rows=d["yearly"]
    assert [r["source_year"] for r in rows]==[2022,2024]
    assert rows[0]["annual_matched_delivered_H2_kg"]==10950000.
    assert rows[1]["annual_matched_delivered_H2_kg"]==10980000.
    assert d["compressor_MWh_is_electrical_load_SUBSET_NOT_added_to_grid_consumption"]
    for row in rows:
        assert row["source_year_UTC_hours"] in (8760,8784)
        assert row["grid_energy_delta_implies_CO2e_sign"] is None
        assert row["environmental_superiority_certified"] is False
        assert row["native_BAFU_v11_foreground_manufacturing_plus_replacements_GWP_kgCO2e"] is None
        assert set(row["cases"])=={"E","E_plus_S"}


def test_2022_more_NET_energy_despite_2022_model_wholesale_saving():
    r=m.build()["yearly"][0]
    assert r["EplusS_MINUS_E_delta_import_MWh"]==pytest.approx(-8244.812981100084)
    assert r["EplusS_MINUS_E_delta_export_MWh"]==pytest.approx(-9144.901379136776)
    assert r["EplusS_MINUS_E_delta_net_grid_import_MWh"]==pytest.approx(
        900.0883980366925)
    assert r["EplusS_MINUS_E_delta_compressor_MWh_ALREADY_INCLUDED_in_system_load"]==pytest.approx(
        432.6413695898382)
    assert r["EplusS_MINUS_E_delta_net_grid_import_kWh_per_kg_delivered_H2"]>0
    assert r["modelled_year_specific_wholesale_E_MINUS_ES_saving_EUR"]>0


def test_2024_lower_NET_energy_and_higher_compressor_MWh():
    r=m.build()["yearly"][1]
    assert r["EplusS_MINUS_E_delta_import_MWh"]==pytest.approx(-11659.94802281793)
    assert r["EplusS_MINUS_E_delta_export_MWh"]==pytest.approx(-10779.189715810862)
    assert r["EplusS_MINUS_E_delta_net_grid_import_MWh"]==pytest.approx(
        -880.7583070070687)
    assert r["EplusS_MINUS_E_delta_compressor_MWh_ALREADY_INCLUDED_in_system_load"]==pytest.approx(
        576.5523077855414)
    assert r["EplusS_MINUS_E_delta_net_grid_import_kWh_per_kg_delivered_H2"]<0
    assert r["modelled_year_specific_wholesale_E_MINUS_ES_saving_EUR"]>0


def test_compressor_subset_is_not_counted_as_extra_purchase():
    for row in m.build()["yearly"]:
        for case in row["cases"].values():
            assert case["modelled_annual_grid_import_MWh"]>=0
            assert case["modelled_annual_grid_export_MWh"]>=0
            assert case["modelled_annual_compressor_electricity_MWh_WITHIN_system_load"]>0
            assert case["modelled_annual_signed_NET_grid_import_MWh"]==pytest.approx(
                case["modelled_annual_grid_import_MWh"]-
                case["modelled_annual_grid_export_MWh"])
            assert case["modelled_annual_signed_net_import_kWh_per_kg_H2"]==pytest.approx(
                1000*case["modelled_annual_signed_NET_grid_import_MWh"]/
                row["annual_matched_delivered_H2_kg"])


def test_source_year_public_replay_integrity_blocks_changed_energy(tmp_path,monkeypatch):
    original=m.source_file(2022)
    d=json.loads(original.read_text(encoding="utf-8"))
    d["case_results"]["E"]["independent_annual_grid_import_MWh"]+=50.
    changed=tmp_path/"tampered_2022_source.json"
    changed.write_text(json.dumps(d),encoding="utf-8")
    genuine=m.source_file
    monkeypatch.setattr(m,"source_file",lambda year:
                        changed if year==2022 else genuine(year))
    with pytest.raises(m.MatchedStorageDCFError,match="Git blob"):
        m.build()


def test_no_fabricated_GWP_from_2022_energy_or_wholesale_money():
    r=m.build()
    assert r["lifecycle_incremental_kgCO2e_per_kg_delivered_H2"] is None
    assert r["missing_hourly_time_matched_energy_grid_emission_factors"] is True
    assert r["missing_complete_native_BAFU_v11_manufacturing_BoP_replacements_EOL"] is True
    assert r["claim_of_environmentally_superior_storage_allowed"] is False
    assert "NOT LCIA" in m.markdown(r)
    assert "NEVER" not in m.markdown(r) or "CO2e" in m.markdown(r)
