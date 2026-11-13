"""Unit / identity checks. Empirical LCA CI uses ORIGINAL source ZIP artifacts."""
import pytest
from ptxlens.lca_screen import (
    GRID_OPERATIONAL, GRID_UPSTREAM, GRID_INFRA, WIND_LIFECYCLE, SOURCES, _closed,
)

def test_published_2023_nl_factor_decomposition():
    assert GRID_OPERATIONAL == pytest.approx(.290)
    assert GRID_UPSTREAM == pytest.approx(.047)
    assert GRID_INFRA == pytest.approx(.007)
    assert GRID_OPERATIONAL+GRID_UPSTREAM == pytest.approx(.337)
    assert sum((GRID_OPERATIONAL,GRID_UPSTREAM,GRID_INFRA)) == pytest.approx(.344)
    assert SOURCES["grid_2023"]["year"] == 2023

def test_published_unece_offshore_wind_factor():
    assert WIND_LIFECYCLE == pytest.approx(.0142)
    assert "unece.org" in SOURCES["wind_offshore"]["url"]

def test_identity_checks_reject_energy_mismatch():
    _closed(125.0,125.0,"energy")
    with pytest.raises(ValueError,match="identity"):
        _closed(125.0,125.01,"energy")

def test_gwp_physical_units():
    # 1 MWh electricity * 1000 kWh/MWh * .337 kgCO2e/kWh
    assert 1000*(GRID_OPERATIONAL+GRID_UPSTREAM) == pytest.approx(337)
    assert 1000*WIND_LIFECYCLE == pytest.approx(14.2)
