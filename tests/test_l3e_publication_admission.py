"""L3-E stringent seven-artifact PUBLIC release audit regression.

Reuses ONLY already published source-Git-blob-pinned 2022/24 original annual
integer aggregate and original F2 Type I reference 19-line BOM. Synthetic
copies of freshly regenerated outputs are used to test tamper refusal;
no private hourly vector or manufacturer quote document is loaded.
"""
import json

import pytest

from ptxlens import l3e_publication_admission as m


def populate(tmp_path):
    a=tmp_path/"PtXLens"/"data"/"results"
    b=tmp_path/"PtXFlex"/"data"/"results"
    a.mkdir(parents=True)
    b.mkdir(parents=True)
    for (repo,filename),body in m.artifacts().items():
        p=(a if repo=="PtXLens" else b)/filename
        p.write_text(body,encoding="utf-8",newline="\n")
    return a,b


def test_all_seven_reconstructed_from_both_git_locked_public_source_repos(tmp_path):
    lens,flex=populate(tmp_path)
    r=m.audit(lens,flex)
    assert r["schema_version"]==m.SCHEMA
    files=r["exactly_seven_safe_reconstructed_public_research_reports"]
    assert len(files)==7
    assert len([f for f in files if f["repository"]=="PtXLens"])==6
    assert len([f for f in files if f["repository"]=="PtXFlex"])==1
    assert all(len(f["source_rebuilt_identical_sha256"])==64 for f in files)
    assert r["all_reports_independently_regenerated_from_git_pinned_public_inputs"]
    assert r["real_supplier_quotes_or_price_assumptions_present"] is False
    assert r["native_BAFU_v11_process_and_LCIA_reproduced"] is False
    assert r["real_site_project_NPV_or_environmental_superiority_claimed"] is False
    assert r["git_staging_push_or_private_data_upload_performed"] is False


def test_actual_source_rebuild_holds_unknown_equipment_and_no_GWP():
    files=m.artifacts()
    assert len(files)==7
    economic_name=next(k for k in files if k[1]==m.economic.OUT_JSON)
    hardware_name=next(k for k in files if k[1]==m.hardware.OUT_JSON)
    energy_name=next(k for k in files if k[1]==m.energy.OUT_JSON)
    supplier_name=next(k for k in files if k[1]==m.vendor.OUT)
    e=json.loads(files[economic_name])
    h=json.loads(files[hardware_name])
    o=json.loads(files[energy_name])
    v=json.loads(files[supplier_name])
    assert len(e["two_year_assumption_scenario_grid"])==324
    assert len(h["nineteen_research_equipment_and_evidence_lines"])==19
    assert len(v["nineteen_required_supplier_and_site_intake_lines"])==19
    assert e["manufacturer_supplier_verified_incremental_all_in_CAPEX_eur"] is None
    assert h["native_BAFU_independently_linked_process_and_LCIA_total_GWP_kgCO2e"] is None
    assert v["manufacturer_quote_aggregated_all_in_incremental_installed_CAPEX_eur"] is None
    assert o["yearly"][0]["EplusS_MINUS_E_delta_net_grid_import_MWh"]>0
    assert o["yearly"][1]["EplusS_MINUS_E_delta_net_grid_import_MWh"]<0


@pytest.mark.parametrize("label",[
    "dcf","hardware","energy","supplier"
])
def test_source_rebuild_refuses_falsified_public_outputs(tmp_path,label):
    lens,flex=populate(tmp_path)
    name={
        "dcf":m.economic.OUT_JSON,
        "hardware":m.hardware.OUT_JSON,
        "energy":m.energy.OUT_JSON,
        "supplier":m.vendor.OUT,
    }[label]
    p=(flex if label=="supplier" else lens)/name
    raw=json.loads(p.read_text(encoding="utf-8"))
    raw["fake_signed_manufacturer_cost_eur"]=1.
    p.write_text(json.dumps(raw,sort_keys=True,indent=2),encoding="utf-8",newline="\n")
    with pytest.raises(m.L3EPublicAdmissionError,match="differs byte-for-byte"):
        m.audit(lens,flex)


def test_allows_NO_missing_original_cross_repository_vendor_intake(tmp_path):
    lens,flex=populate(tmp_path)
    (flex/m.vendor.OUT).unlink()
    with pytest.raises(m.L3EPublicAdmissionError,match="missing"):
        m.audit(lens,flex)


def test_reject_windows_crlf_after_checkout_if_sha_integrity_at_risk(tmp_path):
    lens,flex=populate(tmp_path)
    p=lens/m.economic.OUT_MD
    raw=p.read_bytes()
    p.write_bytes(raw.replace(b"\n",b"\r\n"))
    with pytest.raises(m.L3EPublicAdmissionError,match="non-LF"):
        m.audit(lens,flex)


def test_reject_private_annual_source_witness_or_credential_phrase(tmp_path):
    lens,flex=populate(tmp_path)
    p=lens/m.energy.OUT_MD
    p.write_bytes(p.read_bytes()+b"\nPtX_PRIVATE_RESEARCH\n")
    with pytest.raises(m.L3EPublicAdmissionError):
        m.audit(lens,flex)


def test_release_does_not_import_original_private_wind_price_files():
    code=m.__doc__
    assert "Never opens PtX_PRIVATE_RESEARCH" in code
    assert "Does NOT stage, commit or push" in code
    assert "no" in code.lower()
