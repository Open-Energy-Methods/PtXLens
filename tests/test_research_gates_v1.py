"""Research programme dependency and scientific-release lock regression tests.

Not a proxy for physical validation; prevents accidentally marking v1.0
released when any mandatory source/physics/LCIA/cost gate remains open.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GATES=ROOT/"research/gates-v1.0.json"
MASTER=ROOT/"docs/PROGRAMME_MASTER_PLAN_v1.0.md"
ADRS=ROOT/"docs/DECISION_REGISTER_v1.0.md"


def test_master_programme_and_original_adrs_exist():
    plan=MASTER.read_text(encoding="utf-8")
    decisions=ADRS.read_text(encoding="utf-8")
    assert "OEM-PTX-2026-01" in plan
    assert "RQ-H2" in plan and "RQ-MeOH" in plan
    assert "ADR-012" in decisions
    assert "P0" in plan and "X2" in plan
    assert "source" in plan.lower() and "uncertainty" in plan.lower()


def test_dependency_dag_and_gates_have_one_owner_and_nonempty_source_status():
    r=json.loads(GATES.read_text(encoding="utf-8"))
    ps=r["work_packages"]
    ids={p["id"] for p in ps}
    assert ids=={"P0","P1","F1","F2","L1","F3","L2","L3","F4","L4","X1","X2"}
    assert len(ps)==len(ids)
    for p in ps:
        assert p["owner"] in {"Both","PtXFlex","PtXLens"}
        assert p["status"] in r["statuses"]
        assert p["current_evidence_status"].strip()
        assert set(p["depends_on"]).issubset(ids-{p["id"]})
        assert p["gate_result"] in ("NOT_PASSED","PASSED")
        if p["gate_result"]=="PASSED":
            assert p["status"]=="verified"
            assert p["acceptance_evidence"] and p["last_scientific_review"] is not None
    by_id={p["id"]:p for p in ps}
    visiting=set()
    visited=set()
    def visit(node):
        if node in visited:return
        assert node not in visiting,"work package dependency cycle"
        visiting.add(node)
        for upstream in by_id[node]["depends_on"]:visit(upstream)
        visiting.remove(node);visited.add(node)
    for node in ids:visit(node)


def test_public_v1_release_is_blocked_until_all_required_scientific_gates_pass():
    data=json.loads(GATES.read_text(encoding="utf-8"))
    pkgs=data["work_packages"]
    core=all(x["gate_result"]=="PASSED" for x in pkgs if x["required_for_hydrogen_core_v1"])
    full=all(x["gate_result"]=="PASSED" for x in pkgs if x["required_for_full_methanol_v1"])
    flags=data["release_readiness"]
    assert flags["hydrogen_core_v1_allowed"] is core
    assert flags["full_methanol_v1_allowed"] is full
    assert flags["latest_verified_scoped_h2_native_lca"] is True
    assert flags["original_historical_E_EplusS_service_matched"] is False
    assert flags["additive_storage_BOM_validated"] is False
    assert flags["independent_scientific_peer_review_passed"] is False
    assert data["source_and_licensing_guardrails"]["authorized_BAFU_2026_v11_raw_inventory_private"] is True
