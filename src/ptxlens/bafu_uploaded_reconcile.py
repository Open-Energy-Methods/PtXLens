"""Independent source-verified BAFU:2026 v1 PEM 30bar LCIA reconstruction.

Consumes the user's *original* EcoSpold v1 ZIP, corrected LCIA workbook, and
original PyNEXUS verified BAFU2026 E/ES source audit. None are included in repo,
copied to CI, or redistributed. Outputs derived results only.

NOTE: The original native v1.1 zolca is a DISTINCT dataset release and must
be checked independently in the actual GreenDelta openLCA 2.7 engine.
"""
from __future__ import annotations
from io import BytesIO
import hashlib
import json
import math
from pathlib import Path
import re
import zipfile
from lxml import etree as ET

REFERENCE="99a1af16-58cd-3f11-a877-c43d3c8e5d78"
CITATION="Life Cycle Inventory database of the Swiss Federal Administration, BAFU:2026"
EPS=2e-7


def corrected_v1_reference(ecospold_zip, corrected_lcia_zip):
    """Exactly reconstruct published reference GWP from ALL SIX tech inputs.

    Energy reference unit in corrected workbook is MJ, but the original
    EcoSpold exchange uses kWh: multiply by 3.6 once and only once.
    """
    with zipfile.ZipFile(ecospold_zip) as z:
        source=next((n for n in z.namelist() if n.endswith("process_"+REFERENCE+".xml")),None)
        if source is None:
            raise ValueError("published BAFU 30bar PEM source UUID missing from original EcoSpold")
        root=ET.fromstring(z.read(source))
    ref=root.find(".//referenceFunction")
    loc=root.find(".//processInformation/geography")
    if ref is None or loc is None or ref.get("unit")!="kg" or ref.get("name")!="Hydrogen production, gaseous, 30 bar, from PEM electrolysis, from grid electricity":
        raise ValueError("original 1kg BAFU30bar PEM source process changed")
    upstream=[]
    for x in root.findall(".//flowData/exchange"):
        g=x.find("inputGroup")
        if g is None or g.text!="5":continue
        upstream.append({
            "name":x.get("name"),"location":x.get("location"),
            "unit":x.get("unit"),"original_output_flow_number":x.get("number"),
            "amount":float(x.get("meanValue"))
        })
    if len(upstream)!=6:
        raise ValueError("unexpected original source upstream input count")
    with zipfile.ZipFile(corrected_lcia_zip) as z:
        path=next((n for n in z.namelist() if n.endswith(".xlsx")),None)
        if path is None:raise ValueError("corrected LCIA workbook missing")
        xlsx=z.read(path)
    requested={f"{x['name']} - {x['location']}" for x in upstream}
    reference_name=f"{ref.get('name')} - {loc.get('location')}"
    requested.add(reference_name)
    matched={}
    with zipfile.ZipFile(BytesIO(xlsx)) as wb:
        shared_xml=ET.fromstring(wb.read("xl/sharedStrings.xml"))
        shared=["".join(x.itertext()) for x in shared_xml.findall("{*}si")]
        with wb.open("xl/worksheets/sheet2.xml") as stream:
            for _,r in ET.iterparse(stream,events=("end",),tag="{*}row"):
                row={}
                for c in r.findall("{*}c"):
                    v=c.find("{*}v")
                    if v is None:continue
                    col=re.match("[A-Z]+",c.get("r")).group(0)
                    if col not in ("A","D","E"):continue
                    row[col]=shared[int(v.text)] if c.get("t")=="s" else v.text
                if row.get("A") in requested:
                    if row["A"] in matched:
                        raise ValueError("duplicate source corrected LCIA product")
                    matched[row["A"]]=row
                r.clear()
                while r.getprevious() is not None:del r.getparent()[0]
    if set(matched)!=requested:
        raise ValueError("required corrected original BAFU source data missing")
    contributions=[]
    for x in upstream:
        p=matched[f"{x['name']} - {x['location']}"]
        unit=p["D"]
        if x["unit"]=="kWh" and unit=="MJ":
            conversion=3.6
        elif (x["unit"],unit) in (("kg","kg"),("p","Item(s)")):
            conversion=1.0
        else:raise ValueError("uncorroborated physical unit conversion")
        factor=float(p["E"])
        if not math.isfinite(factor):raise ValueError("source LCIA factor nonfinite")
        contributions.append({**x,
           "original_corrected_GWP100_kgco2e_per_source_unit":factor,
           "source_factor_unit":unit,
           "physical_conversion_to_source_unit":conversion,
           "reference_input_GWP100_kgco2e_per_kgH2":x["amount"]*conversion*factor})
    source_gwp=float(matched[reference_name]["E"])
    independent=sum(x["reference_input_GWP100_kgco2e_per_kgH2"] for x in contributions)
    if not math.isclose(source_gwp,independent,rel_tol=0,abs_tol=EPS):
        raise ValueError("six direct original BAFU suppliers fail independent corrected LCIA reconstruction")
    electricity=next(x for x in contributions if x["name"]=="Electricity, low voltage, at grid")
    if electricity["amount"]!=54:
        raise ValueError("54kWh/kg original PEM source electricity changed")
    return {
        "schema_version":"ptxlens.uploaded_bafu_v1_corrected_30bar_PEM_reconstruction.v0.1",
        "root_source_uuid":REFERENCE,
        "BAFU_v1_original_source_EcoSpold_sha256":hashlib.sha256(Path(ecospold_zip).read_bytes()).hexdigest(),
        "BAFU_v1_original_corrected_LCIA_zip_sha256":hashlib.sha256(Path(corrected_lcia_zip).read_bytes()).hexdigest(),
        "source_citation":CITATION,
        "source_reference":reference_name,
        "original_corrected_IPCC_2021_GWP100_kgCO2e_per_kgH2":source_gwp,
        "sum_six_original_supplier_GWP100_kgCO2e_per_kgH2":independent,
        "reconstruction_absolute_difference":abs(source_gwp-independent),
        "reference_54kWh_CH_electricity_component_kgCO2e_per_kgH2":electricity["reference_input_GWP100_kgco2e_per_kgH2"],
        "reference_non_direct_operational_electricity_component_kgCO2e_per_kgH2":(
            source_gwp-electricity["reference_input_GWP100_kgco2e_per_kgH2"]),
        "six_original_input_supplier_contributions":contributions,
        "source_BAFU_v11_native_equivalence_not_assumed":True,
        "native_2023_Dutch_product_system_calculated":False
    }


def reconcile_original_dispatch(ecospold_zip,corrected_lcia_zip,original_E_ES_result_zip,output):
    p=Path(output)
    if p.exists():raise FileExistsError("refusing overwrite of scientific result")
    reference=corrected_v1_reference(ecospold_zip,corrected_lcia_zip)
    with zipfile.ZipFile(original_E_ES_result_zip) as z:
        raw=z.read("2023_original_E_vs_ES_BAFU2026_method_sensitivity.json")
    model=json.loads(raw)
    if model.get("published_version")!="BAFU:2026 v1":
        raise ValueError("source-screen BAFU edition mismatch")
    scenarios={}
    non_electric=reference["reference_non_direct_operational_electricity_component_kgCO2e_per_kgH2"]
    for name in ("E","E_plus_S"):
        row=model[name]
        if row["full_product_system_LCA_claim_allowed"] is not False:
            raise ValueError("source E/ES model falsely labelled complete")
        electricity=row["BAFU_energy_supply_intensity_kgco2e_per_kg_model_delivered_H2"]
        scenarios[name]={
            "original_2023_model_dispatch_SHA":row["original_source_archive_sha256"],
            "2023_modelled_delivered_hydrogen_kg":row["historical_2023_modelled_H2_delivered_kg"],
            "BAFU_2026_electricity_supply_only_kgco2e_per_kgH2":electricity,
            "retained_BAFU_original_30bar_non_direct_electricity_kgco2e_per_kgH2":non_electric,
            "illustrative_direct_electricity_substituted_reference_kgco2e_per_kgH2":electricity+non_electric,
            "E_plus_S_added_hydrogen_storage_equipment_included":False,
            "is_native_2023_Dutch_LCIA":False,
            "is_full_cradle_to_gate_2023_Dutch_hydrogen_LCA":False
        }
    report={
        "schema_version":"ptxlens.uploaded_BAFU_v1_corrected_stoichiometric_reference_and_2023_sensitivity.v0.1",
        "reference":reference,
        "scenarios":scenarios,
        "physical_quality_note":"Corrected v1 source factors, source-v1 unit exchanges and original modeled 2023 Dutch electricity; 2026 background technology and 30bar Swiss original non-electric sources retained unchanged.",
        "not_included":["E+S incremental H2 storage BOM, compressors and losses",
                        "2023 matching operational electricity technology, 2026 impact-method background source age",
                        "Native BAFU v1.1 reparameterized product system, matched product service"],
        "full_cradle_to_gate_claim":False
    }
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return report
