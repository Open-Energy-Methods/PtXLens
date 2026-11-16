"""F3-D fail-closed nine-file scientific publication audit tests (synthetic).

No private 2022 provider arrays or production E/ES integer witness files are
present or used by these tests. The Git-blob helper is monkeypatched solely
for synthetic fixture admission; actual release checks the REAL source blob.
"""
import copy
import hashlib
import json
import math
from pathlib import Path

import pytest

from ptxlens import f3d_2022_public_evidence_admission as m


def synthetic_evidence():
    src_price="a"*64
    src_wind="b"*64
    src_h2="c"*64
    delivered=10950000.
    targetsha=m.floating_sha([1250.]*8760)
    cases=[]
    for day in (25.,27.5,30.):
        for k in (.9,.95,1.):
            target=m.floating_sha([day*1000/24.]*8760)
            cases.append({
                "exogenous_H2_tonnes_per_day":day,
                "source_wind_power_multiplier":k,
                "exogenous_H2_original_same_hourly_SHA256":target,
                "cases":{"E":{
                    "HiGHS_LP_status_code":0,
                    "original_integer_MILP_feasible":None
                },"E_plus_S":{
                    "HiGHS_LP_status_code":0,
                    "original_integer_MILP_feasible":None
                }},
            })
    lp={
        "schema_version":m.EXOGENOUS_LP_SCHEMA,
        "source_year":2022,"capacity_semantics":"max_inventory",
        "source_calendar_UTC_hours":8760,
        "source_original_4_case_public_Git_blob_sha1":m.SOURCE_PUBLISHED_GIT_BLOB,
        "source_original_price_float64_SHA256":src_price,
        "source_original_wind_power_float64_SHA256":src_wind,
        "source_original_E_max_selected_hourly_H2_float64_SHA256":src_h2,
        "prespecified_exogenous_delivery_tonnes_day":[25.,27.5,30.],
        "source_wind_electric_power_multipliers":[.9,.95,1.],
        "same_H2_target_hourly_for_E_and_ES_at_every_wind_factor":True,
        "original_integer_dispatch_or_matched_wholesale_savings_certified":False,
        "real_site_or_manufacturer_or_native_BAFU_or_scientific_v1_0":False,
        "nine_service_factor_pairs_two_architectures_LP_cells":cases,
    }
    costs={"E":32160567.931485903,"E_plus_S":28878954.877419014}
    integer={
        "schema_version":m.EXOGENOUS_INTEGER_SCHEMA,
        "source_year":2022,"capacity_semantics":"max_inventory",
        "source_year_UTC_hours":8760,
        "source_original_four_case_public_Git_blob_sha1":m.SOURCE_PUBLISHED_GIT_BLOB,
        "independent_LP_screen_bytes_SHA256":"placeholder",
        "original_price_f64_SHA256":src_price,
        "original_wind_electric_power_f64_SHA256":src_wind,
        "exogenous_fixed_hourly_hydrogen_service_f64_SHA256":targetsha,
        "matched_exogenous_hydrogen_service_tonnes_day":30.,
        "matched_exogenous_service_annual_H2_kg":delivered,
        "E_and_ES_fully_independent_primal_mass_electricity_EOS_market_replay":True,
        "cost_lower_bound_source_reported_NOT_independent_dual_reconstruction":True,
        "actual_site_or_manufacturer_or_BAFU_LCIA_or_scientific_v1_0_certified":False,
        "original_hourly_provider_arrays_or_solver_witnesses_in_public":False,
        "case_results":{
            key:{
                "status":"INDEPENDENT_ORIGINAL_FULL_YEAR_INTEGER_PRIMAL_H2_ELECTRIC_EOS_REPLAY_PASSED",
                "original_private_hourly_H2_wind_price_primal_vectors_NOT_in_public":True,
                "independent_integer_cost_dual_tree_proof":False,
                "independent_annual_delivered_H2_kg":delivered,
                "source_reported_relative_MIP_gap":1e-7,
                "independent_source_max_physical_residual":2e-6,
                "independent_EOS_min_absolute_bar":35.,
                "independent_EOS_max_absolute_bar":150.,
                "source_modelled_nominal_original_year_wholesale_eur":val,
                "source_reported_solver_cost_lower_bound_eur":val-0.001,
            } for key,val in costs.items()
        },
        "matched_service_modelled_wholesale_E_minus_ES_saving_source_eur":
            costs["E"]-costs["E_plus_S"],
        "matched_service_modelled_saving_eur_per_kg_H2":
            (costs["E"]-costs["E_plus_S"])/delivered,
        "matched_service_source_solver_reported_savings_lower_upper_eur":[
            costs["E"]-0.001-costs["E_plus_S"],
            costs["E"]-(costs["E_plus_S"]-0.001)
        ],
    }
    original={"cases":[{
        "year":2022,"storage_capacity_semantics":"max_inventory",
        "source_year_price_f64_sha256":src_price,
        "source_year_wind_f64_sha256":src_wind,
        "price_neutral_E_uniform_hydrogen_service":{
            "hourly_target_f64_sha256":src_h2
        }
    }]}
    other={
      fn:{"schema_version":schema}
      for fn,schema in m.NAME_TO_SCHEMA.items()
    }
    lp_name=next(n for n in other if "EXOGENOUS_H2_SOURCE_LP" in n)
    integer_name=next(n for n in other if "BOTH_INTEGER_INDEPENDENT_REPLAY" in n)
    other[lp_name]=lp
    other[integer_name]=integer
    return original,other,lp_name,integer_name


def write_synthetic_files(tmp_path):
    original,other,lp_name,integer_name=synthetic_evidence()
    filenames={}
    for filename,data in other.items():
        raw=(json.dumps(data,sort_keys=True,indent=2)+"\n").encode("utf-8")
        (tmp_path/filename).write_bytes(raw)
        filenames[filename]=hashlib.sha256(raw).hexdigest()
    for filename in m.ADDITIONAL_MD_FILES:
        raw=b"# F3-D synthetic independently reviewed result\n\nNo real plant viability.\n"
        (tmp_path/filename).write_bytes(raw)
        filenames[filename]=hashlib.sha256(raw).hexdigest()
    integer=other[integer_name]
    integer["independent_LP_screen_bytes_SHA256"]=filenames[lp_name]
    raw=(json.dumps(integer,sort_keys=True,indent=2)+"\n").encode("utf-8")
    (tmp_path/integer_name).write_bytes(raw)
    filenames[integer_name]=hashlib.sha256(raw).hexdigest()
    source_file=tmp_path/"SYNTHETIC_original_source.json"
    source_file.write_text(json.dumps(original),encoding="utf-8")
    return source_file


def test_all_nine_public_research_outputs_safe_and_crosslinked(tmp_path,monkeypatch):
    source=write_synthetic_files(tmp_path)
    monkeypatch.setattr(m,"source_blob_sha",lambda raw:m.SOURCE_PUBLISHED_GIT_BLOB)
    certificate=m.audit(tmp_path,source)
    assert len(certificate["approved_public_files"])==9
    assert certificate["all_9_sanitized_source_model_evidence_files_present"] is True
    assert certificate["independently_replayed_original_integer_H2_power_EOS_market"] is True
    assert certificate["paired_E_minus_EplusS_nominal_source_year_eur"]==pytest.approx(
        3281613.054066889)
    assert certificate["per_kg_modelled_source_year_nominal_eur"]==pytest.approx(
        .2996906898691223)
    assert certificate["integer_MIP_tree_dual_independently_recomputed"] is False
    assert certificate["real_site_OEM_native_BAFU_and_scientific_v1_0_verified"] is False


def test_private_hourly_witness_and_large_arrays_rejected_without_reader(tmp_path):
    for node in (
        {"hourly_solved_states":[[1.0]*8]},
        {"cost_optimum_hourly_states":[0.]},
        {"not_a_source_name":[1.]*8760},
        {"field":{"a":[1.] * 21}},
        {"secret":"BEGIN PRIVATE KEY"},
    ):
        with pytest.raises(m.EvidenceReleaseError):
            m.minimize_tree(node)
    m.minimize_tree({"status":"source_model_replayed",
                     "source_original_hourly_primal_NOT_in_public_report":True})


def test_no_missing_public_file_or_source_symlink_admitted(tmp_path):
    source=write_synthetic_files(tmp_path)
    md=tmp_path/m.ADDITIONAL_MD_FILES[0]
    md.unlink()
    with pytest.raises(m.EvidenceReleaseError,match="absent"):
        m.audit(tmp_path,source)
    md.symlink_to(source)
    with pytest.raises(m.EvidenceReleaseError,match="symlink"):
        m.audit(tmp_path,source)


def test_consolidated_pair_saving_cannot_deviate_from_original_source_costs(tmp_path,monkeypatch):
    source=write_synthetic_files(tmp_path)
    monkeypatch.setattr(m,"source_blob_sha",lambda raw:m.SOURCE_PUBLISHED_GIT_BLOB)
    name=next(n for n in m.NAME_TO_SCHEMA if "BOTH_INTEGER_INDEPENDENT_REPLAY" in n)
    file=tmp_path/name
    d=json.loads(file.read_text())
    d["matched_service_modelled_wholesale_E_minus_ES_saving_source_eur"]=1.
    file.write_text(json.dumps(d),encoding="utf-8")
    with pytest.raises(m.EvidenceReleaseError,match="arithmetic"):
        m.audit(tmp_path,source)


def test_untrusted_LP_screen_SHA_breaks_independent_2022_integer_replay_link(tmp_path,monkeypatch):
    source=write_synthetic_files(tmp_path)
    monkeypatch.setattr(m,"source_blob_sha",lambda raw:m.SOURCE_PUBLISHED_GIT_BLOB)
    filename=next(n for n in m.NAME_TO_SCHEMA if "EXOGENOUS_H2_SOURCE_LP" in n)
    path=tmp_path/filename
    data=json.loads(path.read_text())
    data["fake_field"]="changed"
    path.write_text(json.dumps(data),encoding="utf-8")
    with pytest.raises(m.EvidenceReleaseError,match="independent full-year source H30"):
        m.audit(tmp_path,source)


def test_source_original_git_blob_not_a_fake_sha(tmp_path):
    source=write_synthetic_files(tmp_path)
    with pytest.raises(m.EvidenceReleaseError,match="Git blob"):
        m.audit(tmp_path,source)


def test_replay_bool_tampering_rejected_without_real_2022_source(tmp_path,monkeypatch):
    source=write_synthetic_files(tmp_path)
    monkeypatch.setattr(m,"source_blob_sha",lambda raw:m.SOURCE_PUBLISHED_GIT_BLOB)
    name=next(n for n in m.NAME_TO_SCHEMA if "BOTH_INTEGER_INDEPENDENT_REPLAY" in n)
    file=tmp_path/name
    data=json.loads(file.read_text())
    data["E_and_ES_fully_independent_primal_mass_electricity_EOS_market_replay"]=False
    file.write_text(json.dumps(data),encoding="utf-8")
    with pytest.raises(m.EvidenceReleaseError,match="independent full-year"):
        m.audit(tmp_path,source)
