"""Source-contract tests. Constructed arrays below test parsing only, not research."""
import copy
import hashlib
import io
import json
import math
from datetime import datetime,timedelta,timezone
import zipfile

import pytest

from ptxlens.doe import assess_doe_capital_component
from ptxlens.energy_charts import parse_price_response,build_url
from ptxlens.observed import KNOWN_SHA256,load_archive,compare_archives
from ptxlens.olca_real import validate_openlca_contract,per_kg_electricity_from_verified_observed

OBSERVED_E = {
    "schema_version":"ptxlens.pynexus_wp5_observed.v0.1",
    "scenario":"E",
    "archive_sha256":KNOWN_SHA256["E"],
    "annual_delivered_h2_kg":16335279.317376737,
    "annual_electrolyser_input_mwh":774961.3661277184,
    "annual_produced_h2_kg":16340919.535390353,
    "annual_grid_import_mwh":300591.2538625492,
    "annual_wind_consumed_mwh":474370.11226516915,
    "annual_net_wholesale_settlement_eur":25748968.928416785,
    "electrolyser_capacity_mw":125,
    "online_hours":8722,
}
OBSERVED_ES = dict(OBSERVED_E,
    scenario="E+S", archive_sha256=KNOWN_SHA256["E+S"],
    annual_delivered_h2_kg=16679072.08788669,
    annual_electrolyser_input_mwh=791525.0706026762,
    annual_produced_h2_kg=16690183.60694752,
    annual_grid_import_mwh=302644.15636347805,
    annual_wind_consumed_mwh=488880.9142391982,
    annual_net_wholesale_settlement_eur=27508060.360551164,
    online_hours=8708)

def test_observed_primary_source_checksums_are_recorded():
    assert len(KNOWN_SHA256)==2
    for k,v in KNOWN_SHA256.items():
        assert len(v)==64 and all(c in "0123456789abcdef" for c in v)

def test_doe_primary_source_capex_and_currency_gate():
    d=assess_doe_capital_component(OBSERVED_E, installed_cost_usd2022_kw=2000,
                                   real_discount_rate=.08)
    assert d["initial_installed_capex_usd2022"] == 250000000
    assert d["capital_price_year"] == 2022 and d["currency"] == "USD"
    assert d["replacement_times_years"][0] == pytest.approx(40000/8722)
    assert len(d["replacement_times_years"]) == 6
    assert d["capital_component_usd2022_per_kg_delivered_h2"] == pytest.approx(1.6702374359,abs=1e-7)
    assert d["separate_wholesale_electricity_eur2023_per_kg_delivered_h2"] == pytest.approx(1.5762796845,abs=1e-7)
    assert d["pynexus_modelled_kwh_per_kg_produced"] < d["doe_reference_system_kwh_per_kg"]

def test_doe_real_e_and_es_comparison_is_not_matched_service():
    a=assess_doe_capital_component(OBSERVED_E, installed_cost_usd2022_kw=2000,real_discount_rate=.08)
    b=assess_doe_capital_component(OBSERVED_ES, installed_cost_usd2022_kw=2000,real_discount_rate=.08)
    assert b["capital_component_usd2022_per_kg_delivered_h2"] < a["capital_component_usd2022_per_kg_delivered_h2"]
    assert b["separate_wholesale_electricity_eur2023_per_kg_delivered_h2"] > a["separate_wholesale_electricity_eur2023_per_kg_delivered_h2"]

def test_doe_requires_sourced_capex_case_and_explicit_rate():
    with pytest.raises(ValueError):
        assess_doe_capital_component(OBSERVED_E,installed_cost_usd2022_kw=800,real_discount_rate=.08)
    with pytest.raises(ValueError):
        assess_doe_capital_component(OBSERVED_E,installed_cost_usd2022_kw=2000,real_discount_rate=float("nan"))

def test_market_price_url_enforces_nl():
    assert "bzn=NL" in build_url(2023)
    with pytest.raises(ValueError):
        build_url(2023,"FI")  # licence class not established for FI

def test_market_api_parser_requires_full_year_no_gaps():
    start=datetime(2023,1,1,tzinfo=timezone.utc)
    timestamps=[int((start+timedelta(hours=i)).timestamp()) for i in range(8760)]
    raw={"unix_seconds":timestamps,"price":[float(i%37) for i in range(8760)],
         "unit":"EUR/MWh","license_info":"NL CC BY 4.0"}
    out=parse_price_response(raw,2023,raw_sha256="test",request_url="test")
    assert out["row_count"]==8760
    assert out["series"][0]["timestamp_utc"]=="2023-01-01T00:00:00Z"
    assert out["series"][-1]["timestamp_utc"]=="2023-12-31T23:00:00Z"
    raw["unix_seconds"].pop(10)
    raw["price"].pop(10)
    with pytest.raises(ValueError,match="coverage"):
        parse_price_response(raw,2023)

def test_market_api_rejects_duplicate_and_nonfinite():
    start=datetime(2023,1,1,tzinfo=timezone.utc)
    base={"unix_seconds":[int((start+timedelta(hours=i)).timestamp()) for i in range(8760)],
          "price":[30.0]*8760,"unit":"EUR/MWh","license_info":"NL CC BY 4.0"}
    bad=copy.deepcopy(base);bad["unix_seconds"][1]=bad["unix_seconds"][0]
    with pytest.raises(ValueError,match="repeated"):
        parse_price_response(bad,2023)
    bad=copy.deepcopy(base);bad["price"][1]=None
    with pytest.raises(ValueError,match="missing/nonfinite"):
        parse_price_response(bad,2023)

def test_openlca_dispatch_normalization_is_real_observed_electricity():
    kwh=per_kg_electricity_from_verified_observed(OBSERVED_E)
    assert kwh["electricity_grid_kwh_per_kg"]==pytest.approx(18.4013,rel=.001)
    assert sum(kwh.values())==pytest.approx(1000*774961.3661277184/16335279.317376737)

def test_openlca_must_have_real_model_and_database_contract():
    cfg={"product_system_id":"p","product_system_name":"PEM hydrogen",
         "impact_method_id":"m","impact_method_name":"EF Climate change",
         "database_name":"open process LCI","database_version":"v1",
         "database_license":"source dependent","database_provider":"documented",
         "reference_flow_amount_kg_h2":1,
         "parameter_mapping":{"electricity_grid_kwh_per_kg":"grid_elec_kwh",
                              "electricity_wind_kwh_per_kg":"wind_elec_kwh"}}
    assert validate_openlca_contract(cfg) is cfg
    del cfg["impact_method_id"]
    with pytest.raises(ValueError):
        validate_openlca_contract(cfg)

def test_audit_rejects_unknown_archive(tmp_path):
    bogus=tmp_path/"bogus.zip"
    with zipfile.ZipFile(bogus,"w") as archive:
        archive.writestr("manifest.json",json.dumps({"full_year":True,"hours":8760,
            "cost_claim":"NONE_GRID_SETTLEMENT_ONLY",
            "price_kind":"PROCESSED_ENTSOE_2023_NL_DAY_AHEAD_NOT_INVOICE"}))
        archive.writestr("E/record.json","{}")
    with pytest.raises(ValueError,match="archive bytes"):
        load_archive(bogus)
