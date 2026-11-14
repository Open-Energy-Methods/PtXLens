"""Tests use declared synthetic financial and H2 fixtures, never observations."""
import copy
import hashlib
import json
import struct
import pytest

from ptxlens.f3d_external_year_independent_review import (
    ExternalYearReviewError, check_result, review_four_cases,
    SCHEMA, SEL, E_SHA, ES_SHA,
)


def fixture(year=2024,mode="usable_service"):
    hours=8784 if year==2024 else 8760
    alpha=0.85 if mode=="usable_service" else 0.83
    target=(50000./24.)*alpha
    h2=hours*target
    digest=hashlib.sha256(struct.pack("<d",target)*hours).hexdigest()
    p={"EOS_hourly_mass_bounds_imply_pressure_limits":True,
       "temperature_k_is_fixed_screening_assumption":True}
    def case(cost,dual):
        return {
            "modelled_hourly_H2_service_sha256":digest,
            "modelled_annual_hydrogen_kg":h2,
            "modelled_cost_eur_in_source_calendar_not_inflation_adjusted":cost,
            "solver_cost_lower_bound_eur":dual,
            "mip_relative_gap":1e-7,
            "max_independent_residual":1e-7,
            "not_actual_industrial_operation":True,
            "pressure_EOS_screen_bounds":copy.deepcopy(p),
            "modelled_grid_import_mwh":10000,
            "modelled_grid_export_mwh":2000,
            "modelled_compressor_electricity_mwh":500,
            "modelled_hydrogen_storage_peak_kg":15000,
        }
    e,es=case(1_000_000.,999_998.),case(900_000.,899_999.)
    return {
      "schema_version":SCHEMA,"year":year,"capacity_semantics":mode,
      "year_UTC_hours":hours,"original_source_E_zip_SHA256":E_SHA,
      "original_source_ES_zip_SHA256":ES_SHA,
      "provider_pair_source_2023_reconstruction_and_calendar_verified":True,
      "source_A44_and_ERA5_provider_original_files_held_private":True,
      "source_year_price_f64_sha256":"a"*64,
      "source_year_wind_f64_sha256":"b"*64,
      "E_price_blind_identical_model_H2_service_selection":{
        "schema_version":SEL,"year":year,"testing_only":False,
        "E_binary_price_neutral_feasible":True,"source_E_pressure_screen_only":True,
        "selected_fraction_50t_per_day":alpha,
        "certified_fraction_upper_bound":alpha+5e-8,
        "E_price_neutral_mip_relative_gap":1e-7,
        "modelled_E_flat_h2_service_kg_per_hour":target,
        "modelled_E_annual_h2_service_kg":h2,
        "original_nominal_h2_demand_kg":hours*50000/24.,
        "selected_h2_target_float64_sha256":digest,
        "E_price_neutral_physical_residual_max":1e-7,
      },
      "E":e,"E_plus_S":es,
      "mathematically_matched_exact_same_modelled_hourly_H2_target":True,
      "cost_savings_E_minus_EplusS_source_calendar_nominal_eur":100000.,
      "solver_difference_guaranteed_lower_upper_interval_eur":[99998.,100001.],
      "actual_industrial_H2_delivery_or_independent_measurements":False,
      "vendor_200bar_compressor_and_storage_station_BOM_verified":False,
      "native_BAFU_whole_plant_GWP_verified":False,
      "installed_plant_LCOH_or_investment_DCF_certified":False,
      "independent_external_scientific_peer_review_completed":False,
      "v1_0_scientific_release_allowed":False,
      "no_provider_price_wind_or_dispatch_hourly_arrays_in_report":True,
      "energy_year_2022_and_2024_eur_not_yet_inflation_normalized":True,
    }


@pytest.mark.parametrize("year,mode",[(2022,"max_inventory"),(2022,"usable_service"),
                                       (2024,"max_inventory"),(2024,"usable_service")])
def test_independent_review_accepts_only_complete_synthetic_arithmetic_envelopes(year,mode):
    r=check_result(fixture(year,mode))
    assert r["year"]==year and r["capacity_semantics"]==mode
    assert r["metadata_arithmetic_model_scope_review_passed"] is True
    assert r["independent_source_NetCDF_XML_or_dispatch_primal_replay_completed"] is False


@pytest.mark.parametrize("corrupt",[
    lambda r:r.update(year_UTC_hours=8760),
    lambda r:r["E"].update(modelled_hourly_H2_service_sha256="0"*64),
    lambda r:r["E_plus_S"].update(solver_cost_lower_bound_eur=1_000_000.),
    lambda r:r.update(solver_difference_guaranteed_lower_upper_interval_eur=[0,0]),
    lambda r:r.update(v1_0_scientific_release_allowed=True),
    lambda r:r["E_price_blind_identical_model_H2_service_selection"].update(testing_only=True),
    lambda r:r["E_price_blind_identical_model_H2_service_selection"].update(selected_fraction_50t_per_day=0.89),
    lambda r:r["E_plus_S"]["pressure_EOS_screen_bounds"].update(EOS_hourly_mass_bounds_imply_pressure_limits=False),
])
def test_independent_review_rejects_unsupported_or_changed_claims(corrupt):
    r=fixture(2024,"usable_service")
    corrupt(r)
    with pytest.raises(ExternalYearReviewError):
        check_result(r)


def test_full_matrix_requires_two_separate_years_and_capacity_interpretations(tmp_path):
    paths=[]
    for year in (2022,2024):
        for mode in ("max_inventory","usable_service"):
            f=tmp_path/f"synthetic_{year}_{mode}.json"
            f.write_text(json.dumps(fixture(year,mode)))
            paths.append(f)
    result=review_four_cases(paths)
    assert result["year_mode_count"]==4
    assert result["original_source_lca_tea_safety_and_v1_0_still_blocked"] is True
    assert result["source_data_and_original_dispatch_witnesses_NOT_independently_replayed"] is True
    with pytest.raises(ExternalYearReviewError,match="BOTH years"):
        review_four_cases(paths[:3])


def test_gross_usable_same_year_must_use_same_price_and_weather_history(tmp_path):
    paths=[]
    for year in (2022,2024):
        for mode in ("max_inventory","usable_service"):
            r=fixture(year,mode)
            if year==2022 and mode=="usable_service":
                r["source_year_wind_f64_sha256"]="f"*64
            p=tmp_path/f"synthetic_{year}_{mode}.json"
            p.write_text(json.dumps(r))
            paths.append(p)
    with pytest.raises(ExternalYearReviewError,match="unmatched original"):
        review_four_cases(paths)
