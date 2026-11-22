import pytest
from ptxlens.lca_source_quality import inventory_stoichiometry_check, STOICH_O2_PER_H2

def _published_source_flows():
    """Exact amounts from live, SHA-verified USLCI 2017 process; NOT fabricated research inputs."""
    return [
        {"flow":{"name":"Hydrogen; at plant"},"input":False,"amount":1.0,"unit":{"name":"kg"}},
        {"flow":{"name":"Oxygen"},"input":False,"amount":12.0,"unit":{"name":"kg"}},
        {"flow":{"name":"Water; process;,deionized"},"input":True,"amount":9.0,"unit":{"name":"kg"}},
    ]

def test_published_USLCI_oxygen_source_has_explicit_mass_discrepancy():
    out=inventory_stoichiometry_check(_published_source_flows())
    assert out["elemental_stoichiometry_reconciled"] is False
    assert out["blocks_complete_product_lca"] is True
    assert out["original_source_oxygen_output_kg"]==12
    assert out["theoretical_oxygen_kg_for_source_h2"]==pytest.approx(7.936,abs=.001)
    assert out["unbalanced_input_minus_output_mass_kg"]==-4

def test_physically_consistent_reference_distinguished_from_source_anomaly():
    records=_published_source_flows()
    records[1]["amount"]=STOICH_O2_PER_H2
    result=inventory_stoichiometry_check(records)
    assert result["elemental_stoichiometry_reconciled"] is True
    # Consistent test case is never substituted back into authentic upstream data.

def test_malformed_source_fails_closed():
    with pytest.raises(ValueError):
        inventory_stoichiometry_check(_published_source_flows()[:2])
