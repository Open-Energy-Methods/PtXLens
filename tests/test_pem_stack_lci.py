"""Published PEM stack LCI source integrity tests, not unreported factor assumptions."""
from pathlib import Path
import pytest
from ptxlens.pem_stack_lci import inventory_reference

ROOT=Path(__file__).resolve().parents[1]
LCI=ROOT/"data/lci/pem_stack_kanz_2024_1mw.json"


def test_published_tue_stack_inventory_has_8_nonzero_real_materials():
    x=inventory_reference(LCI)
    materials={item["name"]:item["kg_per_1mw_stack"] for item in x["materials"]}
    assert len(materials)==8
    assert materials["titanium"]==528
    assert materials["aluminium primary"]==27
    assert materials["stainless steel 18/8"]==100
    assert materials["copper"]==4.5
    assert materials["nafion membrane precursor proxy"]==16
    assert materials["activated carbon"]==9
    assert materials["iridium in PGM concentrate"]==.75
    assert materials["platinum"]==.075
    assert "20240626_Kanz_hf.pdf" in x["source"]["url"]


def test_no_impact_factor_implied_by_material_mass():
    x=inventory_reference(LCI)
    assert "GaBi" in x["blockers"][0]
    assert all("provider_lci_name" in i and "kgco2e" not in i for i in x["materials"])
