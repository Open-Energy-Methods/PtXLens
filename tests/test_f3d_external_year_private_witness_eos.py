"""Independent PtXLens CoolProp hydrogen pressure checks, synthetic-only.

No original provider XML, ERA5 or site operation data in the fixture.
"""
import copy
import pytest

pytest.importorskip("CoolProp")
from ptxlens.f3d_external_year_private_witness_replay import (
    ExternalYearReviewError,verify_eos,
)


def bank(semantics):
    return {
        "vessel_id":"I_200bar",
        "capacity_semantics":semantics,
        "gas_minimum_absolute_bar":20.0,
        "gas_maximum_absolute_bar":200.0,
        "temperature_k":313.0,
        "source_PEM_outlet_absolute_bar":30.0,
        "compressor_eta_isentropic":0.8,
        "motor_eta":0.9,
        "compressor_stages":2,
        "includes_cooling_electricity":False,
        "includes_vessel_material_fabrication_lca":False,
        "bank_free_volume_m3":1500.0,
        "gas_heel_kg":1000.0,
    }


@pytest.mark.parametrize("semantics",("max_inventory","usable_service"))
def test_independent_313k_hydrogen_EOS_both_inventory_interpretations(semantics):
    duty=bank(semantics)
    z=verify_eos(duty,9000.0,11000.0)
    assert z["min_bar_absolute"]>=20.
    assert z["max_bar_absolute"]<=200.
    assert z["independent_313K_CoolProp_Hydrogen_EOS_recomputed"] is True
    assert z["matched_original_screened_solver_extrema"] is False
    p={
        "real_gas_minimum_dispatched_pressure_bar_absolute":z["min_bar_absolute"],
        "real_gas_maximum_dispatched_pressure_bar_absolute":z["max_bar_absolute"]
    }
    assert verify_eos(duty,9000.,11000.,p)["matched_original_screened_solver_extrema"] is True
    p["real_gas_minimum_dispatched_pressure_bar_absolute"]+=1.
    with pytest.raises(ExternalYearReviewError,match="extrema differ"):
        verify_eos(duty,9000.,11000.,p)


def test_independent_source_pressure_does_not_approve_bad_temperature_or_vessel():
    d=bank("max_inventory")
    d["temperature_k"]=298.15
    with pytest.raises(ExternalYearReviewError,match="pressure and compressor"):
        verify_eos(d,9000.,11000.)
    d=bank("max_inventory")
    d["vessel_id"]="IV_350bar"
    with pytest.raises(ExternalYearReviewError,match="pressure and compressor"):
        verify_eos(d,9000.,11000.)
