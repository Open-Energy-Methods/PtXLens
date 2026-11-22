"""L3-E fail-closed seven-file source-rebuilt publication integrity admission.

Rebuilds from pinned existing PUBLIC source: 2022/2024 H30 W090 full
E20t/E+S40t physical/cost receipts, F2 original 19-line Type I equipment
requirements. Exact regenerations, not self-attested JSON metadata, must
match every research output byte-for-byte: DCF JSON+Markdown, original F2
hardware/BAFU 19-line JSON+MD, source annual import/export inventory JSON+MD,
and PtXFlex original 19-line OEM questionnaire JSON.

Never opens PtX_PRIVATE_RESEARCH, original hourly market/wind arrays, full
8-column original source MILP witnesses or any private manufacturer document.
Does NOT stage, commit or push research outputs. It certifies provenance,
reproducibility and safe public metadata only, NOT manufacturer hardware,
native BAFU process mapping, lifecycle impacts, industrial safety, or NPV.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

from . import l3e_exogenous_incremental_dcf as economic
from . import l3e_exogenous_incremental_hardware_lci as hardware
from . import l3e_exogenous_operational_energy_inventory as energy
from ptxflex import f2l3e_exogenous_vendor_cost_intake as vendor

SCHEMA="ptxlens.l3e_source_rebuild_verified_7file_H30_2022_2024_public_research_admission.v1"
MAX_JSON_BYTES=2500000
MAX_MD_BYTES=180000


class L3EPublicAdmissionError(ValueError):
    pass


def need(ok,reason):
    if not ok:
        raise L3EPublicAdmissionError("L3-E publication admission: "+reason)


def artifacts():
    """Read actual source-backed code results, not metadata claim flags."""
    dcf=economic.build(economic.load_admitted_source())
    bom=hardware.build()
    op=energy.build()
    supplier=vendor.make()
    docs={
        ("PtXLens",economic.OUT_JSON):json.dumps(
            dcf,sort_keys=True,indent=2,allow_nan=False)+"\n",
        ("PtXLens",economic.OUT_MD):economic.markdown(dcf),
        ("PtXLens",hardware.OUT_JSON):json.dumps(
            bom,sort_keys=True,indent=2,allow_nan=False)+"\n",
        ("PtXLens",hardware.OUT_MD):hardware.markdown(bom),
        ("PtXLens",energy.OUT_JSON):json.dumps(
            op,sort_keys=True,indent=2,allow_nan=False)+"\n",
        ("PtXLens",energy.OUT_MD):energy.markdown(op),
        ("PtXFlex",vendor.OUT):json.dumps(
            supplier,sort_keys=True,indent=2,allow_nan=False)+"\n",
    }
    need(len(docs)==7,"source code did not reconstruct exactly seven outputs")
    # An original F2 reference does not become installed OEM foreground by
    # successfully writing a signed-source-ready empty questionnaire.
    need(dcf.get("scientific_v1_0_economic_gate_passed") is False and
         dcf.get("manufacturer_supplier_verified_incremental_all_in_CAPEX_eur") is None and
         bom.get("scientific_v1_0_environmental_release_allowed") is False and
         bom.get("actual_manufacturer_total_incremental_material_input_kg") is None and
         op.get("lifecycle_incremental_kgCO2e_per_kg_delivered_H2") is None and
         supplier.get("manufacturer_quote_aggregated_all_in_incremental_installed_CAPEX_eur") is None and
         supplier.get("native_BAFU_2026_original_v11_inventory_or_LCIA_certified") is False,
         "L3-E financial/OEM/BAFU evidence was promoted beyond source-supported status")
    need(len(dcf["two_year_assumption_scenario_grid"])==324 and
         len(bom["nineteen_research_equipment_and_evidence_lines"])==19 and
         len(supplier["nineteen_required_supplier_and_site_intake_lines"])==19 and
         len(op["yearly"])==2 and
         op["yearly"][0]["EplusS_MINUS_E_delta_net_grid_import_MWh"]>0 and
         op["yearly"][1]["EplusS_MINUS_E_delta_net_grid_import_MWh"]<0,
         "source DCF grid/hardware quantity/annual energy sign or source data changed")
    return docs


def audit(lens_results,flex_results):
    lens_results=Path(lens_results)
    flex_results=Path(flex_results)
    need(lens_results.is_dir() and not lens_results.is_symlink() and
         flex_results.is_dir() and not flex_results.is_symlink(),
         "public research result directories missing or symlinked")
    expected=artifacts()
    allowed=[]
    for (which,filename),reconstructed in expected.items():
        target=(lens_results if which=="PtXLens" else flex_results)/filename
        need(target.parent.is_dir() and target.is_file() and not target.is_symlink(),
             "source rebuilt public research evidence file missing: "+filename)
        raw=target.read_bytes()
        limit=MAX_JSON_BYTES if filename.endswith(".json") else MAX_MD_BYTES
        need(0<len(raw)<=limit and b"\x00" not in raw and b"\r" not in raw,
             "source rebuilt file contains binary data, excess size or non-LF newline: "+filename)
        canonical=reconstructed.encode("utf-8")
        need(raw==canonical,
             "source 2022/2024/F2 reconstructed file differs byte-for-byte: "+filename)
        need(b"-----BEGIN PRIVATE" not in raw and
             b"PRIVATE_F3D_EXOGENOUS" not in raw and
             b"PtX_PRIVATE_RESEARCH" not in raw and
             b"github_pat_" not in raw,
             "public output accidentally contains original private data path/credential: "+filename)
        allowed.append({
            "repository":which,
            "relative_path":"data/results/"+filename,
            "source_rebuilt_identical_sha256":hashlib.sha256(raw).hexdigest(),
            "file_bytes":len(raw),
            "private_original_provider_hourly_witness_included":False,
        })
    need(len(allowed)==7,"some original independently reconstructed outputs missing")
    return {
        "schema_version":SCHEMA,
        "source_2022_2024_exogenous_H30_crossyear_original_Git_blob":
            economic.SOURCE_GIT_BLOB,
        "source_original_F2_200bar_typeI_19_line_BOM_Git_blob":
            vendor.SOURCE_GIT_BLOB,
        "source_original_2022_and_2024_hourly_electricity_replay_blob_SHA1":
            [energy.BLOBS[2022],energy.BLOBS[2024]],
        "exactly_seven_safe_reconstructed_public_research_reports":allowed,
        "all_reports_independently_regenerated_from_git_pinned_public_inputs":True,
        "real_supplier_quotes_or_price_assumptions_present":False,
        "actual_virgin_steel_input_derived_from_empty_equipment_mass":False,
        "native_BAFU_v11_process_and_LCIA_reproduced":False,
        "real_site_project_NPV_or_environmental_superiority_claimed":False,
        "git_staging_push_or_private_data_upload_performed":False,
    }


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--lens-results",type=Path,required=True)
    p.add_argument("--flex-results",type=Path,required=True)
    args=p.parse_args(argv)
    report=audit(args.lens_results,args.flex_results)
    print("L3E_PUBLIC_RESEARCH_EXACT_7_ARTIFACT_SOURCE_REBUILD_ADMISSION_PASS")
    for item in report["exactly_seven_safe_reconstructed_public_research_reports"]:
        print(item["repository"],item["relative_path"],
              item["source_rebuilt_identical_sha256"],
              "bytes",item["file_bytes"])
    print("No private source/quotes/witnesses, no OEM certification, no BAFU native LCIA, no scientific v1")


if __name__=="__main__":
    main()
