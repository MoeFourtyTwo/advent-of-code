from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def next_candidate(n: int) -> int:
    if (count := len(str(n))) % 2 != 0:
        n = 10**count

    as_str = str(n)
    first_half = int(as_str[: len(as_str) // 2])
    second_half = int(as_str[len(as_str) // 2 :])

    if first_half == second_half:
        first_half += 1

    return int(str(first_half) * 2)


def sum_invalid_ids(lower_bound: int, upper_bound: int) -> int:
    invalid_sum = 0

    current = next_candidate(lower_bound - 1)

    while current <= upper_bound:
        if current >= lower_bound:
            invalid_sum += current
        current = next_candidate(current)

    return invalid_sum


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    [line] = get_lines(path)

    total = 0
    for bounds in line.split(","):
        lower_bound, upper_bound = map(int, bounds.split("-"))
        total += sum_invalid_ids(lower_bound, upper_bound)

    return total
