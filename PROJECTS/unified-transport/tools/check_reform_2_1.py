#!/usr/bin/env python3
"""Reproducible *arithmetic* check of author's Transport Reform 2.1 assumptions.

This is NOT a feasibility study or current price estimate. Values come from
the author's 64-page document. No network, external packages or personal data.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Mapping, Tuple

Range = Tuple[float, float]

# Billions of roubles (bn RUB), as stated in section 24 of source.
CAPEX_BN: Mapping[str, Range] = {
    "bus_fleet": (6.0, 21.0),
    "depot_energy_centres": (4.5, 12.0),
    "local_charging_nodes": (0.3, 2.0),
    "energy_storage": (1.0, 4.0),
    "grid_connection": (3.0, 10.0),
    "digital_infrastructure": (1.0, 3.0),
}
STATED_CAPEX_BN: Range = (15.0, 50.0)
# Operating line items, bn RUB per year.
FLEET_MAINTENANCE_FRACTION: Range = (0.08, 0.15)
OPEX_BN_PER_YEAR: Mapping[str, Range] = {
    "electricity": (0.8, 2.0),
    "personnel": (2.0, 4.0),
    "it_and_administration": (0.3, 1.0),
}
STATED_OPEX_BN_PER_YEAR: Range = (3.0, 7.0)
ENERGY_GRID_DEPOTS: Range = (5.0, 20.0)  # MW per depot
ENERGY_GRID_LOCAL_NODES: Range = (0.5, 3.0)  # MW per node
DEPOT_COUNT: int = 3
LOCAL_NODE_COUNTS: Tuple[int, int] = (6, 10)
NIGHT_AND_DAY_HOURS_PER_WEEK: int = 24 * 7
DAY_HOURS_PER_WEEK: int = 18 * 7
PAID_SHIFT_HOURS: float = 6.0
SHIFTS_PER_EMPLOYEE_PER_WEEK: int = 5


def add_ranges(values: Mapping[str, Range]) -> Range:
    """Independent envelope, NOT a consistent joint scenario."""
    if not values:
        raise ValueError("Expected at least one range")
    for name, (lo, hi) in values.items():
        if lo < 0 or hi < lo:
            raise ValueError("Invalid range: " + name)
    return (round(sum(lo for lo, _ in values.values()), 5),
            round(sum(hi for _, hi in values.values()), 5))


@dataclass(frozen=True)
class Audit:
    units: str
    capex_component_envelope_bn: Range
    capex_stated_bn: Range
    capex_gap_bn: Range
    annual_maintenance_from_fleet_bn: Range
    annual_opex_component_envelope_bn: Range
    annual_opex_stated_bn: Range
    annual_opex_gap_bn: Range
    depot_and_local_node_power_envelope_mw: Range
    day_driver_posts_fte_lower_bound: float
    round_the_clock_driver_posts_fte_lower_bound: float
    note: str


def audit() -> Audit:
    capex = add_ranges(CAPEX_BN)
    maintained = (CAPEX_BN["bus_fleet"][0] * FLEET_MAINTENANCE_FRACTION[0],
                  CAPEX_BN["bus_fleet"][1] * FLEET_MAINTENANCE_FRACTION[1])
    opex = add_ranges({**OPEX_BN_PER_YEAR, "fleet": maintained})
    power = (DEPOT_COUNT * ENERGY_GRID_DEPOTS[0] +
             LOCAL_NODE_COUNTS[0] * ENERGY_GRID_LOCAL_NODES[0],
             DEPOT_COUNT * ENERGY_GRID_DEPOTS[1] +
             LOCAL_NODE_COUNTS[1] * ENERGY_GRID_LOCAL_NODES[1])
    weekly_work = PAID_SHIFT_HOURS * SHIFTS_PER_EMPLOYEE_PER_WEEK
    return Audit(
        units="bn RUB, bn RUB/year, MW, theoretical FTE per continuously occupied driver post",
        capex_component_envelope_bn=capex,
        capex_stated_bn=STATED_CAPEX_BN,
        capex_gap_bn=(round(capex[0] - STATED_CAPEX_BN[0], 5),
                      round(capex[1] - STATED_CAPEX_BN[1], 5)),
        annual_maintenance_from_fleet_bn=tuple(round(x, 5) for x in maintained),
        annual_opex_component_envelope_bn=opex,
        annual_opex_stated_bn=STATED_OPEX_BN_PER_YEAR,
        annual_opex_gap_bn=(round(opex[0] - STATED_OPEX_BN_PER_YEAR[0], 5),
                            round(opex[1] - STATED_OPEX_BN_PER_YEAR[1], 5)),
        depot_and_local_node_power_envelope_mw=(round(power[0], 5), round(power[1], 5)),
        day_driver_posts_fte_lower_bound=round(DAY_HOURS_PER_WEEK / weekly_work, 5),
        round_the_clock_driver_posts_fte_lower_bound=round(
            NIGHT_AND_DAY_HOURS_PER_WEEK / weekly_work, 5
        ),
        note=("Ranges are arithmetic envelopes of independently chosen endpoints, "
              "not independently validated budgets; FTE excludes breaks, training, "
              "leave, replacement time and other staffing constraints."),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print machine-readable audit")
    args = parser.parse_args()
    report = asdict(audit())
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for key, value in report.items():
            print(key + ": " + str(value))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
