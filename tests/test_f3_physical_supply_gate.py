"""Source-hash controlled prospective physical H2 route, with negative LCIA gates."""
import json
import pytest

from ptxlens.f3_physical_supply_gate import (
    PATH,REGISTERED_SHA256,IneligibleH2PhysicalSupply,
    verify_prospective_design_basis,native_lca_tea_admissibility,
)


def test_actual_2023_modelled_h2_vs_2026_network_temporal_gate():
    d=verify_prospective_design_basis()
    assert d["reference_weather_and_wholesale_price_year"]==2023
    assert d["external_network_architecture_source_year"]==2026
    assert d["prospective_2026_infrastructure_is_not_observed_2023_site_supply"]
    for mode,r in d["modes"].items():
        pipe=r["pathways"]["contracted_dedicated_H2_pipeline"]
        assert pipe["customer_guaranteed_min_exit_pressure_bar_absolute"] is None
        assert pipe["the_30barg_value_is_not_site_customer_exit_pressure"]
        assert not r["environmental_and_tea_comparison_eligible"]


def test_bafu_source_provider_and_full_dcf_are_not_zero_from_missing_physical_supply():
    g=native_lca_tea_admissibility()
    assert g["native_BAFU_2026_v11_full_system_matched_service_GWP"] is None
    assert g["full_system_discounted_EUR2023_LCOH"] is None
    assert not g["comparative_environmental_or_tea_result_allowed"]
    assert REGISTERED_SHA256=="dbb42012e9a4375adc703aa336a66cfc83994f3b2ab15a7a9b98aa9b94596ce3"


@pytest.mark.parametrize("change",[
  lambda d:d.update(reference_weather_and_wholesale_price_year=2026),
  lambda d:d.update(physically_verified_common_hourly_service=True),
  lambda d:d.update(backup_LCA_process_inventory_available=True),
  lambda d:d["modes"]["max_inventory"]["pathways"]["contracted_dedicated_H2_pipeline"].update(customer_guaranteed_min_exit_pressure_bar_absolute=31.01325),
  lambda d:d["modes"]["usable_service"]["pathways"]["gaseous_tube_trailer_delivery"].update(actual_deliverable_peak_flow_kg_h=190),
  lambda d:d["modes"]["max_inventory"].update(environmental_and_tea_comparison_eligible=True),
])
def test_tampered_site_supply_or_2023_causality_is_rejected(tmp_path,change):
    x=json.loads(PATH.read_text())
    change(x)
    p=tmp_path/"candidate_fake.json";p.write_text(json.dumps(x))
    with pytest.raises(IneligibleH2PhysicalSupply,match="unsigned/changed"):
        verify_prospective_design_basis(p)
