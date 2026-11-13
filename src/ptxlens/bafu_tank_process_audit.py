"""Audit actual licensed original BAFU v1 EcoSpold high-pressure tank LCI.

Reads a private, user-provided original BAFU 2026 v1 EcoSpold ZIP and
produces a limited, derived metadata/physical-units report. Never republishes
the original XML. It does not infer that the v1.1 native tank matches v1.

Critical trap: source high-pressure tank has reference unit "kg" but the
source generalComment explicitly describes "per 1 kg hydrogen" and the
technosphere recipe contains >10 kg actual raw materials. This cannot be
automatically linked as per kg empty Type I steel vessel without verifying
the actual intended reference flow and technology. We reject that mapping.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import zipfile

from lxml import etree

BAFU_TANK_UUID="b4739ad2-aa38-368d-8ada-63f5417c8b55"
BAFU_SOURCE_V1_ZIP_SHA256="ebaab56717a6227b5eb271fcb4c86fb9db206115eb937fb0ec0b10d7accf26c7"
SOURCE_NAME="High pressure hydrogen storage tank"
SOURCE_CITATION="BAFU:2026 v1 original EcoSpold, source process UUID b4739ad2-aa38-368d-8ada-63f5417c8b55"
VALIDATED_MATERIALS={
 "Steel, low-alloyed, at plant":("kg",0.9),
 "Chromium steel 18/8, at plant":("kg",0.9),
 "Carbon fiber, weaved, at factory":("kg",7.14),
 "Aluminium alloy, AlMg3, at plant":("kg",0.6),
 "Epoxy resin, liquid, at plant":("kg",3.06),
}
# Manufacturing operations in kg-equivalent handling; NEVER count as extra
# kg of installed tank material.
VALIDATED_PROCESSING={
 "Sheet rolling, copper":("kg",0.9),
 "Sheet rolling, aluminium":("kg",0.6),
 "Sheet rolling, chromium steel":("kg",0.9),
}


class PhysicalSourceMismatch(ValueError):
    pass


def _sha_file(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for c in iter(lambda:f.read(1<<20),b""):h.update(c)
    return h.hexdigest()


def inspect_original_bafu_tank(original_zip):
    original_zip=Path(original_zip)
    digest=_sha_file(original_zip)
    if digest!=BAFU_SOURCE_V1_ZIP_SHA256:
        raise PhysicalSourceMismatch("unverified original BAFU:2026 v1 EcoSpold ZIP SHA256")
    try:
        with zipfile.ZipFile(original_zip) as z:
            exact=[p for p in z.namelist() if p.endswith("process_"+BAFU_TANK_UUID+".xml")]
            if len(exact)!=1:
                raise PhysicalSourceMismatch("exact original high-pressure tank UUID missing or ambiguous")
            root=etree.fromstring(z.read(exact[0]))
    except zipfile.BadZipFile as exc:
        raise PhysicalSourceMismatch("not a real BAFU source archive") from exc

    rf=root.find(".//referenceFunction")
    if rf is None or rf.get("name")!=SOURCE_NAME or rf.get("unit")!="kg":
        raise PhysicalSourceMismatch("original source tank reference product metadata mismatch")
    comment=rf.get("generalComment") or ""
    if "per 1 kg hydrogen" not in comment or "Boureima et al" not in comment:
        raise PhysicalSourceMismatch("source functional-basis caveat missing")

    inps={}
    for e in root.findall(".//flowData/exchange"):
        if e.findtext("inputGroup")!="5":continue
        name=e.get("name")
        if name in inps:raise PhysicalSourceMismatch("duplicate material/process exchange")
        val=float(e.get("meanValue"))
        if not math.isfinite(val) or val<0:
            raise PhysicalSourceMismatch("invalid source LCI input amount")
        inps[name]={"unit":e.get("unit"),"amount":val}

    for source,expected in {**VALIDATED_MATERIALS,**VALIDATED_PROCESSING}.items():
        item=inps.get(source)
        if item is None or item["unit"]!=expected[0] or not math.isclose(item["amount"],expected[1],rel_tol=0,abs_tol=1e-12):
            raise PhysicalSourceMismatch("source tank material/process inventory changed: "+source)

    raw_material_input_kg=sum(inps[name]["amount"] for name in VALIDATED_MATERIALS)
    if raw_material_input_kg<=10:
        raise PhysicalSourceMismatch("unexpected source tank composite material mass")
    return {
      "schema_version":"ptxlens.BAFU2026_v1_original_high_pressure_tank_technological_mismatch.v0.1",
      "source_original_sha256":digest,"source_reference_uuid":BAFU_TANK_UUID,
      "source_reference_name":SOURCE_NAME,"source_reference_unit":rf.get("unit"),
      "source_citation":SOURCE_CITATION,
      "source_general_comment_reference_basis":"Source explicitly says per 1 kg hydrogen, despite labelled product unit kg.",
      "verified_source_documented_lifetime_years":20,
      "named_input_materials_kg_per_unit_of_ambiguous_reference":{
          name:inps[name]["amount"] for name in VALIDATED_MATERIALS},
      "named_material_inputs_sum_kg_per_reference_unit":raw_material_input_kg,
      "material_processing_operations_separate_from_product_mass":{
          name:inps[name]["amount"] for name in VALIDATED_PROCESSING},
      "is_source_raw_exported_unit_equivalent_to_1kg_empty_steel_vessel":False,
      "is_physical_technology_equivalent_to_stationary_Type_I_200bar_steel":False,
      "is_native_BAFU_v11_tank_provider_verified":False,
      "can_apply_GWP_to_1kg_PtXFlex_empty_reference_vessel_mass":False,
      "missing_equipment_impact_counted_as_zero":False,
      "source_data_not_republished":True,
      "scientific_interpretation":"Vehicle-transport high-pressure tank recipe including carbon fibre and epoxy, with reference unit kg but source saying per 1 kg H2 capacity. Not valid as mass-based Type I stationary steel tank supplier.",
      "next_verification":"Establish native BAFU v1.1 tank UUID/exchanges and appropriate true stationary-type vessel materials and engineering BOM; only then build compatible foreground LCIA."
    }


def write_tank_audit(original_zip,output):
    path=Path(output)
    if path.exists():raise FileExistsError("do not overwrite source-verified tank provider audit")
    data=inspect_original_bafu_tank(original_zip)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return data


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--original-bafu-v1-ecospold",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    d=write_tank_audit(a.original_bafu_v1_ecospold,a.output)
    print(json.dumps(d,indent=2,sort_keys=True))
