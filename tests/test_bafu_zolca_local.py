"""Local archive-format tests, NOT fictitious material/environmental results."""
import zipfile
import pytest
from ptxlens.bafu_zolca_local import inspect_zolca

def test_nested_outer_nexus_zip_not_treated_as_database(tmp_path):
    p=tmp_path/"nexus_outer.zip"
    with zipfile.ZipFile(p,"w") as z:
        z.writestr("BAFU_2026_v1.zolca",b"not a backed-up database")
    with pytest.raises(ValueError,match="legally obtained inner"):
        inspect_zolca(p)

def test_invalid_archive_refused(tmp_path):
    p=tmp_path/"BAFU_2026_v1.zolca"
    p.write_bytes(b"not an original .zolca file")
    with pytest.raises(ValueError,match="not a valid ZIP"):
        inspect_zolca(p)

def test_unsafe_zip_members_block_native_import(tmp_path):
    p=tmp_path/"BAFU_2026_v1.zolca"
    with zipfile.ZipFile(p,"w") as z:
        z.writestr("../traversal","x")
        z.writestr("service.properties","x")
        z.writestr("seg0/c.dat","x")
        z.writestr("log/log1.dat","x")
    with pytest.raises(ValueError,match="unsafe"):
        inspect_zolca(p)

def test_minimal_format_check_does_not_claim_licensed_release_or_LCA(tmp_path):
    p=tmp_path/"local-archive.zolca"
    with zipfile.ZipFile(p,"w") as z:
        z.writestr("service.properties","only test structure; never original BAFU")
        z.writestr("seg0/c.dat","test")
        z.writestr("log/log1.dat","test")
        for i in range(51):
            z.writestr(f"log/test_{i}.dat",b"no research data")
    result=inspect_zolca(p)
    assert result["edition_verified_from_nexus_account"] is False
    assert result["can_claim_provider_complete"] is False
    assert result["native_openlca_Derby_backup_structure_verified"] is True
    assert len(result["original_archive_sha256"])==64
