from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> None:
    lines = get_lines(path)

    next_x = 1
    register_values = []

    for line in lines:
        match line.split():
            case ["noop"]:
                register_values += [next_x]
            case ["addx", value]:
                register_values += [next_x, next_x]
                next_x += int(value)

    screen = ""
    offset = 0
    for cursor, register_value in enumerate(register_values, start=1):
        if cursor in (register_value + offset * 40, register_value + 1 + offset * 40, register_value + 2 + offset * 40):
            screen += "#"
        else:
            screen += "."

        if cursor % 40 == 0:
            screen += "\n"
            offset += 1

    print(screen)
