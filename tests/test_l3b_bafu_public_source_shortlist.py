"""Independent BAFU public-v1 shortlist negative controls; mock is NOT original data."""
import copy
import json
import pytest
import ptxlens.l3b_bafu_public_source_shortlist as m


def synthetic_public_index_from_real_registry_structure():
    # The source catalogue is retrieved and SHA-verified by the live workflow.
    # This mock ONLY tests that its independent shortlist checker fails closed.
    r=json.loads(m.REGISTER.read_text(encoding="utf-8"))
    index={c["uuid"]:{
        "processName":c["processName"],
        "location":c["location"],
        "referenceUnit":c["referenceUnit"],
    } for c in r["entries"]}
    return r,index


def test_shortlist_scope_can_be_replayed_only_with_exact_source_columns(monkeypatch):
    r,index=synthetic_public_index_from_real_registry_structure()
    monkeypatch.setattr(m,"original_public_catalogue",lambda *_:(
        index,r["original_BAFU_v1_public_process_csv_SHA256"]))
    result=m.audit_shortlist("NOT_REAL.csv","NOT_REAL.json")
    assert result["source_selected_UUID_name_geo_unit_exact_matches"]==16
    assert result["original_native_v11_zolca_or_technosphere_examined_by_this_validator"] is False
    assert result["source_independent_native_LCIA_and_supplier_BOM_passed"] is False


def test_changing_source_GWP_unit_and_reference_is_rejected(monkeypatch):
    r,index=synthetic_public_index_from_real_registry_structure()
    altered=copy.deepcopy(index)
    first=r["entries"][0]["uuid"]
    altered[first]["referenceUnit"]="MJ"
    monkeypatch.setattr(m,"original_public_catalogue",lambda *_:(
        altered,r["original_BAFU_v1_public_process_csv_SHA256"]))
    with pytest.raises(m.BafuCrosswalkEvidenceError,match="reference unit mismatch"):
        m.audit_shortlist("NOT_REAL.csv","NOT_REAL.json")


def test_native_supplier_promotion_without_new_database_is_rejected(tmp_path,monkeypatch):
    r,index=synthetic_public_index_from_real_registry_structure()
    r["entries"][0]["native_v11_process_verified_in_current_crosswalk"]=True
    p=tmp_path/"SYNTHETIC_REGISTRY_TAMPERED.json"
    p.write_text(json.dumps(r))
    monkeypatch.setattr(m,"original_public_catalogue",lambda *_:(
        index,r["original_BAFU_v1_public_process_csv_SHA256"]))
    with pytest.raises(m.BafuCrosswalkEvidenceError,match="not an OEM material"):
        m.audit_shortlist("NOT_REAL.csv","NOT_REAL.json",p)


def test_public_source_version_catalogue_sha_cannot_be_replaced(monkeypatch):
    r,index=synthetic_public_index_from_real_registry_structure()
    monkeypatch.setattr(m,"original_public_catalogue",lambda *_:(index,"f"*64))
    with pytest.raises(m.BafuCrosswalkEvidenceError,match="SHA drift"):
        m.audit_shortlist("NOT_REAL.csv","NOT_REAL.json")
