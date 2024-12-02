from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    safe = 0

    for line in lines:
        values = list(map(int, line.split()))

        if is_safe(values):
            safe += 1
            continue

        # remove one and check
        for i in range(len(values)):
            if is_safe(values[:i] + values[i + 1 :]):
                safe += 1
                break

    return safe


def is_safe(values: list[int]) -> bool:
    differences = {left - right for left, right in zip(values[1:], values[:-1])}
    return all(difference in {1, 2, 3} for difference in differences) or all(
        difference in {-1, -2, -3} for difference in differences
    )
