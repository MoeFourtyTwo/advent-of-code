from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    left_numbers, right_numbers = map(list, zip(*[list(map(int, line.split())) for line in lines]))

    result = sum(
        abs(left_number - right_number)
        for left_number, right_number in zip(sorted(left_numbers), sorted(right_numbers))
    )

    return result
