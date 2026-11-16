"""Synthetic 2024 public admission and two-year comparison negative regression tests.

This file constructs only pseudonymous synthetic source fingerprints and
aggregate cases, never touches actual 2022/2024 hourly provider/witness data.
"""
import copy
import hashlib
import json

import pytest

from ptxlens import f3d_2024_crossyear_publication as m


def cases(year,cost_e,cost_s):
    hours=8760 if year==2022 else 8784
    annual=hours*1250.
    a={}
    for name,cost in (("E",cost_e),("E_plus_S",cost_s)):
        a[name]={
            "status":"INDEPENDENT_ORIGINAL_FULL_YEAR_INTEGER_PRIMAL_H2_ELECTRIC_EOS_REPLAY_PASSED",
            "original_private_hourly_H2_wind_price_primal_vectors_NOT_in_public":True,
            "independent_integer_cost_dual_tree_proof":False,
            "independent_hourly_primal_SHA256":("a" if name=="E" else "b")*64,
            "independent_annual_delivered_H2_kg":annual,
            "source_reported_relative_MIP_gap":5e-7,
            "independent_source_max_physical_residual":4e-9,
            "independent_EOS_min_absolute_bar":20.,
            "independent_EOS_max_absolute_bar":199.9,
            "source_modelled_nominal_original_year_wholesale_eur":cost,
            "source_reported_solver_cost_lower_bound_eur":cost-0.001,
        }
    result={
        "schema_version":m.INTEGER_SCHEMA,
        "source_year":year,
        "capacity_semantics":"max_inventory",
        "source_year_UTC_hours":hours,
        "matched_exogenous_hydrogen_service_tonnes_day":30.,
        "matched_exogenous_service_annual_H2_kg":annual,
        "E_and_ES_fully_independent_primal_mass_electricity_EOS_market_replay":True,
        "cost_lower_bound_source_reported_NOT_independent_dual_reconstruction":True,
        "actual_site_or_manufacturer_or_BAFU_LCIA_or_scientific_v1_0_certified":False,
        "original_hourly_provider_arrays_or_solver_witnesses_in_public":False,
        "original_source_year_eur_not_inflation_adjusted":True,
        "case_results":a,
        "matched_service_modelled_wholesale_E_minus_ES_saving_source_eur":cost_e-cost_s,
        "matched_service_modelled_saving_eur_per_kg_H2":(cost_e-cost_s)/annual,
        "matched_service_source_solver_reported_savings_lower_upper_eur":[
            cost_e-0.001-cost_s,cost_e-(cost_s-0.001)
        ],
    }
    return result


def fixture():
    sha_orig=m.base.SOURCE_PUBLISHED_GIT_BLOB
    p2022="1"*64
    w2022="2"*64
    p2024="3"*64
    w2024="4"*64
    e_selected_2024="5"*64
    annual2022=10950000.
    pbase=cases(2022,32160567.931485903,28878954.877419014)
    p2024=cases(2024,2544581.872826561,612906.0201971165)
    original={
        "cases":[{
            "year":2022,"storage_capacity_semantics":"max_inventory",
            "source_year_price_f64_sha256":p2022,
            "source_year_wind_f64_sha256":w2022,
        },{
            "year":2024,"storage_capacity_semantics":"max_inventory",
            "source_year_price_f64_sha256":p2024,
            "source_year_wind_f64_sha256":w2024,
            "price_neutral_E_uniform_hydrogen_service":{
                "hourly_target_f64_sha256":e_selected_2024,
                "modelled_delivered_h2_tonnes_per_day":30.8321785,
            },
        }],
    }
    lp={
        "schema_version":m.LP_SCHEMA,
        "source_year":2024,
        "capacity_semantics":"max_inventory",
        "source_calendar_UTC_hours":8784,
        "source_original_4_case_public_Git_blob_sha1":sha_orig,
        "source_original_price_float64_SHA256":p2024,
        "source_original_wind_power_float64_SHA256":w2024,
        "source_original_E_max_selected_hourly_H2_float64_SHA256":e_selected_2024,
        "original_selected_E_max_nominal_tonnes_day":30.8321785,
        "prespecified_exogenous_delivery_tonnes_day":[25.,27.5,30.],
        "source_wind_electric_power_multipliers":[.9,.95,1.],
        "source_price_year_input_unchanged":True,
        "same_H2_target_hourly_for_E_and_ES_at_every_wind_factor":True,
        "exogenous_delivery_schedules_selected_without_looking_at_stressed_wind_outcomes":True,
        "original_integer_dispatch_or_matched_wholesale_savings_certified":False,
        "real_site_or_manufacturer_or_native_BAFU_or_scientific_v1_0":False,
        "nine_service_factor_pairs_two_architectures_LP_cells":[],
    }
    for d in (25.,27.5,30.):
        for k in (.9,.95,1.):
            lp["nine_service_factor_pairs_two_architectures_LP_cells"].append({
                "source_year":2024,"capacity_semantics":"max_inventory",
                "exogenous_H2_tonnes_per_day":d,
                "source_wind_power_multiplier":k,
                "exogenous_H2_original_same_hourly_SHA256":
                    m.base.floating_sha([d*1000/24]*8784),
                "exogenous_same_product_annual_H2_kg":d*1000*366,
                "E_and_ES_original_integer_dispatch_both_certified":False,
                "matched_source_annual_E_minus_EplusS_cost_saving_eur":None,
                "cases":{key:{
                    "HiGHS_LP_status_code":0,
                    "original_integer_MILP_feasible":None,
                    "source_E_or_EplusS_original_model_LP_status":
                        "SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED"
                } for key in ("E","E_plus_S")}
            })
    lpbytes=(json.dumps(lp,sort_keys=True,indent=2)+"\n").encode("utf-8")
    lp_sha=hashlib.sha256(lpbytes).hexdigest()
    p2024.update({
        "source_original_four_case_public_Git_blob_sha1":sha_orig,
        "independent_LP_screen_bytes_SHA256":lp_sha,
        "original_price_f64_SHA256":p2024,
        "original_wind_electric_power_f64_SHA256":w2024,
        "exogenous_fixed_hourly_hydrogen_service_f64_SHA256":
            m.base.floating_sha([1250.]*8784),
        "source_original_E_selected_max_H2_tonnes_day":30.8321785,
    })
    pbase.update({
        "original_price_f64_SHA256":p2022,
        "original_wind_electric_power_f64_SHA256":w2022,
    })
    previous_saving=pbase["matched_service_modelled_wholesale_E_minus_ES_saving_source_eur"]
    old_audit={
        "verified_original_historical_source_public_blob":sha_orig,
        "exogenous_year":2022,
        "capacity_semantics":"max_inventory",
        "independently_replayed_original_integer_H2_power_EOS_market":True,
        "paired_E_minus_EplusS_nominal_source_year_eur":previous_saving,
        "per_kg_modelled_source_year_nominal_eur":previous_saving/annual2022,
        "real_site_OEM_native_BAFU_and_scientific_v1_0_verified":False,
    }
    return original,lp,p2024,pbase,old_audit,lp_sha


def audit_fixture(monkeypatch,mutable=None):
    original,lp,integer,old_int,old_audit,lp_sha=fixture()
    if mutable:
        mutable(lp,integer,old_int,old_audit,original)
    records={m.LP_FILE:lp,m.INTEGER_FILE:integer}
    sha_orig_for_test=m.base.SOURCE_PUBLISHED_GIT_BLOB
    monkeypatch.setattr(m.base,"source_blob_sha",lambda raw: sha_orig_for_test)
    return m.audit_2024_and_compare(
        records,{m.LP_FILE:lp_sha},
        json.dumps(original).encode("utf-8"),old_audit,old_int)


def test_2024_full_crossyear_source_service_and_costs_accepted(monkeypatch):
    r=audit_fixture(monkeypatch)
    y2022,y2024=r["source_year_results"]
    assert y2022["calendar_UTC_hours"]==8760
    assert y2024["calendar_UTC_hours"]==8784
    assert y2024["annual_delivered_H2_kg"]==10980000.
    assert y2024["source_year_wholesale_E_minus_EplusS_saving_eur"]==pytest.approx(
        1931675.8526294443)
    assert y2024["source_year_wholesale_saving_eur_per_kg"]==pytest.approx(
        .17592676253455777)
    assert y2022["source_year_wholesale_saving_eur_per_kg"]==pytest.approx(
        .2996906898691223)
    assert r["2024_minus_2022_nominal_saving_eur_per_kg"]<0
    assert r["both_source_years_storage_reduces_modelled_wholesale_electricity_cost"]
    assert not r["public_hourly_provider_price_wind_or_original_MILP_witness_arrays_in_report"]
    assert r["comparison_2022_2024_nominal_EUR_NOT_inflation_adjusted"]
    assert "NOT uncertainty" in m.report_markdown(r) or "not a weather-risk" in m.report_markdown(r)


@pytest.mark.parametrize("mutator",[
    lambda lp,i,o,a,s: i.update(independent_LP_screen_bytes_SHA256="bad"),
    lambda lp,i,o,a,s: i.update(matched_exogenous_service_annual_H2_kg=10950000.),
    lambda lp,i,o,a,s: i.update(matched_service_modelled_wholesale_E_minus_ES_saving_source_eur=1.),
    lambda lp,i,o,a,s: i.update(original_price_f64_SHA256="bad"),
    lambda lp,i,o,a,s: i.update(source_original_E_selected_max_H2_tonnes_day=30.),
    lambda lp,i,o,a,s: i.update(actual_site_or_manufacturer_or_BAFU_LCIA_or_scientific_v1_0_certified=True),
    lambda lp,i,o,a,s: i["case_results"]["E"].update(
        independent_annual_delivered_H2_kg=10970000.),
    lambda lp,i,o,a,s: i["case_results"]["E_plus_S"].update(
        source_reported_relative_MIP_gap=.01),
    lambda lp,i,o,a,s: i["case_results"]["E_plus_S"].update(
        independent_EOS_max_absolute_bar=250.),
    lambda lp,i,o,a,s: lp["nine_service_factor_pairs_two_architectures_LP_cells"][6][
        "cases"]["E"].update(HiGHS_LP_status_code=2),
    lambda lp,i,o,a,s: lp["nine_service_factor_pairs_two_architectures_LP_cells"].pop(),
    lambda lp,i,o,a,s: a.update(independently_replayed_original_integer_H2_power_EOS_market=False),
    lambda lp,i,o,a,s: o["case_results"]["E"].update(independent_integer_cost_dual_tree_proof=True),
])
def test_2024_source_or_old_published_evidence_tampering_fails_closed(monkeypatch,mutator):
    with pytest.raises(m.base.EvidenceReleaseError):
        audit_fixture(monkeypatch,mutator)


def test_2024_only_three_expected_public_source_files_and_no_hourly_arrays(tmp_path):
    data={
        m.LP_FILE:{"schema_version":m.LP_SCHEMA},
        m.INTEGER_FILE:{"schema_version":m.INTEGER_SCHEMA},
    }
    for name,value in data.items():
        (tmp_path/name).write_text(json.dumps(value),encoding="utf-8",newline="\n")
    (tmp_path/m.LP_MD).write_text("# Synthetic E/ES source H2 LP\n",encoding="utf-8",newline="\n")
    result,hashes=m.get_2024_files(tmp_path)
    assert set(result)=={m.LP_FILE,m.INTEGER_FILE}
    assert len(hashes)==3
    path=tmp_path/m.INTEGER_FILE
    d=data[m.INTEGER_FILE]
    d["original_full_hourly_states_8var_PRIVATE"]=[[0]*8 for _ in range(8784)]
    path.write_text(json.dumps(d),encoding="utf-8",newline="\n")
    with pytest.raises(m.base.EvidenceReleaseError):
        m.get_2024_files(tmp_path)


def test_2024_private_hourly_material_never_required_to_generate_cross_year_summary(monkeypatch):
    r=audit_fixture(monkeypatch)
    summary=m.report_markdown(r)
    assert "2024 (8,784 h)" in summary
    assert "2022 (8,760 h)" in summary
    assert "EUR/kg" in summary
    assert "not inflation-adjusted" in summary.lower()
    assert "private" not in str(r["source_year_results"]).lower() or all(
        case["private_hourly_state_arrays_in_public"] is False
        for year in r["source_year_results"] for case in year["source_cases"].values())


def test_cross_year_output_immutable_and_no_extra_2024_public_files(tmp_path,monkeypatch):
    r=audit_fixture(monkeypatch)
    created=m.write_immutable_output(tmp_path,r)
    assert len(created)==2
    assert created==[m.STEM+".json",m.STEM+".md"]
    assert m.write_immutable_output(tmp_path,r)==created
    altered=copy.deepcopy(r)
    altered["source_year_results"][1]["source_year_wholesale_E_minus_EplusS_saving_eur"]=2.
    with pytest.raises(m.base.EvidenceReleaseError):
        m.write_immutable_output(tmp_path,altered)
