from __future__ import annotations

import pathlib

from rich.progress import track

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)

DIRECTIONS = {"N": complex(0, -1), "E": complex(1, 0), "S": complex(0, 1), "W": complex(-1, 0)}


@timeit
def go(path: pathlib.Path = DATA_PATH, min_saving: int = 100) -> int:
    lines = get_lines(path)

    positions = set()
    start = complex(0, 0)
    goal = complex(0, 0)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != "#":
                positions.add(complex(x, y))
            if char == "S":
                start = complex(x, y)
            if char == "E":
                goal = complex(x, y)

    current = start
    current_direction = next(direction for direction in DIRECTIONS.values() if current + direction in positions)

    steps = [current]

    while current != goal:
        for direction in DIRECTIONS.values():
            if direction * -1 == current_direction:
                continue

            if current + direction in positions:
                current += direction
                current_direction = direction
                steps.append(current)
                break
        else:
            raise ValueError("No path found")

    valid_cheats = 0

    for index, position in enumerate(track(steps)):
        for second_index, second_position in enumerate(steps[index:], start=index):
            distance = abs(second_position.real - position.real) + abs(second_position.imag - position.imag)
            if distance > 20:
                continue

            time_saved = second_index - index - distance

            if time_saved >= min_saving:
                valid_cheats += 1

    return valid_cheats
