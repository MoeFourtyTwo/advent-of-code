from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    new_ranges = set()

    it = iter(lines)

    for line in it:
        if not line:
            break
        lower_bound, upper_bound = map(int, line.split("-"))
        new_ranges.add((lower_bound, upper_bound))

    cleansed_ranges = set()

    while new_ranges:
        current_lower, current_upper = new_ranges.pop()

        added = False
        new_cleansed_ranges = set()
        while cleansed_ranges:
            other_lower, other_upper = cleansed_ranges.pop()

            overlapping = max(current_lower, other_lower) <= min(current_upper, other_upper)

            if overlapping:
                added = True
                lower = min(current_lower, other_lower)
                upper = max(current_upper, other_upper)
                new_ranges.add((lower, upper))
                break

            new_cleansed_ranges.add((other_lower, other_upper))

        if not added:
            new_cleansed_ranges.add((current_lower, current_upper))

        cleansed_ranges |= new_cleansed_ranges

    return sum(upper - lower + 1 for lower, upper in cleansed_ranges)
