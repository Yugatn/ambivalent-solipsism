"""Tests for the arithmetic checks; run: python3 -m unittest tools/test_check_reform_2_1.py

This test suite uses only the Python standard library and no live transport data.
"""
import unittest

from check_reform_2_1 import (
    CAPEX_BN,
    STATED_CAPEX_BN,
    add_ranges,
    audit,
)


class Reform21ArithmeticTests(unittest.TestCase):
    def test_capex_component_envelope(self):
        self.assertEqual(add_ranges(CAPEX_BN), (15.8, 52.0))

    def test_stated_capex_is_different(self):
        self.assertNotEqual(add_ranges(CAPEX_BN), STATED_CAPEX_BN)

    def test_opex_component_envelope(self):
        self.assertEqual(audit().annual_opex_component_envelope_bn, (3.58, 10.15))

    def test_opex_maintenance_range(self):
        self.assertEqual(audit().annual_maintenance_from_fleet_bn, (0.48, 3.15))

    def test_power_envelope_is_not_grid_connection(self):
        self.assertEqual(audit().depot_and_local_node_power_envelope_mw, (18.0, 90.0))

    def test_driver_post_lower_bounds(self):
        self.assertEqual(audit().day_driver_posts_fte_lower_bound, 4.2)
        self.assertEqual(audit().round_the_clock_driver_posts_fte_lower_bound, 5.6)

    def test_reject_invalid_range(self):
        with self.assertRaises(ValueError):
            add_ranges({"bad": (4.0, 3.0)})


if __name__ == "__main__":
    unittest.main()
