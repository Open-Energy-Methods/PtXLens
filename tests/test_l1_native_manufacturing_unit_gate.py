"""Independent synthetic dimensional-oracle checks; no native BAFU LCI shipped."""
import unittest
from ptxlens.l1_native_manufacturing_unit_gate import audit_manufacturing_functional_unit as audit

class NativeManufacturingUnitGateTests(unittest.TestCase):
    def setUp(self):
        self.row = dict(
            provider_id="synthetic-test-only",
            source_sha256="a" * 64,
            reference_flow_denominator="kg_empty_equipment",
            reference_flow_amount=1.0,
            manufacturing_process_scope="stationary_type_i_steel_vessel_manufacturing",
        )

    def test_synthetic_matching_structure_only(self):
        result = audit(self.row)
        self.assertTrue(result["passed"])
        self.assertIn("not native LCIA", result["claim_scope"])

    def test_composite_tank_h2_capacity_is_not_steel_equipment_mass(self):
        row = dict(self.row, reference_flow_denominator="kg_h2_nominal_capacity")
        result = audit(row)
        self.assertFalse(result["passed"])
        self.assertTrue(any("incompatible functional-unit" in x for x in result["findings"]))

    def test_steel_input_mass_is_not_empty_vessel_mass(self):
        row = dict(self.row, reference_flow_denominator="kg_steel_input")
        self.assertFalse(audit(row)["passed"])

    def test_unknown_provider_scope_and_hash_rejected(self):
        row = dict(self.row, provider_id="", source_sha256="unverified",
                   manufacturing_process_scope="automotive_composite_tank")
        result = audit(row)
        self.assertFalse(result["passed"])
        self.assertGreaterEqual(len(result["findings"]), 3)

    def test_nonfinite_zero_boolean_and_missing_amount_rejected(self):
        for amount in (0, -1, True, float("nan"), float("inf"), None):
            with self.subTest(amount=amount):
                self.assertFalse(audit(dict(self.row, reference_flow_amount=amount))["passed"])

    def test_missing_or_invalid_record_fails_closed(self):
        for record in (None, {}, []):
            with self.subTest(record=record):
                self.assertFalse(audit(record)["passed"])

    def test_no_implicit_unit_conversion(self):
        row = dict(self.row, reference_flow_denominator="unit_vessel")
        self.assertFalse(audit(row)["passed"])
        self.assertTrue(audit(row, required_denominator="unit_vessel")["passed"])

if __name__ == "__main__":
    unittest.main()
