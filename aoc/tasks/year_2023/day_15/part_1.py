from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def calc_hash(data: str) -> int:
    current_value = 0
    for char in data:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    [line] = get_lines(path)

    return sum(map(calc_hash, line.split(",")))
