"""Independent PtXLens physics replay tests (synthetic mathematics, not ERA5).

Actual original provider/witness playback requires private downloaded files.
"""
import copy
import csv
from datetime import datetime,timedelta,timezone

import pytest

from ptxlens.f3d_external_year_private_witness_replay import (
    ExternalYearReviewError,expected_params,read_private_year_csv,
    replay_equations,f64_hash,
)


def synthetic_feasible_fixture():
    p=expected_params(20000)
    target=[2000.]*3
    yield_kg=p["h2_coefficient_kg_mwh"]
    wind=[]
    states=[]
    for i in range(3):
        P=(target[i]+1.)/yield_kg
        wind.append(P)
        states.append([P,1.,0.,0.,10000.,1.,0.,1.])
    prices=[-20.,10.,50.]
    return states,target,wind,prices,p


def test_independent_mass_grid_bank_and_binary_primal_replay_matches_analytical():
    states,target,wind,price,p=synthetic_feasible_fixture()
    out=replay_equations(states,target,wind,price,p)
    assert out["modelled_annual_hydrogen_kg"]==pytest.approx(6000.)
    assert out["independent_source_year_signed_grid_cost_eur"]==0.
    assert out["minimum_source_bank_model_kg"]==10000.
    assert out["hourly_service_sha256"]==f64_hash(target)
    assert out["hourly_states_sha256"]==f64_hash(z for x in states for z in x)
    assert max(out["maxima"].values())<1e-8


def test_compressor_electrical_charge_duty_is_independently_recomputed():
    states,target,wind,prices,p=synthetic_feasible_fixture()
    # 2kWh/kg compression adds 0.002MW per kg/h of charging.
    duty={"compressor_electrical_kwh_per_kg_charged":2.0,
          "gas_heel_kg":0.,
          "capacity_semantics":"usable_service"}
    wind=[v+.002 for v in wind]
    result=replay_equations(states,target,wind,prices,p,duty)
    assert result["independent_annual_compressor_electricity_mwh"]==pytest.approx(.006,abs=1e-10)
    assert max(result["maxima"].values())<1e-8


@pytest.mark.parametrize("edit",[
    lambda x:x[0].__setitem__(0,x[0][0]+1.),
    lambda x:x[0].__setitem__(1,0.),
    lambda x:x[0].__setitem__(3,2.),
    lambda x:x[0].__setitem__(4,9000.),
    lambda x:x[0].__setitem__(6,2.),
    lambda x:x[0].__setitem__(7,0.),
])
def test_independent_audit_rejects_changed_dispatch_component(edit):
    states,target,wind,price,p=synthetic_feasible_fixture()
    edit(states)
    with pytest.raises(ExternalYearReviewError,match="primal residual"):
        replay_equations(states,target,wind,price,p)


def test_source_year_float_digest_is_little_endian_and_nan_fails():
    assert len(f64_hash([0.,1.,-1.]))==64
    with pytest.raises(ExternalYearReviewError,match="float64"):
        f64_hash([float("nan")])


def test_2024_leap_calendar_cannot_be_truncated_or_modified(tmp_path):
    n=8784
    f=tmp_path/"synthetic_price_calendar.csv"
    first=datetime(2024,1,1,tzinfo=timezone.utc)
    with f.open("w",encoding="utf-8",newline="") as handle:
        writer=csv.writer(handle)
        writer.writerow(["timestamp_utc","day_ahead_eur_mwh"])
        for i in range(n):
            writer.writerow([(first+timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ"),"-2" if i==0 else "10"])
    out=read_private_year_csv(f,2024,"day_ahead_eur_mwh")
    assert len(out)==8784 and out[0]==-2.
    with f.open("w",encoding="utf-8",newline="") as handle:
        writer=csv.writer(handle)
        writer.writerow(["timestamp_utc","day_ahead_eur_mwh"])
        for i in range(8760):
            writer.writerow([(first+timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ"),"10"])
    with pytest.raises(ExternalYearReviewError,match="missing source 2024 leap"):
        read_private_year_csv(f,2024,"day_ahead_eur_mwh")
