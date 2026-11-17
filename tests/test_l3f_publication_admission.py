"""L3-F source-rebuilt eight public research files and negative release tests."""
import json
import pytest

from ptxlens import l3f_publication_admission as m


def staged_fixture(tmp_path):
    lens=tmp_path/"PtXLens"/"data"/"results"
    flex=tmp_path/"PtXFlex"/"data"/"results"
    lens.mkdir(parents=True)
    flex.mkdir(parents=True)
    for (repo,name),body in m.reconstruct().items():
        path=(lens if repo=="PtXLens" else flex)/name
        path.write_text(body,encoding="utf-8",newline="\n")
    return lens,flex


def test_eight_outputs_exactly_include_pressure_site_finance_and_BAFU(tmp_path):
    lens,flex=staged_fixture(tmp_path)
    r=m.audit(lens_results=lens,flex_results=flex)
    assert len(r["exactly_eight_public_safe_research_reports"])==8
    assert len([x for x in r["exactly_eight_public_safe_research_reports"]
                if x["repo"]=="PtXFlex"])==4
    assert len([x for x in r["exactly_eight_public_safe_research_reports"]
                if x["repo"]=="PtXLens"])==4
    assert all(len(x["SHA256_exact_original_source_rebuilt"])==64
               for x in r["exactly_eight_public_safe_research_reports"])
    assert r["OEM_PED_site_pressure_vessels_qualified"] is False
    assert r["authentic_supplier_installed_price_verified"] is False
    assert r["native_BAFU_2026_v11_process_system_and_LCIA_replayed"] is False
    assert r["environmental_superiority_or_NPV_certified"] is False
    assert r["git_add_or_commit_or_push_performed"] is False


def test_original_F2_19lines_and_distinct_gross_usable_in_all_reports():
    source=m.reconstruct()
    a=json.loads(source[("PtXFlex",m.thermal.OUT_JSON)])
    b=json.loads(source[("PtXFlex",m.site.OUT_JSON)])
    c=json.loads(source[("PtXLens",m.costs.OUT_JSON)])
    d=json.loads(source[("PtXLens",m.bafu.OUT_JSON)])
    assert a["origin"]["extra_gross_H2_at_maximum_kg"]==20000.
    assert a["origin"]["original_pressure_swing_extra_withdrawable_H2_kg"]==pytest.approx(17784.924849614785)
    assert b["model_pressure_high_BAR_ABSOLUTE_NOT_automatic_PED_gauge_MAWP"]==200.
    assert len(b["original_19_equipment_qualification_lines"])==19
    assert len(c["nineteen_site_verified_supplier_installed_scope_lines"])==19
    assert len(d["separate_19_manufacturer_and_provider_flow_requirements"])==19
    assert d["source_empty_equipment_1924800kg_NOT_virgin_steel_or_procurement"]
    assert d["original_native_BAFU_2026_v11_incremental_total_kgCO2e"] is None


@pytest.mark.parametrize("repo,name",[
    ("PtXFlex",m.thermal.OUT_JSON),
    ("PtXFlex",m.site.OUT_MD),
    ("PtXLens",m.costs.OUT_JSON),
    ("PtXLens",m.bafu.OUT_JSON),
])
def test_changed_staged_source_F2_or_published_cost_file_rejected(tmp_path,repo,name):
    lens,flex=staged_fixture(tmp_path)
    path=(lens if repo=="PtXLens" else flex)/name
    path.write_bytes(path.read_bytes()+b"\nUNSUPPORTED PUBLIC IMPACT\n")
    with pytest.raises(m.L3FAdmissionError,match="differs"):
        m.audit(lens_results=lens,flex_results=flex)


def test_private_data_marker_rejected_by_exact_source_audit(tmp_path):
    lens,flex=staged_fixture(tmp_path)
    path=lens/m.bafu.OUT_MD
    path.write_bytes(path.read_bytes()+b"PtX_PRIVATE_RESEARCH\n")
    with pytest.raises(m.L3FAdmissionError):
        m.audit(lens_results=lens,flex_results=flex)


def test_Windows_CRLF_of_source_locked_file_rejected(tmp_path):
    lens,flex=staged_fixture(tmp_path)
    path=flex/m.thermal.OUT_MD
    path.write_bytes(path.read_bytes().replace(b"\n",b"\r\n"))
    with pytest.raises(m.L3FAdmissionError,match="non-LF"):
        m.audit(lens_results=lens,flex_results=flex)


def test_missing_any_OEM_PED_site_requirement_file_rejected(tmp_path):
    lens,flex=staged_fixture(tmp_path)
    (flex/m.site.OUT_JSON).unlink()
    with pytest.raises(m.L3FAdmissionError,match="missing"):
        m.audit(lens_results=lens,flex_results=flex)
