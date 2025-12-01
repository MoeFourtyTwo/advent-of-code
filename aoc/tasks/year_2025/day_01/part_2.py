from __future__ import annotations

import pathlib
import typing

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


MAX_VALUE = 100


def rotate(initial_value: int, steps: int, direction: typing.Literal["L", "R"]) -> tuple[int, int]:
    zeros = 0
    if direction == "L":
        value = initial_value - steps
        while value < 0:
            value += MAX_VALUE
            zeros += 1
        if value == 0 and steps > 0:
            zeros += 1
        if initial_value == 0 and steps > 0:
            zeros -= 1

    elif direction == "R":
        value = initial_value + steps
        while value >= MAX_VALUE:
            value -= MAX_VALUE
            zeros += 1
    else:
        raise ValueError(f"Unknown direction: {direction}")

    return value, zeros


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    value = 50

    password = 0

    for line in lines:
        value, clicks = rotate(value, int(line[1:]), line[0])
        password += clicks

    return password
