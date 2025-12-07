from __future__ import annotations

import functools
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


DOWN = complex(0, 1)
LEFT = complex(-1, 0)
RIGHT = complex(1, 0)


@functools.cache
def calc_number_of_paths(position: complex, splitters: frozenset[complex], max_depth: int) -> int:
    if position.imag >= max_depth:
        return 1

    if position + DOWN in splitters:
        return calc_number_of_paths(
            position + DOWN + LEFT,
            splitters,
            max_depth,
        ) + calc_number_of_paths(
            position + DOWN + RIGHT,
            splitters,
            max_depth,
        )
    return calc_number_of_paths(position + DOWN, splitters, max_depth)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    splitters = set()
    initial_position = complex(00, 0)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "^":
                splitters.add(complex(x, y))
            if char == "S":
                initial_position = complex(x, y)

    max_depth = len(lines)

    return calc_number_of_paths(initial_position, frozenset(splitters), max_depth)
