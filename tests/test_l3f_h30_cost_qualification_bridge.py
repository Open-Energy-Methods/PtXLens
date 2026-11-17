"""L3-F 19 original Type I cost roles vs 2022/2024 conditional DCF.

No actual supplier quote or original private hourly provider data needed.
"""
import pytest

from ptxlens import l3f_h30_cost_qualification_bridge as m
from ptxflex import f2l3e_exogenous_vendor_cost_intake as vendor


def test_original_source_year_costs_and_physical_scope_contract():
    d=m.build()
    assert d["schema_version"]==m.SCHEMA
    assert d["source_F2_incremental_20t_gross_not_20t_usable"] is True
    assert d["matched_2022_2024_H2_daily_tonnes"]==30.
    rows=d["nineteen_site_verified_supplier_installed_scope_lines"]
    assert len(rows)==19
    assert len({r["original_F2_line_id"] for r in rows})==19
    assert rows[0]["original_802_pressure_vessel_count_is_ONLY_paper_reference"]
    assert all(row["incremental_real_supplier_initial_CAPEX_EUR"] is None for row in rows)
    assert all(row["real_supplier_price_can_be_used_in_NPV"] is False for row in rows)
    assert d["all_in_actual_installed_incremental_CAPEX_eur"] is None
    assert d["site_project_commercial_NPV_authorized"] is False


def test_same_20year_8pct_real_repeat_and_replacement_matches_L3E_reference():
    r=m.build()["source_year_conditional_cost_limits"]
    assert set(r)=={"2022","2024"}
    assert r["2022"]["original_independently_replayed_wholesale_saving_eur"]==pytest.approx(
        3281613.054066889)
    assert r["2024"]["original_independently_replayed_wholesale_saving_eur"]==pytest.approx(
        1931675.8526294443)
    for yr in ("2022","2024"):
        s=r[yr]["repeat_fraction_sensitivity"]
        assert set(s)=={"0.50","0.75","1.00"}
        assert (s["0.50"]["zero_NPV_maximum_incremental_all_in_CAPEX_year_eur"]<
                s["0.75"]["zero_NPV_maximum_incremental_all_in_CAPEX_year_eur"]<
                s["1.00"]["zero_NPV_maximum_incremental_all_in_CAPEX_year_eur"])
        assert s["1.00"]["verified_manufacturer_OEM_all_in_installed_price_EUR"] is None
        assert s["1.00"]["actual_investment_profitable"] is None
    assert r["2022"]["repeat_fraction_sensitivity"]["1.00"][
        "zero_NPV_maximum_incremental_all_in_CAPEX_year_eur"]==pytest.approx(
            29301630.35909155)
    assert r["2024"]["repeat_fraction_sensitivity"]["1.00"][
        "zero_NPV_maximum_incremental_all_in_CAPEX_year_eur"]==pytest.approx(
            16047747.92457916)


def test_original_19_supplier_source_missing_prices_do_not_pretend_zero():
    result=m.review_private_supplier_ledger_without_project_approval(vendor.make())
    assert result["source_supplier_ledger_precheck"][
        "complete_supplier_cost_quote_line_count"]==0
    assert len(result["source_supplier_ledger_precheck"][
        "unquoted_or_unpriced_line_ids"])==19
    assert result["can_compare_actual_verified_2022_2024_all_in_costs_against_DCF"] is False
    assert result["actual_financial_return_inferable"] is False


def test_metadata_filled_without_real_document_custody_still_fails_v1():
    fake=vendor.make()
    first=fake["nineteen_required_supplier_and_site_intake_lines"][0]
    first["manufacturer_total_quoted_incremental_CAPEX_eur"]=750000.
    first["signed_quote_file_sha256"]="a"*64
    r=m.review_private_supplier_ledger_without_project_approval(fake)
    assert r["all_required_private_supplier_original_documents_authenticated"] is False
    assert r["actual_financial_return_inferable"] is False


def test_readable_reports_disclose_uncertainty_and_no_supplier_data():
    d=m.build()
    x=m.markdown(d)
    assert "50" not in x or "0.50" in x
    assert "20t MAX-inventory" in x
    assert "None are accepted now" in x
    assert "| None |" not in x
    assert "NOT" in x
