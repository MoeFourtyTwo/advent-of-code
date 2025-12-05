from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    input_ranges = []

    for line in lines:
        if not line:
            break
        lower_bound, upper_bound = map(int, line.split("-"))
        input_ranges.append((lower_bound, upper_bound))

    input_ranges = sorted(input_ranges)

    condensed_ranges = []
    current_range = input_ranges.pop(0)

    while input_ranges:
        next_candidate = input_ranges.pop(0)

        if current_range[1] >= next_candidate[0]:
            current_range = (current_range[0], max(current_range[1], next_candidate[1]))
        else:
            condensed_ranges.append(current_range)
            current_range = next_candidate

    if condensed_ranges[-1] != current_range:
        condensed_ranges.append(current_range)

    return sum(upper - lower + 1 for lower, upper in condensed_ranges)
