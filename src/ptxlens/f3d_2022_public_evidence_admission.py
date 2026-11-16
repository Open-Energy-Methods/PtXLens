"""F3-D guarded publication admission for nine PUBLIC-SAFE original 2022 research results.

Only accepts the nine exact 2022/max_inventory result basenames produced by
previous separately executed PtXLens reviewers. No private source CSVs or
full-hour solver witnesses. This is an *additional source/provenance/data
minimization check*, not an independent rerun of an optimization or physics.

Fails closed on:
  - missing/extra listed files, symlinks, odd schema, overwritten source
  - changed SHA256 link between LP screening and H30 integer replay
  - nonfinite scientific quantities, unmatched original H2/price/wind hashes
  - contradiction in paired E/E+S source economics or false release flags
  - large lists, tall hidden arrays, suspicious private-witness data keys
  - unrecognized original public four-case Git blob
  - excessive string lengths or accidental original source-hour time vectors

Neither this tool nor a passing result asserts source integer-tree dual
independent proof, real manufacturer costs, site performance or BAFU LCIA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from .f3d_exogenous_service_lp_screen import SCHEMA as EXOGENOUS_LP_SCHEMA
from .f3d_exogenous_h2_integer_independent_replay import (
    SCHEMA as EXOGENOUS_INTEGER_SCHEMA
)
from .f3d_external_year_counterfactual_independent_review import (
    SCHEMA as WIND_CF_SCHEMA
)
from .f3d_wind_reduction_independent_feasibility import (
    SCHEMA as WIND_RECONSTRUCTED_LP_SCHEMA
)
from .f3d_analytic_wind_feasibility_threshold import (
    SCHEMA as ANALYTIC_WIND_SCHEMA
)
from .f3d_independent_wind_lp_bracket import SCHEMA as WIND_LP_BRACKET_SCHEMA
from .f3d_source_year_independent_cost_lp_dual import SOURCE_PUBLISHED_GIT_BLOB

SCHEMA="ptxlens.f3d_2022_independently_verified_source_model_safe_publication_admission.v1"
YEAR=2022
MODE="max_inventory"
NAME_TO_SCHEMA={
    "F3D_2022_max_inventory_EXOGENOUS_H2_SOURCE_LP_FEASIBILITY_SCREEN_v1.json":
        EXOGENOUS_LP_SCHEMA,
    "F3D_CF_2022_max_inventory_wind_power_090_INDEPENDENT_PUBLIC_REPLAY.json":
        WIND_CF_SCHEMA,
    "F3D_EXOGENOUS_2022_max_inventory_H30_W090_BOTH_INTEGER_INDEPENDENT_REPLAY_v1.json":
        EXOGENOUS_INTEGER_SCHEMA,
    "F3D_WIND_090_2022_max_inventory_ANALYTIC_FEASIBILITY_FACTOR_LOWER_BOUND_v1.json":
        ANALYTIC_WIND_SCHEMA,
    "F3D_WIND_090_2022_max_inventory_INDEPENDENT_E_LP_FEASIBILITY_BRACKET_v1.json":
        WIND_LP_BRACKET_SCHEMA,
    "F3D_WIND_090_2022_max_inventory_INDEPENDENT_SOURCE_LP_FEASIBILITY_v1.json":
        WIND_RECONSTRUCTED_LP_SCHEMA,
}
ADDITIONAL_MD_FILES=(
    "F3D_2022_max_inventory_EXOGENOUS_H2_SOURCE_LP_FEASIBILITY_SCREEN_v1.md",
    "F3D_WIND_090_2022_max_inventory_ANALYTIC_FEASIBILITY_FACTOR_LOWER_BOUND_v1.md",
    "F3D_WIND_090_2022_max_inventory_INDEPENDENT_E_LP_FEASIBILITY_BRACKET_v1.md",
)
APPROVED=tuple(NAME_TO_SCHEMA)+ADDITIONAL_MD_FILES

# Explicit high-risk PRIVATE producer keys; broader input checks below catch
# many plausible renamed or nested arrays too. Flags mentioning "NOT_in_public"
# are legitimate and need not be rejected.
BANNED_KEYS={
    "source_original_model_8field_primal_witness",
    "original_full_hourly_states_8var_PRIVATE",
    "cost_optimum_hourly_states",
    "E_price_neutral_alpha_witness_hourly_states",
    "target_hourly_kg",
    "normalized_UTC_price",
    "normalized_UTC_wind",
    "hourly_solved_states",
    "modelled_hourly_delivered_kg",
    "source_original_price_hourly",
    "source_original_wind_hourly",
}
MAX_JSON_BYTES=256*1024
MAX_MD_BYTES=128*1024
MAX_STRING_CHARS=4096
MAX_SEQUENCE_ENTRIES=20
MAX_OBJECT_ENTRIES=80


class EvidenceReleaseError(ValueError):
    pass


def need(ok, message):
    if not ok:
        raise EvidenceReleaseError("F3-D public evidence admission: "+message)


def numeric(value,name):
    need(type(value) in (int,float) and math.isfinite(value),
         "nonfinite or missing "+name)
    return float(value)


def floating_sha(vec):
    raw=np.asarray(vec,dtype="<f8")
    need(raw.ndim==1 and np.isfinite(raw).all(),
         "registered float64 source vector invalid")
    return hashlib.sha256(raw.tobytes()).hexdigest()


def source_blob_sha(raw):
    return hashlib.sha1(
        b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw
    ).hexdigest()


def minimize_tree(obj, *, stack="root",depth=0):
    """Refuse all high-volume or opaque provider-array shaped public records."""
    need(depth<=16,"public evidence JSON nesting beyond acceptable scientific schema")
    if type(obj) is dict:
        need(len(obj)<=MAX_OBJECT_ENTRIES,
             "oversized scientific metadata object at "+stack)
        for k,v in obj.items():
            need(type(k) is str and len(k)<=160,
                 "unrecognized metadata key type/length at "+stack)
            need(k not in BANNED_KEYS,
                 "forbidden source original hourly or private witness field "+k)
            minimize_tree(v,stack=stack+"."+k,depth=depth+1)
    elif type(obj) is list:
        need(len(obj)<=MAX_SEQUENCE_ENTRIES,
             "overlong source data sequence at "+stack)
        for i,v in enumerate(obj):
            minimize_tree(v,stack=stack+f"[{i}]",depth=depth+1)
    elif type(obj) is str:
        need(len(obj)<=MAX_STRING_CHARS and "\x00" not in obj,
             "oversized/opaque source string at "+stack)
        need(not any(x in obj for x in (
            "BEGIN PRIVATE KEY","AKIA","github_pat_","ghp_","glpat-"
        )), "possibly sensitive credential content in "+stack)
    elif obj is None or type(obj) is bool:
        return
    elif type(obj) in (int,float):
        need(math.isfinite(obj),"nonfinite numeric observation at "+stack)
    else:
        need(False,"unsupported public JSON field at "+stack)


def read_evidence(root):
    root=Path(root)
    need(root.is_dir() and not root.is_symlink(),
         "source research result directory not an ordinary directory")
    records={}; byte_hashes={}
    for filename in APPROVED:
        p=root/filename
        need(p.is_file() and not p.is_symlink() and p.parent==root,
             "expected source public evidence file absent/symlinked "+filename)
        raw=p.read_bytes()
        limit=MAX_JSON_BYTES if filename.endswith(".json") else MAX_MD_BYTES
        need(0<len(raw)<=limit,
             "source public research result file empty/oversized "+filename)
        need(b"\x00" not in raw and b"\r" not in raw,
             "possible binary/CRLF contamination in scientific public file "+filename)
        byte_hashes[filename]=hashlib.sha256(raw).hexdigest()
        if filename.endswith(".json"):
            d=json.loads(raw.decode("utf-8"))
            minimize_tree(d,stack=filename)
            need(d.get("schema_version")==NAME_TO_SCHEMA[filename],
                 "wrong public scientific source report schema "+filename)
            records[filename]=d
        else:
            md=raw.decode("utf-8")
            need("PRIVATE_F3D_" not in md and
                 "PtX_PRIVATE_RESEARCH" not in md and
                 len(md)<MAX_MD_BYTES,
                 "private original source path in generated public MD "+filename)
    return records,byte_hashes


def audit_source_and_exogenous(records,byte_hashes,source_original_bytes):
    def from_base(fragment):
        matches=[(filename,d) for filename,d in records.items() if fragment in filename]
        need(len(matches)==1,"exact public file missing/ambiguous for "+fragment)
        return matches[0]

    need(source_blob_sha(source_original_bytes)==SOURCE_PUBLISHED_GIT_BLOB,
         "original scientific 2022/2024 public source Git blob changed")
    source=json.loads(source_original_bytes.decode("utf-8"))
    original=[c for c in source["cases"] if c["year"]==YEAR and
              c["storage_capacity_semantics"]==MODE]
    need(len(original)==1,"source 2022 max_inventory original reference missing")
    original=original[0]
    historical_price=original["source_year_price_f64_sha256"]
    historical_wind=original["source_year_wind_f64_sha256"]
    original_service=original["price_neutral_E_uniform_hydrogen_service"]["hourly_target_f64_sha256"]

    lp_name,lp=from_base("EXOGENOUS_H2_SOURCE_LP_FEASIBILITY_SCREEN")
    integer_name,integer=from_base("H30_W090_BOTH_INTEGER_INDEPENDENT_REPLAY")
    need(lp.get("source_year")==YEAR and
         lp.get("capacity_semantics")==MODE and
         lp.get("source_calendar_UTC_hours")==8760 and
         lp.get("source_original_4_case_public_Git_blob_sha1")==SOURCE_PUBLISHED_GIT_BLOB and
         lp.get("source_original_price_float64_SHA256")==historical_price and
         lp.get("source_original_wind_power_float64_SHA256")==historical_wind and
         lp.get("source_original_E_max_selected_hourly_H2_float64_SHA256")==original_service and
         lp.get("prespecified_exogenous_delivery_tonnes_day")==[25.,27.5,30.] and
         lp.get("source_wind_electric_power_multipliers")==[.9,.95,1.] and
         lp.get("same_H2_target_hourly_for_E_and_ES_at_every_wind_factor") is True and
         lp.get("original_integer_dispatch_or_matched_wholesale_savings_certified") is False and
         lp.get("real_site_or_manufacturer_or_native_BAFU_or_scientific_v1_0") is False,
         "source 2022 exogenous LP service/year provenance or release scope changed")
    matched=lp.get("nine_service_factor_pairs_two_architectures_LP_cells",[])
    need(type(matched) is list and len(matched)==9 and
         len({(r.get("exogenous_H2_tonnes_per_day"),
               r.get("source_wind_power_multiplier")) for r in matched})==9,
         "original exogenous H2 service / source wind factor grid incomplete/duplicate")
    need(all(set(r.get("cases",{}))=={"E","E_plus_S"} and
             all(c.get("HiGHS_LP_status_code")==0 and
                 c.get("original_integer_MILP_feasible") is None
                 for c in r["cases"].values())
             for r in matched),
         "2022 original LP source case success not complete")
    selected=[r for r in matched if r["exogenous_H2_tonnes_per_day"]==30. and
              r["source_wind_power_multiplier"]==.9]
    need(len(selected)==1,"2022 predeclared H30 W090 comparison absent")
    exo_hash=floating_sha([1250.]*8760)
    need(selected[0]["exogenous_H2_original_same_hourly_SHA256"]==exo_hash,
         "original 30t/day exogenous H2 target float64 not matched")
    need(integer.get("source_year")==YEAR and
         integer.get("capacity_semantics")==MODE and
         integer.get("source_year_UTC_hours")==8760 and
         integer.get("source_original_four_case_public_Git_blob_sha1")==SOURCE_PUBLISHED_GIT_BLOB and
         integer.get("independent_LP_screen_bytes_SHA256")==byte_hashes[lp_name] and
         integer.get("original_price_f64_SHA256")==historical_price and
         integer.get("original_wind_electric_power_f64_SHA256")==historical_wind and
         integer.get("exogenous_fixed_hourly_hydrogen_service_f64_SHA256")==exo_hash and
         integer.get("matched_exogenous_hydrogen_service_tonnes_day")==30. and
         integer.get("E_and_ES_fully_independent_primal_mass_electricity_EOS_market_replay") is True and
         integer.get("cost_lower_bound_source_reported_NOT_independent_dual_reconstruction") is True and
         integer.get("actual_site_or_manufacturer_or_BAFU_LCIA_or_scientific_v1_0_certified") is False and
         integer.get("original_hourly_provider_arrays_or_solver_witnesses_in_public") is False,
         "independent full-year source H30 W090 replay unsupported or source SHA mismatch")
    annual=numeric(integer.get("matched_exogenous_service_annual_H2_kg"),"annual H2")
    need(abs(annual-10950000.)<=.005,"annual H2 not exact matched 30t/day")
    cases=integer.get("case_results")
    need(type(cases) is dict and set(cases)=={"E","E_plus_S"},
         "source E/E+S independently verified integer pair missing")
    cost={}
    for name in ("E","E_plus_S"):
        c=cases[name]
        need(c.get("status")==
             "INDEPENDENT_ORIGINAL_FULL_YEAR_INTEGER_PRIMAL_H2_ELECTRIC_EOS_REPLAY_PASSED" and
             c.get("original_private_hourly_H2_wind_price_primal_vectors_NOT_in_public") is True and
             c.get("independent_integer_cost_dual_tree_proof") is False,
             "source original integer case not independently physically replayed")
        need(abs(numeric(c.get("independent_annual_delivered_H2_kg"),name+" annual H2")-annual)<.005 and
             0<=numeric(c.get("source_reported_relative_MIP_gap"),name+" source MIP gap")<=1e-6 and
             numeric(c.get("independent_source_max_physical_residual"),name+" residual")<=2e-4 and
             numeric(c.get("independent_EOS_min_absolute_bar"),name+" EOS low")>=20.-1e-4 and
             numeric(c.get("independent_EOS_max_absolute_bar"),name+" EOS high")<=200.+1e-4,
             "original source case cost acceptance/pressure/hydrogen/physical residual failed")
        source_cost=numeric(c.get("source_modelled_nominal_original_year_wholesale_eur"),name+" source cost")
        lo=numeric(c.get("source_reported_solver_cost_lower_bound_eur"),name+" solver reported lower")
        need(lo<=source_cost+.10,"source solver reported dual bound exceeds feasible source cost")
        cost[name]={"cost_eur":source_cost,"lower_eur":lo}
    saving=cost["E"]["cost_eur"]-cost["E_plus_S"]["cost_eur"]
    claimed=numeric(integer.get("matched_service_modelled_wholesale_E_minus_ES_saving_source_eur"),"matched saving")
    need(abs(saving-claimed)<=.02,"independent source model E−E+S arithmetic inconsistent")
    need(abs(claimed/annual-numeric(integer.get("matched_service_modelled_saving_eur_per_kg_H2"),"EUR per kg"))<1e-10,
         "matched 30t/day H2 normalized saving inaccurate")
    source_lower=cost["E"]["lower_eur"]-cost["E_plus_S"]["cost_eur"]
    source_upper=cost["E"]["cost_eur"]-cost["E_plus_S"]["lower_eur"]
    interval=integer.get("matched_service_source_solver_reported_savings_lower_upper_eur")
    need(type(interval) is list and len(interval)==2 and
         abs(numeric(interval[0],"source lower")-source_lower)<.05 and
         abs(numeric(interval[1],"source upper")-source_upper)<.05 and
         source_lower-.02<=claimed<=source_upper+.02,
         "source HiGHS cost bound interval not arithmetically reproduced")
    return {
        "verified_original_historical_source_public_blob":SOURCE_PUBLISHED_GIT_BLOB,
        "exogenous_year":YEAR,"capacity_semantics":MODE,
        "exogenous_H2_tonnes_per_day":30.,
        "available_model_wind_electric_power_factor":.9,
        "source_model_annual_h2_kg":annual,
        "annual_E_20t_original_integer_wholesale_cost_eur":cost["E"]["cost_eur"],
        "annual_EplusS_40t_original_integer_wholesale_cost_eur":cost["E_plus_S"]["cost_eur"],
        "independently_replayed_original_integer_H2_power_EOS_market":True,
        "paired_E_minus_EplusS_nominal_source_year_eur":saving,
        "per_kg_modelled_source_year_nominal_eur":claimed/annual,
        "reported_solver_savings_lower_upper_eur":[source_lower,source_upper],
        "integer_MIP_tree_dual_independently_recomputed":False,
        "real_site_OEM_native_BAFU_and_scientific_v1_0_verified":False,
    }


def audit(root,original_public):
    root=Path(root)
    records,sha=read_evidence(root)
    original_public=Path(original_public)
    need(original_public.is_file() and not original_public.is_symlink(),
         "original public source-verified aggregate absent or symlinked")
    out=audit_source_and_exogenous(records,sha,original_public.read_bytes())
    out["schema_version"]=SCHEMA
    out["approved_public_files"]=[
        {"relative_path":"data/results/"+name,"file_SHA256":sha[name]}
        for name in APPROVED
    ]
    out["all_9_sanitized_source_model_evidence_files_present"]=True
    out["private_hourly_provider_and_original_integer_witness_vectors_read_or_exported"]=False
    return out


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--results-dir",required=True,type=Path)
    p.add_argument("--original-public-source",required=True,type=Path)
    opts=p.parse_args(argv)
    r=audit(opts.results_dir,opts.original_public_source)
    print("F3D_PUBLIC_SOURCE_EVIDENCE_PRESUBMISSION_AUDIT_PASS",
          f"{len(r['approved_public_files'])} allowlisted source-audited files",
          "2022 max_inventory exogenous 30t/day x 90pct wind",
          f"modelled wholesale source-EUR saving={r['paired_E_minus_EplusS_nominal_source_year_eur']:.2f}",
          "independent hourly replay YES, original HiGHS integer-tree dual NO",
          "real plant/OEM/native BAFU v1 NO")
    for item in r["approved_public_files"]:
        print(item["relative_path"],item["file_SHA256"])


if __name__=="__main__":
    main()
