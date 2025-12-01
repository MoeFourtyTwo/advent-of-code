from __future__ import annotations

import pathlib
import typing

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


MAX_VALUE = 100


def rotate(initial_value: int, steps: int, direction: typing.Literal["L", "R"]) -> int:
    if direction == "L":
        return (initial_value - steps) % MAX_VALUE
    elif direction == "R":
        return (initial_value + steps) % MAX_VALUE
    else:
        raise ValueError(f"Unknown direction: {direction}")


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    value = 50

    password = 0

    for line in lines:
        value = rotate(value, int(line[1:]), line[0])
        if value == 0:
            password += 1

    return password
