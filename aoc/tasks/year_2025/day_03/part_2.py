from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def extract_joltage(line: str) -> int:
    number_array = list(map(int, line))

    digits = []

    front_offset = 0
    for back_offset in range(len(number_array) - 11, len(number_array) + 1):
        max_index, digit = max(enumerate(number_array[front_offset:back_offset]), key=lambda x: x[1])
        digits.append(digit)
        front_offset = max_index + 1 + front_offset

    return int("".join(map(str, digits)))


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    return sum(extract_joltage(line) for line in lines)
