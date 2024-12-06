from __future__ import annotations

import pathlib

from rich.progress import track

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

    possible_obstacles = set()

    current_position = complex(0, 0)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == ".":
                continue
            if char == "#":
                obstacles.add(complex(x, y))
            else:
                current_position = complex(x, y)

    possible_obstacles = {p[0] for p in has_circle(current_position, obstacles, x_max, y_max)[1]}

    return sum(
        has_circle(current_position, obstacles | {possible_obstacle}, x_max, y_max)[0]
        for possible_obstacle in track(possible_obstacles)
    )


def has_circle(
    current_position: complex, obstacles: set[complex], x_max: int, y_max: int
) -> tuple[bool, set[tuple[complex, complex]]]:
    current_direction = complex(0, -1)
    visited = {(current_position, current_direction)}
    while True:
        possible_position = current_position + current_direction

        if possible_position in obstacles:
            current_direction = NEXT_DIRECTION[current_direction]
            continue

        x, y = possible_position.real, possible_position.imag

        if x < 0 or x >= x_max or y < 0 or y >= y_max:
            return False, visited

        current_position = possible_position

        if (current_position, current_direction) in visited:
            return True, set()

        visited.add((current_position, current_direction))
