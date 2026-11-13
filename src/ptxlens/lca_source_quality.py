"""Scientific gate for the actual published USLCI PEM electrolysis foreground.

Uses elemental conservation and source flow direction/units. Flags a published
dataset inconsistency; NEVER silently changes original provider or O2 quantity.
"""
from __future__ import annotations
import math

M_H2=2*1.008
M_O2=2*15.999
STOICH_O2_PER_H2=M_O2/(2*M_H2)
STOICH_WATER_PER_H2=(M_O2+2*M_H2)/(2*M_H2)


def inventory_stoichiometry_check(exchanges):
    def get(name, is_input):
        matching=[
            r for r in exchanges if
            r.get("flow",{}).get("name")==name and
            r.get("input") is is_input and
            r.get("unit",{}).get("name")=="kg"
        ]
        if len(matching)!=1:
            raise ValueError(f"must match exactly one source flow {name}, input={is_input}")
        amount=matching[0].get("amount")
        if (isinstance(amount,bool) or not isinstance(amount,(int,float))
                or not math.isfinite(amount) or amount<=0):
            raise ValueError(f"invalid published source mass: {name}")
        return float(amount)
    h2=get("Hydrogen; at plant",False)
    o2=get("Oxygen",False)
    water=get("Water; process;,deionized",True)
    expected_o2=STOICH_O2_PER_H2*h2
    expected_water=STOICH_WATER_PER_H2*h2
    mass_error=water-(h2+o2)
    ratio_error=o2-expected_o2
    consistent=(abs(ratio_error)<=0.05*h2 and water>=expected_water*.98)
    return {
        "calculation":"2 H2O -> 2 H2 + O2; approximate atomic weights 1.008 and 15.999",
        "original_source_water_kg":water,
        "original_source_hydrogen_output_kg":h2,
        "original_source_oxygen_output_kg":o2,
        "theoretical_oxygen_kg_for_source_h2":expected_o2,
        "theoretical_reacted_water_kg_for_source_h2":expected_water,
        "original_reported_oxygen_minus_stoichiometric_kg":ratio_error,
        "unbalanced_input_minus_output_mass_kg":mass_error,
        "elemental_stoichiometry_reconciled":consistent,
        "interpretation":"source output warrants study-level verification of water/oxygen and any missing feed/product. The raw source is not edited.",
        "blocks_complete_product_lca":not consistent,
    }
