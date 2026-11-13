"""Registered, fail-closed PtXFlex F3 2023 pressure-adequacy evidence bridge.

Source is the six-input, ZIP-digest-verified upstream reconciliation. It is
source-based MODELLING, not a physical plant or an equipment-complete BAFU LCA.
No numeric lifecycle result is estimated from annual H2 shortage.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

F3_PATH = Path(__file__).resolve().parents[2]/"data/results/F3_2023_reconciled_research_evidence.json"
F3_DERIVED_SHA256 = "5dead18cfa0c3fecf15562f423e01044bcc6ad4ba4f5212dfb44a010b0d1a0d3"
E_SOURCE_SHA256 = "069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051"
ES_SOURCE_SHA256 = "cd4101fe62c3f1b8aa2d7508d3651d2fee40d2bafe6d5b87e40d5f4d055070f9"


class ReconciledF3EvidenceError(ValueError):
    pass


def read_verified_f3_evidence(path=F3_PATH):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != F3_DERIVED_SHA256:
        raise ReconciledF3EvidenceError("registered original 2023 F3 derived JSON SHA-256 changed")
    d = json.loads(raw)
    if d.get("schema_version") != "ptxflex.f3_2023_pressure_adequacy_reconciled.v1":
        raise ReconciledF3EvidenceError("unregistered F3 research schema")
    if d.get("source_original_E_zip_sha256") != E_SOURCE_SHA256 or d.get("source_original_EplusS_zip_sha256") != ES_SOURCE_SHA256:
        raise ReconciledF3EvidenceError("original source frozen ZIP identity mismatch")
    if (d.get("laboratory_or_vendor_equipment_validation") is not False
            or d.get("full_system_native_BAFU_GWP_or_TEA_available") is not False
            or d.get("matched_service_E_vs_EplusS_LCA_or_TEA_comparison_eligible") is not False
            or d.get("pressure_screen_research_only") is not True):
        raise ReconciledF3EvidenceError("unsupported LCA/TEA or installation validation inference")
    ref = d.get("reference_E_delivered_hourly_target_total_kg")
    full = d.get("full_original_2023_demand_total_kg")
    if ref is None or full is None or abs(ref-16335279.317376737)>.002 or abs(full-18250000.)>.002:
        raise ReconciledF3EvidenceError("full/yearly reference source H2 service mismatch")
    if abs((full-ref)-d.get("original_E_modelled_source_shortfall_before_pressure_kg",float("nan")))>.002:
        raise ReconciledF3EvidenceError("preexisting original full-demand shortfall changed")
    for mode in ("max_inventory","usable_service"):
        rec=d.get("modes",{}).get(mode)
        if not isinstance(rec,dict) or rec.get("eligible_for_direct_20t_vs_40t_cost_or_GWP_comparison") is not False:
            raise ReconciledF3EvidenceError("unregistered capacity scenario service status")
        if rec.get("mathematically_proven_unequal_delivery_service") is not True:
            raise ReconciledF3EvidenceError("unequal source service was silently set to matched")
        E=rec.get("cases",{}).get("E",{})
        ES=rec.get("cases",{}).get("E_plus_S",{})
        for case,x in (("E",E),("E_plus_S",ES)):
            lo=x.get("minimum_additional_modelled_H2_shortfall_lower_bound_kg")
            hi=x.get("minimum_additional_modelled_H2_shortfall_upper_bound_kg")
            if not all(isinstance(t,(int,float)) and not isinstance(t,bool) and math.isfinite(t) for t in (lo,hi)):
                raise ReconciledF3EvidenceError("nonfinite pressure-screen source shortage interval")
            if lo < 0 or hi < 0 or lo>hi+.01 or hi>ref+.01:
                raise ReconciledF3EvidenceError("impossible F3 original source shortage bounds")
            for result in ("native_full_plant_GWP_kgCO2e","complete_project_annual_cost_eur"):
                if result not in x or x[result] is not None:
                    raise ReconciledF3EvidenceError("cost/GWP manufactured from source-adequacy evidence")
            if abs(x.get("original_full_demand_shortfall_lower_bound_kg",float("nan"))-(full-ref+lo))>.002:
                raise ReconciledF3EvidenceError("full source demand shortfall lower closure failed")
            if abs(x.get("original_full_demand_shortfall_upper_bound_kg",float("nan"))-(full-ref+hi))>.002:
                raise ReconciledF3EvidenceError("full source demand shortfall upper closure failed")
        if not (E["minimum_additional_modelled_H2_shortfall_lower_bound_kg"]>.01
                and E["minimum_positive_shortfall_proven"] is True
                and E["zero_shortfall_feasible_and_optimal_proven"] is False
                and ES["minimum_additional_modelled_H2_shortfall_upper_bound_kg"]==0
                and ES["zero_shortfall_feasible_and_optimal_proven"] is True):
            raise ReconciledF3EvidenceError("40t zero-service witness or 20t positive deficit not preserved")
    if set(d.get("stageA_certificate_input_sha256",{})) != {
            "max_inventory_E","max_inventory_E_plus_S","usable_service_E","usable_service_E_plus_S"}:
        raise ReconciledF3EvidenceError("missing historical Stage A artifacts")
    if set(d.get("independent_full_service_witness_sha256",{})) != {"max_inventory","usable_service"}:
        raise ReconciledF3EvidenceError("missing independent full-service witness artifacts")
    return d


def comparative_lca_gate():
    """A study-ready declaration; zero is never imputed for missing LCA."""
    d=read_verified_f3_evidence()
    return {
        "programme":"OEM-PTX-2026-01",
        "study":"2023 original E vs E+S, real-gas Type I pressure screen",
        "source_reconciled_report_sha256":F3_DERIVED_SHA256,
        "source_20t_additional_shortfall_minimum_positive_proven":True,
        "source_40t_additional_shortfall_minimum_zero_proven":True,
        "same_hourly_delivered_service_achieved_in_both":False,
        "system_native_manufacturing_GWP_kgCO2e":None,
        "full_system_LCOH_EUR_kg":None,
        "direct_comparative_environmental_or_financial_claim_allowed":False,
        "next_scientific_dependency":"Sourced common-service backup or new equal-service dispatch + pressure-compatible equipment BOM/providers",
    }
