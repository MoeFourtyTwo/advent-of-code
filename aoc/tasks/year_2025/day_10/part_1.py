from __future__ import annotations

import pathlib
from collections import defaultdict

import z3

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def compute_min_steps(line: str) -> int:
    indicator_str, *button_wiring_str_list, joltage_requirement_str = line.split(" ")

    optimizer = z3.Optimize()

    all_button_press_counts = []
    wiring_map = defaultdict(list)

    for idx, button_wiring_str in enumerate(button_wiring_str_list):
        button_press_count = z3.Int(f"button_count_{idx}")
        optimizer.add(button_press_count >= 0)
        all_button_press_counts.append(button_press_count)

        for v in map(int, button_wiring_str[1:-1].split(",")):
            wiring_map[v].append(button_press_count)

    for indicator_idx, button_press_counts in wiring_map.items():
        optimizer.add(z3.Sum(button_press_counts) % 2 == int(indicator_str[indicator_idx + 1] == "#"))

    cost = z3.Int("cost")

    optimizer.add(cost == z3.Sum(all_button_press_counts))

    optimizer.minimize(cost)
    if optimizer.check() == z3.unsat:
        return 0

    return optimizer.model()[cost].as_long()


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    return sum(compute_min_steps(line) for line in lines)
