from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


NEXT_DIRECTION = {
    complex(0, -1): complex(1, 0),
    complex(1, 0): complex(0, 1),
    complex(0, 1): complex(-1, 0),
    complex(-1, 0): complex(0, -1),
}


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    y_max = len(lines)
    x_max = len(lines[0])

    obstacles = set()

    current_position = complex(0, 0)
    current_direction = complex(0, -1)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == ".":
                continue
            if char == "#":
                obstacles.add(complex(x, y))
            else:
                current_position = complex(x, y)

    visited = {current_position}

    while True:
        possible_position = current_position + current_direction

        if possible_position in obstacles:
            current_direction = NEXT_DIRECTION[current_direction]
            continue

        x, y = possible_position.real, possible_position.imag

        if x < 0 or x >= x_max or y < 0 or y >= y_max:
            return len(visited)

        current_position = possible_position
        visited.add(current_position)
