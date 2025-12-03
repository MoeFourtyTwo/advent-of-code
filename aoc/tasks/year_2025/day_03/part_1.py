from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def extract_joltage(line: str) -> int:
    number_array = list(map(int, line))
    max_index, first_digit = max(enumerate(number_array[:-1]), key=lambda x: x[1])
    second_digit = max(number_array[max_index + 1 :])
    return first_digit * 10 + second_digit


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    return sum(extract_joltage(line) for line in lines)
