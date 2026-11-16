"""DOE HFTO Record 24005 PEM reference cost component (2022 USD).

This is *not* an OpenPyTEA or H2A calculation and not a total hydrogen LCOH.
Explicitly retains different source-year/currency from Dutch 2023 settlement.

Source: https://www.hydrogen.energy.gov/docs/hydrogenprogramlibraries/pdfs/24005-clean-hydrogen-production-cost-pem-electrolyzer.pdf
DOE, 20 May 2024, Table 1, pp 2-3: 57 kWh/kg, 30 years, installed
$1500/$2000/$2500 per kW, stack replacement 40,000 operating hours
at 11% of total installed capital, USD-2022.
"""
import math
from .core import crf

DOE_URL = ("https://www.hydrogen.energy.gov/docs/hydrogenprogramlibraries/"
           "pdfs/24005-clean-hydrogen-production-cost-pem-electrolyzer.pdf")
CAPEX_CASES_USD2022_KW = (1500,2000,2500)
SOURCE_LIFETIME_YEARS = 30
SOURCE_STACK_REPLACE_HOURS = 40000
SOURCE_REPLACE_FRACTION = 0.11
SOURCE_SYSTEM_KWH_PER_KG = 57.0


def assess_doe_capital_component(observed, *, installed_cost_usd2022_kw,
                                 real_discount_rate):
    """Use sourced cost inputs and observed simulated annual operating hours.

    Repeat the observed 2023 *modelled* production year unchanged over 30
    years only for sensitivity. That repeat is not a historical forecast.
    """
    cost = installed_cost_usd2022_kw
    if cost not in CAPEX_CASES_USD2022_KW:
        raise ValueError("must select documented DOE $1500/2000/2500 case")
    if (isinstance(real_discount_rate,bool) or
            not isinstance(real_discount_rate,(int,float)) or
            not math.isfinite(real_discount_rate) or real_discount_rate < 0):
        raise ValueError("explicit valid scenario real discount rate required")
    if observed["scenario"] not in ("E","E+S"):
        raise ValueError("only pinned observed WP5 source scenarios supported")
    hours = observed["online_hours"]
    delivered = observed["annual_delivered_h2_kg"]
    capacity_mw = observed["electrolyser_capacity_mw"]
    if not 0 < hours <= 8760 or delivered <= 0 or capacity_mw <= 0:
        raise ValueError("invalid source utilisation, annual delivery or capacity")
    capex = capacity_mw * 1000 * cost
    replacement_year_interval = SOURCE_STACK_REPLACE_HOURS / hours
    replacement_times = []
    t = replacement_year_interval
    while t < SOURCE_LIFETIME_YEARS - 1e-10:
        replacement_times.append(t)
        t += replacement_year_interval
    pv_replacements = sum(
        capex * SOURCE_REPLACE_FRACTION / (1+real_discount_rate) ** t
        for t in replacement_times)
    capital_annual = (capex + pv_replacements) * crf(real_discount_rate,SOURCE_LIFETIME_YEARS)
    energy_kwh_per_kg = 1000 * observed["annual_electrolyser_input_mwh"]/observed["annual_produced_h2_kg"]
    return {
        "schema_version":"ptxlens.doe_reference_capital.v0.1",
        "source":DOE_URL,"source_document_date":"2024-05-20",
        "scenario":observed["scenario"],"currency":"USD",
        "capital_price_year":2022,"capital_basis":"installed cost USD2022/kW",
        "installed_cost_usd2022_kw":cost,
        "system_lifetime_years":SOURCE_LIFETIME_YEARS,
        "stack_replacement_operating_hours":SOURCE_STACK_REPLACE_HOURS,
        "replacement_fraction_of_initial_installed_cost":SOURCE_REPLACE_FRACTION,
        "doe_reference_system_kwh_per_kg":SOURCE_SYSTEM_KWH_PER_KG,
        "pynexus_modelled_kwh_per_kg_produced":energy_kwh_per_kg,
        "real_discount_rate_scenario_NOT_DOE":real_discount_rate,
        "repeat_year_assumption":"2023 modelled hours and delivered H2 repeated unchanged for 30 years",
        "initial_installed_capex_usd2022":capex,
        "replacement_times_years":replacement_times,
        "replacement_present_value_usd2022":pv_replacements,
        "annualized_initial_and_replacement_capital_usd2022":capital_annual,
        "capital_component_usd2022_per_kg_delivered_h2":capital_annual/delivered,
        "separate_wholesale_electricity_eur2023_per_kg_delivered_h2":(
            observed["annual_net_wholesale_settlement_eur"]/delivered),
        "boundary_warning":(
            "NEITHER a complete LCOH nor a mixed-currency sum. DOE US"
            "2022 USD installed capital scenario + modelled 2023 Dutch"
            " wholesale electricity in nominal EUR are separate."
            " Modelled efficiency differs from DOE 57 kWh/kg and"
            " should not be portrayed as DOE-equivalent technology."
        ),
    }
