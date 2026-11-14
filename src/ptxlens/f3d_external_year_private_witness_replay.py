"""PtXLens independent source-year hourly witness replay (PRIVATE DATA ONLY).

Independently reconstructs H2 mass, electrical balance, storage accumulation,
integer/dispatch bounds, actual price-vector grid settlement and Type-I 313 K
screened bank-pressure extrema from PtXFlex's private solver witness. No
PtXFlex optimization or physics code is imported here.

Only sanitized aggregate residuals/hashes may be exported from this module.
Real-gas pressure checks require CoolProp. Does NOT independently solve the
underlying optimization or verify HiGHS dual certificates.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
from pathlib import Path
import struct

from .f3d_external_year_independent_review import (
    check_result,ExternalYearReviewError,YEAR_HOURS,
)

SCHEMA="ptxflex.f3d_PRIVATE_original_source_dispatch_witness.v1"
REVIEW_SCHEMA="ptxlens.f3d_PRIVATE_primal_hourly_mass_energy_cost_and_EOS_replay.v1"

BASE={
    "initial_kg":10000.,"terminal_kg":10000.,
    "charge_max_kg_h":2200.,"discharge_max_kg_h":2200.,
    "loss_fraction_per_hour":0.0001,
    "rated_mw":125.,"min_load_fraction":0.1,"max_load_fraction":1.,
    "ramp_mw_h":50.,"grid_max_mw":50.,
    "h2_coefficient_kg_mwh":21.086108610861086,
    "delivery_limit_kg_h":7200.,
    "source_bafu_PEM_pressure_bar":30.,
    "source_pipeline_min_delivery_pressure_bar":20.,
}


def need(cond,why):
    if not cond: raise ExternalYearReviewError("PtXLens PRIVATE physical witness: "+why)


def f64_hash(values):
    sha=hashlib.sha256()
    for raw in values:
        need(type(raw) in (int,float) and math.isfinite(raw),"invalid float64 witness input")
        sha.update(struct.pack("<d",float(raw)))
    return sha.hexdigest()


def read_private_year_csv(path,year,column,*,nonnegative=False):
    need(year in YEAR_HOURS,"unknown historical year")
    data=[]
    expected=datetime(year,1,1,tzinfo=timezone.utc)
    with Path(path).open("r",encoding="utf-8-sig",newline="") as file:
        rows=csv.DictReader(file)
        need(rows.fieldnames==["timestamp_utc",column],"private provider source columns changed")
        for hour,row in enumerate(rows):
            need(hour<YEAR_HOURS[year],"source year has excess UTC hours")
            instant=(expected+timedelta(hours=hour)).strftime("%Y-%m-%dT%H:%M:%SZ")
            need(row["timestamp_utc"]==instant,"provider source UTC chronology gap/duplicate")
            val=float(row[column])
            need(math.isfinite(val) and (not nonnegative or val>=0),
                 "provider source has missing/nonfinite value")
            data.append(val)
    need(len(data)==YEAR_HOURS[year],"missing source 2024 leap or 2022 UTC hour")
    return data


def expected_params(capacity_kg):
    need(capacity_kg in (20000,40000),"wrong original E or E+S capacity")
    return {**BASE,"capacity_kg":float(capacity_kg)}


def replay_equations(states,target,wind,price,p,duty=None):
    """Independent hourly primal conservation verifier; low-level testable.

    Full-year source, clock and EOS are enforced separately by
    review_private_witness. All residuals recomputed without trusting a
    PtXFlex solver-derived summary.
    """
    n=len(target)
    need(n>=2 and len(states)==len(wind)==len(price)==n,"witness hourly dimensions differ")
    need(set(p)==set(expected_params(p["capacity_kg"])) and
         all(p[k]==v for k,v in expected_params(p["capacity_kg"]).items()),
         "source 2023 plant physical parameters changed")
    cap=p["capacity_kg"]
    loss=p["loss_fraction_per_hour"]
    y=p["h2_coefficient_kg_mwh"]
    pmax=p["rated_mw"]*p["max_load_fraction"]
    pmin=p["rated_mw"]*p["min_load_fraction"]
    compressor=(float(duty["compressor_electrical_kwh_per_kg_charged"])/1000. if duty else 0.)
    heel=float(duty["gas_heel_kg"]) if duty else 0.
    semantics=duty["capacity_semantics"] if duty else "none"
    need(semantics in ("none","max_inventory","usable_service"),"unknown source 200 bar bank definition")
    min_stock=heel if semantics=="max_inventory" else 0.
    fixed_heel_leak=heel*loss if semantics=="usable_service" else 0.
    prev_storage=p["initial_kg"]
    prev_power=None
    maxima={key:0. for key in (
        "electric_MW","hydrogen_kg_h","inventory_kg","unit_minload_MW",
        "unit_maxload_MW","ramp_MW_h","terminal_storage_kg",
        "wind_curtailment_MW","signed_grid_limit_MW",
        "charge_discharge_exclusivity_kg_h","stock_capacity_kg",
        "binary_unit_and_direction")}
    objective=0.
    total_h2=0.
    compressor_mwh=0.
    grid_import=grid_export=0.
    minimum_stock=float("inf")
    maximum_stock=float("-inf")
    for t,(v,q,w,pr) in enumerate(zip(states,target,wind,price)):
        need(isinstance(v,list) and len(v)==8 and
             all(type(z) in (int,float) and math.isfinite(z) for z in v),
             "missing or invalid 8-column private hourly primal vector")
        P,U,G,C,S,CH,DIS,Z=(float(z) for z in v)
        need(all(math.isfinite(float(z)) for z in (q,w,pr)) and q>=0 and w>=0,
             "invalid original source hourly service/price/wind")
        total_h2+=q
        objective+=G*pr
        compressor_mwh+=CH*compressor
        grid_import+=max(G,0.)
        grid_export+=max(-G,0.)
        maxima["electric_MW"]=max(maxima["electric_MW"],abs(w+G-P-CH*compressor-C))
        maxima["hydrogen_kg_h"]=max(maxima["hydrogen_kg_h"],abs(y*P-CH+DIS-q))
        maxima["inventory_kg"]=max(maxima["inventory_kg"],
            abs(S-(1-loss)*prev_storage-CH+DIS+fixed_heel_leak))
        maxima["unit_minload_MW"]=max(maxima["unit_minload_MW"],max(0.,pmin*U-P))
        maxima["unit_maxload_MW"]=max(maxima["unit_maxload_MW"],max(0.,P-pmax*U))
        if prev_power is not None:
            maxima["ramp_MW_h"]=max(maxima["ramp_MW_h"],max(0.,abs(P-prev_power)-p["ramp_mw_h"]))
        maxima["wind_curtailment_MW"]=max(maxima["wind_curtailment_MW"],max(0.,-C,C-w))
        maxima["signed_grid_limit_MW"]=max(maxima["signed_grid_limit_MW"],
            max(0.,abs(G)-p["grid_max_mw"]))
        maxima["charge_discharge_exclusivity_kg_h"]=max(
            maxima["charge_discharge_exclusivity_kg_h"],
            max(0.,-CH,CH-p["charge_max_kg_h"]*Z,
                -DIS,DIS-p["discharge_max_kg_h"]*(1-Z)))
        maxima["stock_capacity_kg"]=max(maxima["stock_capacity_kg"],
            max(0.,min_stock-S,S-cap))
        maxima["binary_unit_and_direction"]=max(maxima["binary_unit_and_direction"],
            abs(U-round(U)),abs(Z-round(Z)),max(0.,-U,U-1,-Z,Z-1))
        need(P>=-2e-4,"negative source PEM power")
        minimum_stock=min(minimum_stock,S)
        maximum_stock=max(maximum_stock,S)
        prev_storage=S
        prev_power=P
    maxima["terminal_storage_kg"]=abs(prev_storage-p["terminal_kg"])
    need(max(maxima.values())<=2e-4,
         "independent mass/electricity/inventory/unit/pressure-envelope primal residual exceeds 2e-4")
    return {
        "hourly_states_sha256":f64_hash(float(z) for row in states for z in row),
        "hourly_service_sha256":f64_hash(target),
        "hourly_source_wind_sha256":f64_hash(wind),
        "hourly_source_price_sha256":f64_hash(price),
        "modelled_annual_hydrogen_kg":total_h2,
        "independent_source_year_signed_grid_cost_eur":objective,
        "independent_annual_compressor_electricity_mwh":compressor_mwh,
        "independent_grid_import_mwh":grid_import,
        "independent_grid_export_mwh":grid_export,
        "minimum_source_bank_model_kg":minimum_stock,
        "maximum_source_bank_model_kg":maximum_stock,
        "maxima":maxima,
        "year_hour_count":n,
    }


def verify_eos(duty,minimum_stock,maximum_stock,expected_pressure=None):
    """Independent CoolProp 313K H2 density→pressure extremes, no PtXFlex import."""
    try:
        from CoolProp.CoolProp import PropsSI
    except ImportError:
        raise ExternalYearReviewError(
            "CoolProp required to independently verify actual Type I bank pressure EOS") from None
    need(duty["vessel_id"]=="I_200bar" and duty["capacity_semantics"] in (
        "max_inventory","usable_service") and
        duty["gas_minimum_absolute_bar"]==20 and duty["gas_maximum_absolute_bar"]==200 and
        duty["temperature_k"]==313.0 and
        duty["source_PEM_outlet_absolute_bar"]==30.0 and
        duty["compressor_eta_isentropic"]==0.8 and
        duty["motor_eta"]==0.9 and
        duty["compressor_stages"]==2 and
        duty["includes_cooling_electricity"] is False and
        duty["includes_vessel_material_fabrication_lca"] is False,
        "unsupported original Type-I pressure and compressor model")
    heel=duty["gas_heel_kg"] if duty["capacity_semantics"]=="usable_service" else 0.
    volume=float(duty["bank_free_volume_m3"])
    need(volume>0 and minimum_stock+heel>0,"invalid gas volume or storage residual heel")
    def pressure_bar(stock):
        return float(PropsSI("P","Dmass",(stock+heel)/volume,
                             "T",duty["temperature_k"],"Hydrogen"))/100000.
    minimum=pressure_bar(minimum_stock)
    maximum=pressure_bar(maximum_stock)
    need(minimum>=20.-1e-4 and maximum<=200.+1e-4,
         "independent EOS pressure outside 20/200 bar absolute limits")
    if expected_pressure is not None:
        need(isinstance(expected_pressure,dict) and
             abs(expected_pressure["real_gas_minimum_dispatched_pressure_bar_absolute"]-minimum)<=1e-4 and
             abs(expected_pressure["real_gas_maximum_dispatched_pressure_bar_absolute"]-maximum)<=1e-4,
             "source-claimed EOS pressure extrema differ from independent hydrogen PropsSI calculation")
    return {
        "min_bar_absolute":minimum,"max_bar_absolute":maximum,
        "matched_original_screened_solver_extrema":expected_pressure is not None,
        "independent_313K_CoolProp_Hydrogen_EOS_recomputed":True,
    }


def review_private_witness(witness_path,source_report_path,source_price_csv,source_wind_csv):
    """Full private physical primal replay, and independent public summary audit."""
    report=json.loads(Path(source_report_path).read_text(encoding="utf-8"))
    metadata=check_result(report)
    year=metadata["year"]
    mode=metadata["capacity_semantics"]
    witness=json.loads(Path(witness_path).read_text(encoding="utf-8"))
    need(witness.get("schema_version")==SCHEMA and
         witness.get("year")==year and witness.get("capacity_semantics")==mode and
         witness.get("original_E_SHA256")==report["original_source_E_zip_SHA256"] and
         witness.get("original_ES_SHA256")==report["original_source_ES_zip_SHA256"] and
         witness.get("source_year_prices_and_wind_NOT_duplicated_in_witness") is True,
         "private full-year original source witness schema/revision mismatch")
    price=read_private_year_csv(source_price_csv,year,"day_ahead_eur_mwh")
    wind=read_private_year_csv(source_wind_csv,year,"wind_available_mw",nonnegative=True)
    target=witness.get("target_hourly_kg")
    need(isinstance(target,list) and len(target)==YEAR_HOURS[year] and
         all(type(x) in (int,float) and math.isfinite(x) and x>0 for x in target),
         "private original hourly source target missing or invalid")
    psha=f64_hash(price)
    wsha=f64_hash(wind)
    tsha=f64_hash(target)
    need(psha==report["source_year_price_f64_sha256"]==witness["price_float64_sha256"] and
         wsha==report["source_year_wind_f64_sha256"]==witness["wind_float64_sha256"] and
         tsha==report["E_price_blind_identical_model_H2_service_selection"]["selected_h2_target_float64_sha256"]==
         witness["target_float64_sha256"],
         "private calendar/source hourly data cannot be matched by SHA with aggregate report")
    selected=report["E_price_blind_identical_model_H2_service_selection"]
    alpha=selected["selected_fraction_50t_per_day"]
    need(max(abs(x-alpha*50000/24.) for x in target)<1e-10,
         "source H2 customer hours changed from independently reported flat 50t/day fraction")
    cases=witness.get("cases",{})
    need(set(cases)=={"E","E_plus_S"},"original source E/E+S private witnesses missing")
    audited={}
    for name,capacity in (("E",20000),("E_plus_S",40000)):
        case=cases[name]
        expected=expected_params(capacity)
        need(case.get("source_model_parameters")==expected,
             "source original gas/PEM configuration is not unchanged for "+name)
        duty=case.get("Type_I_200bar_model_pressure_duty")
        need(isinstance(duty,dict) and
             duty.get("capacity_semantics")==mode and
             duty.get("scenario_capacity_kg")==capacity,
             "source 20-200bar physical bank scenario mismatch")
        z=replay_equations(case.get("cost_optimum_hourly_states"),target,wind,price,expected,duty)
        public=report[name]
        need(z["hourly_states_sha256"]==public["source_hourly_dispatch_float64_sha256"] and
             abs(z["independent_source_year_signed_grid_cost_eur"]-
                 public["modelled_cost_eur_in_source_calendar_not_inflation_adjusted"])<=0.05 and
             abs(z["modelled_annual_hydrogen_kg"]-
                 public["modelled_annual_hydrogen_kg"])<=0.005 and
             abs(z["independent_annual_compressor_electricity_mwh"]-
                 public["modelled_compressor_electricity_mwh"])<=0.001 and
             abs(z["independent_grid_import_mwh"]-
                 public["modelled_grid_import_mwh"])<=0.001 and
             abs(z["independent_grid_export_mwh"]-
                 public["modelled_grid_export_mwh"])<=0.001,
             name+" original provider-bound hourly witness does not match public financial/physical aggregates")
        z["EOS"]=verify_eos(
            duty,z["minimum_source_bank_model_kg"],z["maximum_source_bank_model_kg"],
            public["pressure_EOS_screen_bounds"])
        audited[name]=z
    selector=replay_equations(
        witness.get("E_price_neutral_alpha_witness_hourly_states"),target,
        wind,[0.]*len(price),expected_params(20000),
        cases["E"]["Type_I_200bar_model_pressure_duty"])
    need(selector["hourly_service_sha256"]==tsha,
         "price-independent E maximal service not physically feasible")
    selection_pressure=verify_eos(
        cases["E"]["Type_I_200bar_model_pressure_duty"],
        selector["minimum_source_bank_model_kg"],
        selector["maximum_source_bank_model_kg"])
    # The price-neutral alpha DUAL bound cannot be derived from the primal
    # witness alone. This independent replay verifies only the E selection
    # PRIMAL, while the original HiGHS gap remains a separately trust-requiring
    # source report assertion.
    return {
        "schema_version":REVIEW_SCHEMA,"year":year,"mode":mode,
        "price_hourly_original_SHA256":psha,"wind_hourly_original_SHA256":wsha,
        "selected_hourly_H2_sha256":tsha,
        "E_source_year_price_blind_service_primal_recomputed":True,
        "E_source_year_E_and_ES_full_hourly_primal_mass_energy_cost_recomputed":True,
        "20_200bar_CoolProp_independent_EOS_extrema_recomputed":True,
        "original_year_UTC_hours":len(price),
        "cost_bounds_and_price_neutral_alpha_global_dual_reoptimized_independently":False,
        "source_hourly_primal_arrays_NOT_in_this_report":True,
        "on_site_industrial_or_native_BAFU_LCA_full_release":False,
        "case_audits":audited,
    }


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--witness",required=True)
    p.add_argument("--aggregate-report",required=True)
    p.add_argument("--private-price",required=True)
    p.add_argument("--private-wind",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args(argv)
    result=review_private_witness(a.witness,a.aggregate_report,a.private_price,a.private_wind)
    out=Path(a.output)
    need(not out.exists(),"do not overwrite previously independently verified case")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print("Independent full-year source primal E/E+S/H2/pressure/cost audit PASSED; HiGHS dual proof and v1.0 NOT certified")


if __name__=="__main__":
    main()
