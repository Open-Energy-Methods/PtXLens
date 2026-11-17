"""L3-F exact eight-file two-repository negative/public scientific admission.

Regenerate ONLY from previously published original source year H30 2022/24
integer physical/cost-replay aggregates, source F2 2023 19-equipment station
reference and conditional L3-E break-even model. No private original hourly
witness, manufacturer quote or BAFU .zolca is accessed.

Eight source-rebuilt results: PtXFlex four (CoolProp thermal two, physical
site PED/HAZOP evidence contract two), PtXLens four (source-year 19-item
unpriced CAPEX viability gate two, native BAFU/OEM/manufacturing evidence
contract two). Regenerate byte-for-byte and reject any accidental private
data disclosure or fabricated cost, equipment certification or native LCIA.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

from ptxflex import f2l3f_stationary_thermal_qualification as thermal
from ptxflex import f2l3f_stationary_site_evidence_gate as site
from . import l3f_h30_cost_qualification_bridge as costs
from . import l3f_bafu_native_mapping_contract as bafu
from . import l3e_exogenous_incremental_dcf as dcf

SCHEMA="ptxlens.l3f_8file_original_H30_max_inventory_2022_2024_source_rebuilt_safety_finance_native_BAFU_release.v1"


class L3FAdmissionError(ValueError):
    pass


def need(condition,text):
    if not condition:
        raise L3FAdmissionError("L3-F eight-file release audit: "+text)


def reconstruct():
    a=thermal.build()
    b=site.make_contract()
    c=costs.build()
    d=bafu.build()
    need(a.get("OEM_qualified_specific_station") is False and
         a.get("installed_incremental_CAPEX_eur") is None and
         b.get("site_pressure_design_engineering_qualified") is False and
         b.get("OEM_and_supplier_all_in_installed_cost_admitted") is False and
         c.get("site_project_commercial_NPV_authorized") is False and
         c.get("all_in_actual_installed_incremental_CAPEX_eur") is None and
         d.get("original_native_BAFU_2026_v11_incremental_total_kgCO2e") is None and
         d.get("scientific_v1_0_native_LCA_gate_passed") is False,
         "original input data promoted beyond an engineering research SCREEN")
    need(len(a["scenarios"])==3 and
         len(b["engineering_domains_to_review"])==13 and
         len(b["original_19_equipment_qualification_lines"])==19 and
         len(c["nineteen_site_verified_supplier_installed_scope_lines"])==19 and
         len(d["separate_19_manufacturer_and_provider_flow_requirements"])==19,
         "expected source equipment, site safety, DCF or BAFU scope changed")
    values={
        ("PtXFlex",thermal.OUT_JSON):json.dumps(a,sort_keys=True,indent=2,allow_nan=False)+"\n",
        ("PtXFlex",thermal.OUT_MD):thermal.markdown(a),
        ("PtXFlex",site.OUT_JSON):json.dumps(b,sort_keys=True,indent=2,allow_nan=False)+"\n",
        ("PtXFlex",site.OUT_MD):site.markdown(b),
        ("PtXLens",costs.OUT_JSON):json.dumps(c,sort_keys=True,indent=2,allow_nan=False)+"\n",
        ("PtXLens",costs.OUT_MD):costs.markdown(c),
        ("PtXLens",bafu.OUT_JSON):json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+"\n",
        ("PtXLens",bafu.OUT_MD):bafu.markdown(d),
    }
    need(len(values)==8,"not exactly eight original scientific artifacts")
    return values


def audit(*,lens_results,flex_results):
    lens=Path(lens_results)
    flex=Path(flex_results)
    need(lens.is_dir() and flex.is_dir() and
         not lens.is_symlink() and not flex.is_symlink(),
         "original public source year result directories unavailable/symlinked")
    results=[]
    for (repo,name),body in reconstruct().items():
        f=(lens if repo=="PtXLens" else flex)/name
        need(f.is_file() and not f.is_symlink(),
             "required source-rebuilt output missing: "+name)
        raw=f.read_bytes()
        need(0<len(raw)<=1200000 and b"\r" not in raw and b"\x00" not in raw,
             "invalid research file binary/size or non-LF: "+name)
        need(raw==body.encode("utf-8"),"source rebuilt report differs: "+name)
        for banned in (b"PtX_PRIVATE_RESEARCH",b"PRIVATE_F3D_",b"BEGIN PRIVATE KEY",
                       b"github_pat_",b"-----BEGIN OPENSSH PRIVATE"):
            need(banned not in raw,"private source/credential marker in "+name)
        results.append({
            "repo":repo,
            "relative_path":"data/results/"+name,
            "size_bytes":len(raw),
            "SHA256_exact_original_source_rebuilt":hashlib.sha256(raw).hexdigest(),
            "original_2022_2024_provider_hourly_or_supplier_signed_docs_exposed":False,
        })
    return {
        "schema_version":SCHEMA,
        "original_2022_2024_exogenous_H30_historical_market_source_Git_blob":dcf.SOURCE_GIT_BLOB,
        "original_F2_source_TypeI_20t_to_40t_reference_blob":thermal.SOURCE_GIT_BLOB,
        "exactly_eight_public_safe_research_reports":results,
        "source_year_matched_hydrogen_and_original_Model_F2_reference_locked":True,
        "actual_2022_2024_dispatch_MILPs_rerun":False,
        "OEM_PED_site_pressure_vessels_qualified":False,
        "authentic_supplier_installed_price_verified":False,
        "native_BAFU_2026_v11_process_system_and_LCIA_replayed":False,
        "environmental_superiority_or_NPV_certified":False,
        "scientific_v1_0_release_qualified":False,
        "git_add_or_commit_or_push_performed":False,
    }


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--lens-results",required=True,type=Path)
    p.add_argument("--flex-results",required=True,type=Path)
    args=p.parse_args(argv)
    d=audit(lens_results=args.lens_results,flex_results=args.flex_results)
    print("L3F_EIGHT_PUBLIC_SAFE_SOURCE_REBUILT_REPORTS_AUDIT_PASS")
    for row in d["exactly_eight_public_safe_research_reports"]:
        print(row["repo"],row["relative_path"],
              row["SHA256_exact_original_source_rebuilt"],"bytes",row["size_bytes"])
    print("Source-audited physical/TEA/BAFU readiness, but no OEM, PED, native LCIA, actual NPV or scientific v1")


if __name__=="__main__":
    main()
