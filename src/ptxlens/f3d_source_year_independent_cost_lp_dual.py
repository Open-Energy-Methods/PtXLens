"""Independent source-year 2022/2024 exact-constraint LP global cost bound.

Reconstruct from scratch (not PtXFlex solver source matrix) the RELAXED
E and E+S H2 dispatch constraints. An optimal LP dual is a mathematically
valid LOWER bound for original identical-physics cost MILP, conditional on
correct construction. Check independent primal feasibility, KKT stationarity,
dual signs/complementarity, objective duality, and source MILP primal cost.

This is NOT independent reconstruction of HiGHS integer branch-and-bound
tree: when the LP–integer primal gap is too wide, status is LP lower bound
ONLY; do not promote original integer MIP global optimality claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

from .f3d_external_year_independent_review import (
    check_result,YEAR_HOURS,
)
from .f3d_external_year_private_witness_replay import (
    read_private_year_csv,review_private_witness,expected_params,
    f64_hash,need,
)

SCHEMA="ptxlens.f3d_independent_original_source_year_relaxed_LP_cost_dual_KKT.v1"
SOURCE_PUBLISHED_GIT_BLOB="ca07f5ef1e381fa157982bc5a68e46ce3022003a"
P,U,G,C,S,CH,DIS,Z=range(8)
FIELDS=8
CASES=("E","E_plus_S")
MODES=("max_inventory","usable_service")


def construct_lp(wind,price,target,params,duty):
    """Independent sparse original-physics *linear-relaxation* reconstruction.

    Source MILP has U,Z binary; LP relaxes them to [0,1].
    All remaining bounds, hourly H2/power/inventory, unit min/max,
    grid, ramp, exclusive charge/discharge and terminal constraints retained.
    """
    n=len(wind)
    need(n>=2 and len(price)==len(target)==n and
         all(np.isfinite(v).all() for v in
             (np.asarray(wind),np.asarray(price),np.asarray(target))),
         "LP original price/wind/H2 series incomplete or nonfinite")
    p=params
    need(p==expected_params(p["capacity_kg"]),
         "LP original source frozen plant parameters changed")
    mode=duty.get("capacity_semantics")
    need(mode in MODES and duty.get("scenario_capacity_kg")==p["capacity_kg"],
         "LP original source compressor/pressure hardware changed")
    heel=float(duty["gas_heel_kg"])
    bottom=heel if mode=="max_inventory" else 0.
    fixed_loss=heel*float(p["loss_fraction_per_hour"]) if mode=="usable_service" else 0.
    comp=float(duty["compressor_electrical_kwh_per_kg_charged"])/1000.
    need(heel>=0 and comp>0 and math.isfinite(comp),
         "source model pressure-screened H2 compressor duty invalid")
    power_max=p["rated_mw"]*p["max_load_fraction"]
    power_min=p["rated_mw"]*p["min_load_fraction"]
    charge=p["charge_max_kg_h"]
    discharge=p["discharge_max_kg_h"]
    loss=p["loss_fraction_per_hour"]
    y=p["h2_coefficient_kg_mwh"]
    grid=p["grid_max_mw"]
    nvar=n*FIELDS
    c=np.zeros(nvar,dtype=np.float64)
    bounds=[]
    eq_i=[];eq_j=[];eq_v=[];beq=[]
    ub_i=[];ub_j=[];ub_v=[];bub=[]
    def put_eq(d,rhs):
        row=len(beq);beq.append(float(rhs))
        for col,v in d.items():
            if v: eq_i.append(row);eq_j.append(col);eq_v.append(float(v))
    def put_ub(d,rhs):
        row=len(bub);bub.append(float(rhs))
        for col,v in d.items():
            if v: ub_i.append(row);ub_j.append(col);ub_v.append(float(v))
    idx=lambda t,k:t*FIELDS+k
    for t in range(n):
        w=float(wind[t]); pr=float(price[t]); h=float(target[t])
        need(0<=w<=125.685+1e-7 and h>0 and
             h<=p["delivery_limit_kg_h"],
             "original source wind power or hourly H2 target outside envelope")
        # LP bounds retain grid signed import/export; curtailment <= wind
        # and all original continuous inventory bounds.
        bounds.extend(((0.,power_max),(0.,1.),(-grid,grid),
                       (0.,w),(bottom,p["capacity_kg"]),
                       (0.,charge),(0.,discharge),(0.,1.)))
        c[idx(t,G)]=pr
        put_eq({idx(t,P):1.,idx(t,C):1.,idx(t,G):-1.,
                idx(t,CH):comp},w)
        put_eq({idx(t,P):y,idx(t,CH):-1.,idx(t,DIS):1.},h)
        flow={idx(t,S):1.,idx(t,CH):-1.,idx(t,DIS):1.}
        if t:
            flow[idx(t-1,S)]=-(1-loss)
            rhs=-fixed_loss
        else:
            rhs=(1-loss)*p["initial_kg"]-fixed_loss
        put_eq(flow,rhs)
        put_ub({idx(t,U):power_min,idx(t,P):-1.},0.)
        put_ub({idx(t,P):1.,idx(t,U):-power_max},0.)
        put_ub({idx(t,CH):1.,idx(t,Z):-charge},0.)
        put_ub({idx(t,DIS):1.,idx(t,Z):discharge},discharge)
        if t:
            put_ub({idx(t,P):1.,idx(t-1,P):-1.},p["ramp_mw_h"])
            put_ub({idx(t-1,P):1.,idx(t,P):-1.},p["ramp_mw_h"])
    put_eq({idx(n-1,S):1.},p["terminal_kg"])
    aeq=coo_matrix((eq_v,(eq_i,eq_j)),shape=(len(beq),nvar)).tocsr()
    aub=coo_matrix((ub_v,(ub_i,ub_j)),shape=(len(bub),nvar)).tocsr()
    return {
        "c":c,"A_eq":aeq,"b_eq":np.asarray(beq,dtype=float),
        "A_ub":aub,"b_ub":np.asarray(bub,dtype=float),
        "lower":np.asarray([z[0] for z in bounds],dtype=float),
        "upper":np.asarray([z[1] for z in bounds],dtype=float),
    }


def solve_and_dual_audit(problem,*,time_limit=900):
    """Independent HiGHS LP KKT and primal–dual objective certificate."""
    need(10<=time_limit<=7200,"unregistered independent LP wall time")
    p=problem
    n=len(p["c"])
    lower=p["lower"]; upper=p["upper"]
    need(lower.shape==upper.shape==(n,) and
         np.isfinite(lower).all() and np.isfinite(upper).all() and
         np.all(lower<=upper),
         "finite source bounds expected for independent dual audit")
    result=linprog(
        c=p["c"],A_eq=p["A_eq"],b_eq=p["b_eq"],
        A_ub=p["A_ub"],b_ub=p["b_ub"],
        bounds=list(zip(lower,upper)),method="highs",
        options={"time_limit":float(time_limit),"presolve":True})
    if result.status!=0 or result.x is None:
        return {
            "LP_optimally_solved":False,
            "HiGHS_LP_status":int(result.status),
            "original_source_MILP_optimality_confirmed":False,
            "source_cost_lower_bound_eur":None,
            "independent_relaxed_LP_dual_KKT_passed":False,
        }
    x=np.asarray(result.x,dtype=np.float64)
    yeq=np.asarray(result.eqlin.marginals,dtype=np.float64)
    yub=np.asarray(result.ineqlin.marginals,dtype=np.float64)
    yl=np.asarray(result.lower.marginals,dtype=np.float64)
    yu=np.asarray(result.upper.marginals,dtype=np.float64)
    # SciPy HiGHS 'marginals' are derivatives of optimal minimization value
    # with respect to RHS; inequality and upper bound marginals <=0,
    # lower bound marginals >=0. All finite bounds make dual objective explicit.
    grad=p["A_eq"].T@yeq+p["A_ub"].T@yub+yl+yu
    stationarity=float(np.max(np.abs(p["c"]-grad)))
    primal_eq=float(np.max(np.abs(p["A_eq"]@x-p["b_eq"])))
    primal_ub=float(np.max(np.maximum(p["A_ub"]@x-p["b_ub"],0.)))
    bound_error=float(np.max(np.maximum(np.maximum(lower-x,x-upper),0.)))
    signs=float(max(0.,np.max(yub),np.max(yu),-np.min(yl)))
    slack_ub=p["b_ub"]-p["A_ub"]@x
    complementarity=float(max(
        np.max(np.abs(yub*slack_ub)),
        np.max(np.abs(yl*(x-lower))),
        np.max(np.abs(yu*(upper-x))),
    ))
    primal=float(np.dot(p["c"],x))
    dual=float(np.dot(p["b_eq"],yeq)+np.dot(p["b_ub"],yub)+
               np.dot(lower,yl)+np.dot(upper,yu))
    objective_diff=primal-dual
    # Tolerances represent numeric residuals of the LP solve; the point
    # is to reject unreliable dual evidence, not silently widen the MIP gap.
    passed=(stationarity<=1e-4 and primal_eq<=5e-4 and
            primal_ub<=5e-4 and bound_error<=5e-5 and
            signs<=1e-5 and complementarity<=5e-2 and
            -0.1<=objective_diff<=0.1 and
            math.isfinite(primal) and math.isfinite(dual))
    return {
        "LP_optimally_solved":True,
        "HiGHS_LP_status":0,
        "source_cost_lower_bound_eur":dual if passed else None,
        "independent_relaxed_LP_dual_KKT_passed":passed,
        "original_source_MILP_optimality_confirmed":False,
        "LP_objective_cost_eur":primal,
        "LP_dual_objective_eur":dual,
        "LP_primal_dual_difference_eur":objective_diff,
        "LP_KKT_max_stationarity":stationarity,
        "LP_KKT_max_equality_residual":primal_eq,
        "LP_KKT_max_inequality_violation":primal_ub,
        "LP_KKT_max_variable_bound_violation":bound_error,
        "LP_KKT_max_sign_violation":signs,
        "LP_KKT_max_complementarity":complementarity,
    }


def check_private_source(year,mode,private_root,public_source):
    need(year in YEAR_HOURS and mode in MODES,"year or storage semantics not accepted")
    root=Path(private_root).resolve(strict=True)
    need(root.name=="PtX_PRIVATE_RESEARCH","independent reviewer only reads original private archive")
    raw=Path(public_source).read_bytes().replace(b"\r\n",b"\n")
    sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    need(sha==SOURCE_PUBLISHED_GIT_BLOB,
         "public original 2022/2024 source Git blob SHA changed")
    source=json.loads(raw.decode("utf-8"))
    cases=[r for r in source.get("cases",[]) if
           r.get("year")==year and r.get("storage_capacity_semantics")==mode]
    need(len(source.get("cases",[]))==4 and len(cases)==1 and
         source.get("independent_year_mode_full_hourly_primal_E_EplusS_and_EOS_replay_passed") is True and
         source.get("independent_solver_dual_certificates_recomputed") is False,
         "missing reviewed original source case or false independent dual")
    published=cases[0]
    rp=root/"results"/f"F3D_ARCO_{year}_{mode}.json"
    wi=root/"results"/f"PRIVATE_F3D_ARCO_{year}_{mode}_primal.json"
    pr=root/f"price-{year}"/"normalized_UTC_price.csv"
    windp=root/f"wind-arco-{year}"/"normalized_UTC_wind.csv"
    verified=check_result(json.loads(rp.read_text(encoding="utf-8")))
    need(verified["year"]==year and verified["capacity_semantics"]==mode and
         verified["source_price_SHA256"]==published["source_year_price_f64_sha256"] and
         verified["source_wind_SHA256"]==published["source_year_wind_f64_sha256"],
         "public original source hashes mismatch local private independently checked report")
    audit=review_private_witness(wi,rp,pr,windp)
    need(audit.get("E_source_year_E_and_ES_full_hourly_primal_mass_energy_cost_recomputed") is True,
         "reference 2022/2024 original full hourly primal failed independent replay")
    witness=json.loads(wi.read_text(encoding="utf-8"))
    target=witness["target_hourly_kg"]
    price=read_private_year_csv(pr,year,"day_ahead_eur_mwh")
    wind=read_private_year_csv(windp,year,"wind_available_mw",nonnegative=True)
    need(f64_hash(target)==published["price_neutral_E_uniform_hydrogen_service"]["hourly_target_f64_sha256"] and
         f64_hash(price)==published["source_year_price_f64_sha256"] and
         f64_hash(wind)==published["source_year_wind_f64_sha256"],
         "new LP cannot use changed private provider price/wind or H2 target")
    return published,witness,wind,price,target


def independent_lp_review(year,mode,private_root,public_source,*,time_limit=900):
    published,witness,wind,price,target=check_private_source(
        year,mode,private_root,public_source)
    results={}
    for name,capacity in (("E",20000),("E_plus_S",40000)):
        params=expected_params(capacity)
        duty=witness["cases"][name]["Type_I_200bar_model_pressure_duty"]
        problem=construct_lp(wind,price,target,params,duty)
        result=solve_and_dual_audit(problem,time_limit=time_limit)
        primal=float(published[name]["modelled_nominal_eur_wholesale_cost"])
        source_dual=float(published[name]["solver_reported_cost_dual_lower_bound_eur"])
        if result["independent_relaxed_LP_dual_KKT_passed"]:
            lb=result["source_cost_lower_bound_eur"]
            need(lb<=primal+.1 and lb<=source_dual+.1 and source_dual<=primal+.1,
                 "independent original model LP floor conflicts with source integer reported objective")
            gap=max(0.,primal-lb)/max(1.,abs(primal))
            result["LP_to_original_integer_primal_relative_cost_gap"]=gap
            result["original_MILP_optimality_inferred_from_independent_root_LP_bound"]=(gap<=1e-6)
        else:
            result["LP_to_original_integer_primal_relative_cost_gap"]=None
            result["original_MILP_optimality_inferred_from_independent_root_LP_bound"]=False
        result["original_source_integer_primal_cost_eur"]=primal
        result["original_source_reported_integer_dual_cost_eur_NOT_independently_verified"]=source_dual
        results[name]=result
    fully_certified=all(r["original_MILP_optimality_inferred_from_independent_root_LP_bound"]
                        for r in results.values())
    return {
        "schema_version":SCHEMA,"source_year":year,"mode":mode,
        "source_hours":YEAR_HOURS[year],
        "original_source_public_Git_blob":SOURCE_PUBLISHED_GIT_BLOB,
        "original_source_price_f64_sha256":published["source_year_price_f64_sha256"],
        "original_source_wind_f64_sha256":published["source_year_wind_f64_sha256"],
        "original_hourly_hydrogen_service_f64_sha256":
            published["price_neutral_E_uniform_hydrogen_service"]["hourly_target_f64_sha256"],
        "E_and_EplusS_independent_LP_relaxed_global_cost_lower_bound_cases":results,
        "both_costs_recovered_within_original_1e_minus6_gap_by_INDEPENDENT_LP":fully_certified,
        "original_HiGHS_branch_and_bound_dual_reconstructed":False,
        "native_BAFU_or_manufacturer_or_site_or_v1_0":False,
        "no_original_private_market_wind_or_dispatch_hourly_vectors_in_report":True,
    }


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--year",type=int,choices=sorted(YEAR_HOURS),required=True)
    p.add_argument("--mode",choices=MODES,required=True)
    p.add_argument("--private-root",type=Path,
                   default=Path.home()/"PtX_PRIVATE_RESEARCH")
    p.add_argument("--public-source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--LP-time-limit",type=int,default=900)
    a=p.parse_args(argv)
    result=independent_lp_review(a.year,a.mode,a.private_root,a.public_source,
                                 time_limit=a.LP_time_limit)
    out=Path(a.output)
    need(out.parent.is_dir(),"existing public evidence directory required")
    text=json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n"
    need(not out.exists() or (out.is_file() and out.read_text(encoding="utf-8")==text),
         "immutable external source LP certificate report changed")
    if not out.exists():
        with out.open("x",encoding="utf-8",newline="\n") as file:file.write(text)
    flag=result["both_costs_recovered_within_original_1e_minus6_gap_by_INDEPENDENT_LP"]
    print(f"PTXLENS_INDEPENDENT_SOURCE_LP_KKT_REVIEW_DONE year={a.year} "
          f"mode={a.mode}; both original source cost optima proven within "
          f"1e-6 by INDEPENDENT LP? {flag}; "
          "not HiGHS integer-tree dual; no vendor/BAFU/plant/v1 release")

if __name__=="__main__":
    main()
