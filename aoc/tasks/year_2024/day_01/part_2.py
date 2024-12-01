from __future__ import annotations

import pathlib
from collections import Counter

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    left_numbers, right_numbers = map(list, zip(*[list(map(int, line.split())) for line in lines]))

    counted_numbers = Counter(right_numbers)

    result = sum(
        counted_numbers[left_number] * left_number if left_number in counted_numbers else 0
        for left_number in left_numbers
    )

    return result
