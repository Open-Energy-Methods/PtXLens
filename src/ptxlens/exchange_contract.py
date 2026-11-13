"""Scientific and structural validation of the shared PtXFlex / PtXLens exchange.

This module enforces cross-field scientific facts JSON Schema cannot represent:
unknown != 0, physical tank capacity != equipment mass, and an unmatched
historical case is NOT a matched-service comparative LCA. The structural
schema is exact-byte mirrored between research repositories.

This is NOT a calculator, solver, LCA engine or source-data provider.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA=Path(__file__).resolve().parents[2] / "contracts" / "ptx-exchange-v1.schema.json"
KNOWN_2023_ORIGINAL={
    "E":"069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051",
    "E_plus_S":"cd4101fe62c3f1b8aa2d7508d3651d2fee40d2bafe6d5b87e40d5f4d055070f9",
}
KNOWN_2023_INPUT_SHA256={
    "market_price_input_sha256":"2dfea4651fce314893201e7b08a4ae0ad24deef6b69ef85d81d9f54428f95bb2",
    "wind_available_input_sha256":"a1c1443c49fa700d57038e008abd99f89c85d87e56a0fbd6141af37215e25520",
    "hourly_demand_input_sha256":"1d35b2a2091a14998c3936819dac4edac0675319bd5b63553944c61a41943cd4",
}
NATIVE_METHOD="IPCC 2021"
NATIVE_CATEGORY="IPCC 2021 GWP 100"


class ScientificContractError(ValueError):
    """A physically/environmentally inconsistent cross-repo research claim."""


def schema():
    loaded=json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(loaded)
    return loaded


def validate_exchange(data):
    """Return the original document unaltered or raise a scientific gate error."""
    if not isinstance(data,dict):
        raise ScientificContractError("exchange must be a JSON object")
    errors=sorted(Draft202012Validator(schema()).iter_errors(data),
                  key=lambda e:list(map(str,e.absolute_path)))
    if errors:
        e=errors[0]
        raise ScientificContractError("schema: "+".".join(map(str,e.absolute_path))+": "+e.message)
    scenario=data["scenario_id"]
    src=data["source"]
    fu=data["functional_unit"]
    storage=data["storage"]
    impact=data["impact"]
    cost=data["economics"]
    claims=data["claims"]
    flows=data["annual_flows"]
    def fail(message):
        raise ScientificContractError(message)

    if src["source_kind"]=="synthetic_test":
        if data["evidence_status"]!="literature_parameterized_scenario":
            fail("synthetic input cannot be labelled observed or source-reconstructed LCA")
        if claims["native_lca_executed"] or claims["industrial_validation"]:
            fail("synthetic inputs cannot assert real native LCA or plant validation")
    if src["source_kind"]=="observed_weather_market_plus_modelled_hydrogen":
        if claims["original_study_observed_plant"] or claims["industrial_validation"]:
            fail("original PyNEXUS hydrogen is modelled, not observed plant telemetry")
        if scenario in KNOWN_2023_ORIGINAL and src["original_source_archive_sha256"]!=KNOWN_2023_ORIGINAL[scenario]:
            fail("known 2023 historical source archive SHA mismatch")
        if src["source_year"]!=2023 or src["hour_count"]!=8760:
            fail("original 2023 NL source must have exactly 8760 hours")
        if scenario in KNOWN_2023_ORIGINAL:
            for name,pinned in KNOWN_2023_INPUT_SHA256.items():
                if src[name]!=pinned:
                    fail("verified frozen PyNEXUS 2023 price/weather/demand series SHA mismatch: "+name)
    if data["evidence_status"]=="external_plant_validated" and not claims["industrial_validation"]:
        fail("external plant validation requires independent measurements and evidence")
    if claims["industrial_validation"] and data["evidence_status"]!="external_plant_validated":
        fail("industrial_validation cannot be true for unmeasured or modelled operation")

    rated=storage["rated_h2_capacity_kg"]
    usable=storage["usable_h2_capacity_kg"]
    if usable is not None and usable>rated+1e-9:
        fail("usable hydrogen mass cannot exceed rated capacity")
    pmin,pmax=storage["minimum_pressure_bar"],storage["maximum_pressure_bar"]
    if (pmin is None)!=(pmax is None):
        fail("pressure bounds must both be known or both remain null")
    if pmin is not None and pmax<=pmin:
        fail("maximum pressure must exceed minimum storage pressure")
    mass=storage["empty_equipment_mass_kg"]
    status=storage["equipment_mass_source_status"]
    if status=="verified_engineering_BOM" and (mass is None or mass<=0 or not storage["physical_vessel_design_source"]):
        fail("verified equipment mass requires positive vessel mass and real design citation")
    if status=="missing" and mass is not None:
        fail("a missing equipment design cannot declare a tank equipment mass")
    if status=="missing" and claims["matched_service_comparison_eligible"]:
        fail("comparison cannot be research-complete with unknown storage equipment")
    if rated>0 and fu["product"]=="H2" and mass==rated and status=="missing":
        fail("H2 stored capacity was inappropriately mapped to tank equipment mass")

    if fu["product"]=="H2":
        if data["research_question"]!="H2_storage":
            fail("H2 gate must use H2 research-question scope")
        if flows["methanol_delivered_kg"] not in (None,0) or flows["co2_feed_kg"] not in (None,0):
            fail("H2 functional unit cannot contain methanol synthesis as unlabeled output")
    else:
        if data["research_question"]!="CO2_to_methanol":
            fail("MeOH functional unit must use methanol research-question scope")
        if flows["methanol_delivered_kg"] in (None,0) or flows["co2_feed_kg"] in (None,0):
            fail("methanol study requires nonzero specified product and CO2 feed")
    if claims["matched_operational_service_verified"]:
        if not fu["same_service_as_comparator"] or fu["service_profile_sha256"] is None:
            fail("operational matched service requires a named identical profile SHA")
        if fu["pressure_bar"] is None or fu["purity_mol_fraction"] is None or not fu.get("quality_verified",False):
            fail("operational matched service requires verified product pressure and purity")
        if data["analysis_scope"] not in ("matched_service_h2","methanol_validated"):
            fail("unmatched historical source cannot be relabelled operationally matched")
        for required in ("market_price_input_sha256","wind_available_input_sha256","hourly_demand_input_sha256"):
            if src[required] is None:
                fail("matched operations require identical source price/weather/demand hashes: "+required)
    if claims["matched_service_comparison_eligible"] and not claims["matched_operational_service_verified"]:
        fail("complete environmental comparison requires first verifying matched operating service")

    native=claims["native_lca_executed"]
    if native:
        if impact["gwp100_kgco2e_per_product_kg"] is None:
            fail("a native LCA executed claim needs an actual source-verified result")
        if impact["source_database"]!="BAFU" or impact["source_database_version"]!="2026 v1.1":
            fail("current native result requires exact licensed BAFU 2026 v1.1 edition")
        if impact["method"]!=NATIVE_METHOD or impact["category"]!=NATIVE_CATEGORY:
            fail("must use exact native IPCC 2021 GWP 100 impact category")
        if impact["unlinked_material_product_inputs"] is None:
            fail("native LCA result must report link completeness")
        if impact["impact_status"] not in ("scoped_native_lcia","full_boundary_candidate","reviewed_full_boundary"):
            fail("native source claim inconsistent with impact status")
    if impact["full_plant_boundary"]:
        if impact["impact_status"] not in ("full_boundary_candidate","reviewed_full_boundary"):
            fail("full boundary cannot be a partial electricity/native reference result")
        if storage["equipment_mass_source_status"]!="verified_engineering_BOM":
            fail("full E/E+S footprint requires validated storage equipment BOM")
        if storage["storage_electricity_kwh"] is None or storage["inventory_losses_kg"] is None:
            fail("full product boundary requires compression and leakage ledger")
        if impact["unlinked_material_product_inputs"]!=0 or not impact["incremental_h2_storage_equipment_included"]:
            fail("full boundary requires closed providers and included incremental storage equipment")
    if impact["impact_status"]=="reviewed_full_boundary" and not impact["full_plant_boundary"]:
        fail("reviewed full boundary status cannot exclude a material process")

    if cost["cost_model_status"] in ("full_DCF_candidate","reviewed_full_DCF"):
        if cost["full_levelized_cost_per_delivered_kg"] is None or cost["currency"] is None or cost["price_year"] is None or cost["discount_rate_fraction"] is None:
            fail("full TEA requires actual discounted cost and coherent currency/year and discount assumptions")
    else:
        if cost["full_levelized_cost_per_delivered_kg"] is not None:
            fail("capital/partial cost must not be reported as full LCOH or LCOM")
    if claims["comparative_superiority_claim"]:
        fail("unreviewed comparative environmental superiority claims not permitted in v1.0 exchange")
    if claims["matched_service_comparison_eligible"] and not impact["full_plant_boundary"]:
        fail("matched complete environmental comparison requires the full relevant plant boundary")
    if src["source_kind"]!="synthetic_test" and not src["native_source_license_reviewed"]:
        fail("source licensing status must be reviewed before sharing")
    return data


def comparable_pair(a,b,*,domain="environmental"):
    """Check identical physical service separately from complete environmental TEA/LCA.

    Operational comparison can legitimately precede full equipment LCIA.
    Environmental comparison additionally requires complete system boundary
    and comparable financial/LCA sources. No unsupported source data are added.
    """
    validate_exchange(a);validate_exchange(b)
    if domain not in ("operational","environmental"):
        raise ScientificContractError("comparison domain must be operational or environmental")
    if {a["scenario_id"],b["scenario_id"]}!={"E","E_plus_S"}:
        raise ScientificContractError("require original E vs E+S pair")
    for d in (a,b):
        if d["analysis_scope"]!="matched_service_h2" or not d["claims"]["matched_operational_service_verified"]:
            raise ScientificContractError("pair is not explicitly validated for equal operating H2 service")
        if domain=="environmental" and not d["claims"]["matched_service_comparison_eligible"]:
            raise ScientificContractError("complete environmental comparison claim has not passed lifecycle gates")
    keys=("product","unit","gate_name","pressure_bar","purity_mol_fraction","service_profile_sha256")
    for k in keys:
        if a["functional_unit"][k]!=b["functional_unit"][k]:
            raise ScientificContractError("different product-gate or hourly service: "+k)
    for k in ("source_year","hour_count","market_price_input_sha256","wind_available_input_sha256","hourly_demand_input_sha256"):
        if a["source"][k]!=b["source"][k]:
            raise ScientificContractError("different source time series or demand: "+k)
    if domain=="environmental":
        for k in ("source_database","source_database_version","method","category"):
            if a["impact"][k]!=b["impact"][k]:
                raise ScientificContractError("environmental method/background not comparable: "+k)
        for k in ("currency","price_year","discount_rate_fraction"):
            if a["economics"][k]!=b["economics"][k]:
                raise ScientificContractError("cost basis not comparable: "+k)
    return True
