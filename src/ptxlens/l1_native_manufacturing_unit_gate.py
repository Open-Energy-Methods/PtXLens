"""Dimensional admission check for native LCI supplier functional units.

No provider data or environmental factors are bundled. Passing this structural
check does not demonstrate compatible manufacturing processes or full LCA.
"""
from __future__ import annotations
from collections.abc import Mapping
from math import isfinite

# Deliberately distinguish H2 gas capacity from empty equipment mass.
SUPPORTED_DENOMINATORS = frozenset({
    "kg_empty_equipment", "unit_vessel", "kg_h2_nominal_capacity",
    "kg_steel_input", "m3_vessel_free_volume",
})

def audit_manufacturing_functional_unit(
    record: Mapping, *, required_denominator: str = "kg_empty_equipment"
) -> dict:
    """Fail closed on incompatible or unsupported inventory reference flows.

    A native provider per kg nominal H2 capacity is not a per kg empty steel
    vessel manufacturing process. No physical conversion is inferred.
    """
    findings = []
    if not isinstance(record, Mapping):
        return {"passed": False, "findings": ["inventory record is not a mapping"],
                "claim_scope": "dimensional compatibility screening only"}
    provider = record.get("provider_id")
    if not isinstance(provider, str) or not provider.strip():
        findings.append("missing native provider identifier")
    source_hash = record.get("source_sha256")
    if not isinstance(source_hash, str) or len(source_hash) != 64 or any(
        c not in "0123456789abcdef" for c in source_hash
    ):
        findings.append("missing/invalid lowercase SHA-256 source provenance")
    denominator = record.get("reference_flow_denominator")
    if denominator not in SUPPORTED_DENOMINATORS:
        findings.append("unknown inventory reference-flow denominator")
    if required_denominator not in SUPPORTED_DENOMINATORS:
        findings.append("unknown requested functional-unit denominator")
    elif denominator != required_denominator:
        findings.append("incompatible functional-unit denominator: no inferred conversion")
    amount = record.get("reference_flow_amount")
    if isinstance(amount, bool) or not isinstance(amount, (int, float)) or not isfinite(amount) or amount <= 0:
        findings.append("invalid reference-flow amount")
    if record.get("manufacturing_process_scope") != "stationary_type_i_steel_vessel_manufacturing":
        findings.append("manufacturing process scope not established for stationary Type I vessel")
    return {"passed": not findings, "findings": findings,
            "claim_scope": "dimensional compatibility screening only; not native LCIA, certification, or provider verification"}
