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
        differences = {left - right for left, right in zip(values[1:], values[:-1])}

        if all(difference in {1, 2, 3} for difference in differences):
            safe += 1

        if all(difference in {-1, -2, -3} for difference in differences):
            safe += 1

    return safe
