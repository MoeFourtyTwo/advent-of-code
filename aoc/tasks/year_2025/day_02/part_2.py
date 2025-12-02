from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def next_candidate(n: int, repeats: int) -> int:
    while (count := len(str(n))) % repeats != 0:
        n = 10**count

    as_str = str(n)
    parts = []

    segment_length = len(as_str) // repeats

    while as_str:
        parts.append(as_str[:segment_length])
        as_str = as_str[segment_length:]

    if all(part == parts[0] for part in parts[1:]):
        parts[0] = str(int(parts[0]) + 1)

    return int(parts[0] * repeats)


def sum_invalid_ids(lower_bound: int, upper_bound: int) -> int:
    invalid_nums = set()

    for repeats in range(2, len(str(upper_bound)) + 1):
        current = next_candidate(lower_bound - 1, repeats)

        while current <= upper_bound:
            if current >= lower_bound:
                invalid_nums.add(current)
            current = next_candidate(current, repeats)

    return sum(invalid_nums)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    [line] = get_lines(path)

    total = 0
    for bounds in line.split(","):
        lower_bound, upper_bound = map(int, bounds.split("-"))
        total += sum_invalid_ids(lower_bound, upper_bound)

    return total
