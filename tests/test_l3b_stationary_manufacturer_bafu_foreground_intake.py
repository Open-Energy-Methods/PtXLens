"""L3-B supplier evidence intake, engineering pressure and native BAFU reject tests."""
import copy
import hashlib
import json
import pytest

import ptxlens.l3b_stationary_manufacturer_bafu_foreground_intake as m


@pytest.mark.parametrize("mode,count",[
    ("max_inventory",802),("usable_service",902)
])
def test_frozen_2023_stationary_typeI_independent_BOM_questionnaire(mode,count):
    q=m.blank_source_questionnaire(mode)
    assert q["schema_version"]==m.SCHEMA
    assert q["source_F2_original_BOM_SHA256"]==m.SOURCE_SHA256
    assert len(q["lines"])==19
    assert {x["line_id"] for x in q["lines"]}==m.EXPECTED_DOC_BOM
    vessel=q["lines"][0]
    assert vessel["line_id"]=="typeI_200bar_bare_reference_vessels"
    assert vessel["reference_paper_discrete_vessel_count_not_OEM_quote"]==count
    assert vessel["OEM_foreground"]["raw_input_material_bill_kg_by_grade"] is None
    assert vessel["supplier_quote"]["net_price_excl_tax"] is None
    assert q["reference_paper_2400kg_per_empty_vessel_not_raw_steel_kg"] is True


def test_unpopulated_supplier_evidence_audit_blocks_complete_LCA_and_EUR(tmp_path):
    out=m.validate_private_evidence(m.blank_source_questionnaire("usable_service"),tmp_path)
    assert out["source_scope_lines"]==19
    assert out["OEM_primary_documents_verifiably_retained_private"]==0
    assert out["supplier_quotations_with_currency_year_and_scope"]==0
    assert out["OEM_grade_specific_raw_material_BOM_lines"]==0
    assert out["native_BAFU_process_mapping_locally_reviewed_lines"]==0
    assert out["full_L3_B_economic_and_environmental_release_ALLOWED"] is False
    assert out["native_BAFU_2026_stationary_typeI_whole_plant_LCIA_ACTUALLY_executed"] is False


def add_private_vessel_source(q,root,*,unit="bar_gauge",rating=200.0):
    original=b"FAKE DATASHEET - SYNTHETIC TEST FIXTURE NO REAL MANUFACTURER"
    filename="test_only_manufacturer.pdf"
    (root/filename).write_bytes(original)
    sha=hashlib.sha256(original).hexdigest()
    line=q["lines"][0]
    line["scope_status"]="OEM_DATASHEET_ONLY"
    line["supplier_name"]="TEST_ONLY_NOT_A_VENDOR"
    line["vendor_model_and_revision"]="TEST_ONLY_0"
    line["source_doc_private_relative_path"]=filename
    line["source_doc_sha256"]=sha
    line["engineering_qualification"].update({
      "rated_pressure_value":rating,
      "rated_pressure_unit":unit,
      "PED_stationary_installation_documented":True,
      "hydrogen_compatibility_documented":True,
    })
    return line


def test_private_datasheet_sha_and_200bara_vs_barg_conversion(tmp_path):
    q=m.blank_source_questionnaire("max_inventory")
    row=add_private_vessel_source(q,tmp_path)
    out=m.validate_private_evidence(q,tmp_path)
    assert out["OEM_primary_documents_verifiably_retained_private"]==1
    assert out["supplier_quotations_with_currency_year_and_scope"]==0
    assert out["full_L3_B_economic_and_environmental_release_ALLOWED"] is False
    row["engineering_qualification"]["rated_pressure_value"]=199.0
    row["engineering_qualification"]["rated_pressure_unit"]="bar_absolute"
    with pytest.raises(m.StationarySourceEvidenceError,match="design rating"):
        m.validate_private_evidence(q,tmp_path)
    row["engineering_qualification"]["rated_pressure_unit"]="bar_gauge"
    assert m.validate_private_evidence(q,tmp_path)["OEM_primary_documents_verifiably_retained_private"]==1


def test_vendor_source_mutation_and_unknown_class_fail_closed(tmp_path):
    q=m.blank_source_questionnaire("usable_service")
    v=add_private_vessel_source(q,tmp_path)
    v["source_doc_sha256"]="0"*63+"1"
    with pytest.raises(m.StationarySourceEvidenceError,match="hash mismatch"):
        m.validate_private_evidence(q,tmp_path)
    q=m.blank_source_questionnaire("usable_service")
    q["lines"][0]["line_id"]="vehicle_composite_storage_tank"
    with pytest.raises(m.StationarySourceEvidenceError,match="exact 19-line"):
        m.validate_private_evidence(q,tmp_path)


def test_no_vendor_data_confuses_source_reference_mass_with_raw_steel(tmp_path):
    q=m.blank_source_questionnaire("max_inventory")
    q["reference_paper_2400kg_per_empty_vessel_not_raw_steel_kg"]=False
    with pytest.raises(m.StationarySourceEvidenceError,match="raw-steel accounting"):
        m.validate_private_evidence(q,tmp_path)
    q=m.blank_source_questionnaire("max_inventory")
    q["lines"][0]["OEM_foreground"]["raw_input_material_bill_kg_by_grade"]={"steel":802*2400}
    # No OEM original quote or manufacturing inventory evidence is counted:
    result=m.validate_private_evidence(q,tmp_path)
    assert result["OEM_grade_specific_raw_material_BOM_lines"]==0


def test_vehicle_composite_uuid_cannot_be_mapped_to_stationary_steel(tmp_path):
    q=m.blank_source_questionnaire("max_inventory")
    v=add_private_vessel_source(q,tmp_path)
    v["BAFU_mapping"]["process_uuid"]=m.FORBIDDEN_BAFU_VEHICLE_PROCESS
    with pytest.raises(m.StationarySourceEvidenceError,match="vehicle composite"):
        m.validate_private_evidence(q,tmp_path)


def test_supplier_quotes_require_actual_currency_year_and_scope(tmp_path):
    q=m.blank_source_questionnaire("max_inventory")
    line=add_private_vessel_source(q,tmp_path)
    line["scope_status"]="OEM_QUOTE_NO_MATERIAL_LCI"
    line["supplier_quote"].update({
      "currency":"EUR","year":2026,
      "scope_installed_or_ex_works":"INSTALLED",
      "net_price_excl_tax":1000.0,
    })
    record=m.validate_private_evidence(q,tmp_path)
    assert record["supplier_quotations_with_currency_year_and_scope"]==1
    assert record["full_L3_B_economic_and_environmental_release_ALLOWED"] is False
    line["supplier_quote"]["year"]=None
    with pytest.raises(m.StationarySourceEvidenceError,match="monetary year"):
        m.validate_private_evidence(q,tmp_path)


def test_fake_manufacturer_reviewer_checkboxes_do_not_bypass_original_native_v11_evidence(tmp_path):
    q=m.blank_source_questionnaire("max_inventory")
    line=add_private_vessel_source(q,tmp_path)
    line["scope_status"]="OEM_AND_NATIVE_BAFU_MAPPING_REVIEWED"
    line["supplier_quote"].update({
        "currency":"EUR","year":2026,
        "scope_installed_or_ex_works":"INSTALLED",
        "net_price_excl_tax":1.0,
    })
    line["OEM_foreground"]["raw_input_material_bill_kg_by_grade"]={"synthetic_test_grade":1000.}
    line["BAFU_mapping"].update({
        "unit_matching_verified":True,
        "process_uuid":"fc9385f8-fe2d-3399-b663-4b66e5062a3f",
        "reference_flow_uuid":"11111111-2222-3333-4444-555555555555",
        "exchange_reference_unit":"kg",
        "independent_reviewer_approved":True,
    })
    line["independent_external_reviewer_signoff"]=True
    with pytest.raises(m.StationarySourceEvidenceError,match="actual original v1.1"):
        m.validate_private_evidence(q,tmp_path)
    fake_review={
        "schema_version":"ptxlens.L3B_BAFU2026_original_v11_quantitative_reference_candidate_REVIEW_NOT_provider_map.v1",
        "source_private_BAFU_v11_original_zolca_SHA256":"0"*64,
        "reference_processes":{},
    }
    with pytest.raises(m.StationarySourceEvidenceError,match="actual original v1.1"):
        m.validate_private_evidence(q,tmp_path,native_v11_identity_review=fake_review)
    # This is a deliberately fabricated synthetic review receipt; only the
    # production reconciler may genuinely create a source-attested one.
    fake_review["source_private_BAFU_v11_original_zolca_SHA256"] = (
        "e63b7e7ef5cde04bfe1176a783a55b5f72e2b73f42c36632b6150af39d348c4c"
    )
    fake_review["reference_processes"]={
        line["BAFU_mapping"]["process_uuid"]:{
            "identity_review_status":"ABSENT_IN_NATIVE_V11",
            "native_v11_reference_flow_uuid":"11111111-2222-3333-4444-555555555555",
            "native_v11_reference_flow_unit":"kg",
            "native_v11_reference_flow_type":"PRODUCT_FLOW",
        }}
    with pytest.raises(m.StationarySourceEvidenceError,match="lacks native original"):
        m.validate_private_evidence(q,tmp_path,native_v11_identity_review=fake_review)


def test_native_process_reference_flow_kg_vs_MJ_not_silently_interchangeable(tmp_path):
    q=m.blank_source_questionnaire("max_inventory")
    row=add_private_vessel_source(q,tmp_path)
    row["scope_status"]="OEM_AND_NATIVE_BAFU_MAPPING_REVIEWED"
    row["supplier_quote"].update({"currency":"EUR","year":2026,
                                  "scope_installed_or_ex_works":"EX_WORKS",
                                  "net_price_excl_tax":1.0})
    row["OEM_foreground"]["raw_input_material_bill_kg_by_grade"]={"synthetic_test_grade":1000.}
    uid="fc9385f8-fe2d-3399-b663-4b66e5062a3f"
    row["BAFU_mapping"].update({
        "process_uuid":uid,
        "reference_flow_uuid":"11111111-2222-3333-4444-555555555555",
        "exchange_reference_unit":"kg","unit_matching_verified":True,
        "independent_reviewer_approved":True,
    })
    row["independent_external_reviewer_signoff"]=True
    simulated_native_receipt={
       "schema_version":"ptxlens.L3B_BAFU2026_original_v11_quantitative_reference_candidate_REVIEW_NOT_provider_map.v1",
       "source_private_BAFU_v11_original_zolca_SHA256":
            "e63b7e7ef5cde04bfe1176a783a55b5f72e2b73f42c36632b6150af39d348c4c",
       "reference_processes":{uid:{
          "identity_review_status":"ORIGINAL_NATIVE_V11_PROCESS_AND_QUANTITATIVE_REFERENCE_ID_VERIFIED_ONLY",
          "native_v11_reference_flow_uuid":"11111111-2222-3333-4444-555555555555",
          "native_v11_reference_flow_unit":"MJ",
          "native_v11_reference_flow_type":"PRODUCT_FLOW",
       }}
    }
    with pytest.raises(m.StationarySourceEvidenceError,match="reference flow/unit"):
        m.validate_private_evidence(
            q,tmp_path,native_v11_identity_review=simulated_native_receipt)
