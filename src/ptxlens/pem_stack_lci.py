"""Real published PEM stack material LCI transcribed from Kanz (TU/e, 2024).

Not an impact result: supplier processes, BOP, exact technology matching and
other lifecycle stages remain unlinked. Do not inject CO2e factors or silently
substitute proprietary GaBi/ecoinvent provider data.
"""
import json
import math
from pathlib import Path

from .observed import load_archive


def inventory_reference(source_file):
    p=Path(source_file)
    model=json.loads(p.read_text(encoding="utf-8"))
    if model.get("schema_version") != "ptxlens.published_pem_stack_inventory.v0.1":
        raise ValueError("unknown PEM LCI model/source register")
    if model.get("reference_stack_rated_power_mw")!=1:
        raise ValueError("expected literature reference 1 MW PEM stack")
    records=model.get("materials",[])
    if len(records)!=8 or len({x["name"] for x in records})!=8:
        raise ValueError("unrecognized published 1 MW inventory")
    for record in records:
        if (record["unit"]!="kg" or
            not math.isfinite(record["kg_per_1mw_stack"]) or
            record["kg_per_1mw_stack"]<=0 or
            not record.get("provider_lci_name") or
            record.get("reference_region") not in ("Europe","Global")):
            raise ValueError("material units, source region or providers invalid")
    return model


def scenario_foreground(source_archive, published_lci_json, *,
                        stack_operating_life_hours=40000, study_years=30):
    """Provisional stack-MASS flows per kg model-delivered H2 under declared extrapolation.

    Study_years repeated original 2023 operation is a **hypothetical future
    allocation**. Stack materials are real published quantities but not
    demonstrated hardware inventory of this actual hypothetical model.
    """
    if (stack_operating_life_hours!=40000 or study_years!=30):
        raise ValueError("currently pinned to DOE 2024 40000h stack and 30y project")
    source=load_archive(source_archive)
    literature=inventory_reference(published_lci_json)
    hours=source["online_hours"]
    capacity=source["electrolyser_capacity_mw"]
    delivered=source["annual_delivered_h2_kg"]
    if hours<=0 or capacity<=0 or delivered<=0:
        raise ValueError("invalid source operating history")
    total_operating_hours=study_years*hours
    # One physical stack at time zero + a new stack whenever another life
    # interval starts before final operating-hour service is complete.
    stack_cycles=math.ceil(total_operating_hours/stack_operating_life_hours)
    modeled_total_h2=study_years*delivered
    if stack_cycles < 1:
        raise ValueError("expected one or more modeled stack services")
    material=[]
    for item in literature["materials"]:
        initial_mass=item["kg_per_1mw_stack"]*capacity
        replaced_mass=initial_mass*(stack_cycles-1)
        total=initial_mass+replaced_mass
        material.append({
            "provider_description":item["provider_lci_name"],
            "provider_region_of_study":item["reference_region"],
            "unit":"kg",
            "stack_reference_1mw_material_kg":item["kg_per_1mw_stack"],
            "initial_125mw_plant_equivalent_mass_kg":initial_mass,
            "replacement_stacks_mass_kg":replaced_mass,
            "assumed_total_lifecycle_input_mass_kg":total,
            "scenario_mass_kg_per_kg_model_delivered_h2":total/modeled_total_h2,
            "provider_product_flow_id":None,
            "provider_process_id":None,
            "lcia_gwp100_kgco2e":None,
            "method_status":"INPUT MATERIAL INVENTORY ONLY; NO LINKED PROVIDER",
        })
    return {
        "schema_version":"ptxlens.published_pem_foreground_scenario.v0.1",
        "scenario":source["scenario"],"source_archive_sha256":source["archive_sha256"],
        "literature_reference":literature["source"],
        "reference_technology":"literature PEM STACK, 1MW per module",
        "derived_model_capacity_mw":capacity,
        "assumed_linear_module_count":capacity,
        "observed_input_model_2023_online_hours":hours,
        "assumed_study_lifetime_years":study_years,
        "assumed_stack_replacement_interval_operating_hours":stack_operating_life_hours,
        "assumed_stack_service_cycles_in_30_years":stack_cycles,
        "hypothetical_total_delivered_h2_kg_over_study_years":modeled_total_h2,
        "water_foreground_inventory_litres_per_kg_h2_low":9.0,
        "water_foreground_inventory_litres_per_kg_h2_high":10.0,
        "lifecycle_material_inputs":material,
        "climate_result":None,
        "can_claim_cradle_to_gate_lca":False,
        "critical_limitations":[
            "Study source model is PEM stack 1MW; PyNEXUS model is generic simplified electrolyser. Hardware technology assumed, not verified",
            "Scaling identical 1MW stacks linearly to nameplate 125MW is a scenario extrapolation, not observed installed materials",
            "Repeated 2023 modeled hydrogen over 30 years is a scenario, not observed 30-year process operation",
            "No mapped openLCA provider UUIDs or GWP LCIA method. This is a REAL published material mass INVENTORY, not emissions",
            "DOE 40k hours is an economic-replacement assumption; not validated against TU Eindhoven 2024 stack wear/replacement model",
            "BoP, storage, compression, water-treatment unit-process inventories and end-of-life impacts unresolved",
        ],
    }


def write_foreground(archive, source_lci, output_file):
    dest=Path(output_file)
    if dest.exists():
        raise FileExistsError("refusing to overwrite existing material LCI")
    data=scenario_foreground(archive,source_lci)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
    return data
