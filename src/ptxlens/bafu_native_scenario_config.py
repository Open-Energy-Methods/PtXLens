"""Generate bounded native BAFU E/E+S input from original-source PyNEXUS audit.

Consumes a source-verified previous 2023 BAFU screening JSON, NOT a synthetic
hours series or manually entered energy inputs. Separate original user-supplied
BAFU 2026 v1.1 native .zolca is required for the actual native calculation.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path

SOURCE_SCHEMA="ptxlens.BAFU_2026_real_observed_source_E_ES_partial_components.v0.1"
KNOWN_SOURCE_SHA={
    "E":"069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051",
    "E_plus_S":"cd4101fe62c3f1b8aa2d7508d3651d2fee40d2bafe6d5b87e40d5f4d055070f9",
}

def make_config(original_bafu_audit):
    if original_bafu_audit.get("schema_version")!=SOURCE_SCHEMA:
        raise ValueError("expected original 2023 PyNEXUS archive and BAFU official API assessment")
    if original_bafu_audit.get("full_product_system_LCA_claim_allowed") is not False:
        raise ValueError("source audit did not preserve partial-LCA claim")
    rows=[]
    for case in ("E","E_plus_S"):
        obj=original_bafu_audit[case]
        actual_sha=obj.get("original_source_archive_sha256")
        if actual_sha != KNOWN_SOURCE_SHA[case]:
            raise ValueError("original historical PyNEXUS E/ES archive is not frozen verified input")
        h2=obj["historical_2023_modelled_H2_delivered_kg"]
        src=obj["historical_2023_electricity_mwh"]
        grid=src["grid_import_for_electrolysis"]*1000/h2
        wind=src["offshore_wind_for_electrolysis"]*1000/h2
        if not all(math.isfinite(v) and v>0 for v in (h2,grid,wind)):
            raise ValueError("invalid observed-input / modeled energy or delivery")
        rows.append({
            "case":case,"original_sha256":actual_sha,
            "modelled_delivered_kg_2023":h2,
            "grid_input_kWh_per_kg_H2":grid,
            "wind_input_kWh_per_kg_H2":wind,
            "incremental_storage_equipment_included":False,
            "source_model":"original frozen 2023 NL PyNEXUS simulated H2 dispatch, observed market prices and ERA5-derived wind"
        })
    return {
        "schema":"ptxlens.native-bafu-2023-source-config-v0.1",
        "source":"source-hash-audited original 2023 NL E and E_plus_S original PyNEXUS artifacts",
        "modelled_not_measured_hydrogen":True,
        "native_BAFU_v11_source_required":True,
        "scope":"30bar PEM reference with changed 2023 grid/wind and NL water; no incremental E+S storage hardware or site-specific validation",
        "cases":rows
    }


def write_config(original_input_json,output_path):
    output=Path(output_path)
    if output.exists():
        raise FileExistsError("do not overwrite source derived scenario inputs")
    raw=Path(original_input_json).read_bytes()
    data=make_config(json.loads(raw))
    data["provenance_previous_audit_sha256"]=hashlib.sha256(raw).hexdigest()
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return data


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--source-audit-json",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    out=write_config(a.source_audit_json,a.output)
    for c in out["cases"]:
        print(c["case"],"grid kWh/kg H2",c["grid_input_kWh_per_kg_H2"],
              "wind kWh/kg H2",c["wind_input_kWh_per_kg_H2"])
