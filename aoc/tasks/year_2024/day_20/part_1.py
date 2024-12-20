from __future__ import annotations

import pathlib

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
    step_map: dict[complex, int] = {current: 0}
    step = 0

    while current != goal:
        for direction in DIRECTIONS.values():
            if direction * -1 == current_direction:
                continue

            if current + direction in positions:
                current += direction
                current_direction = direction
                steps.append(current)
                step += 1
                step_map[current] = step
                break
        else:
            raise ValueError("No path found")

    valid_cheats = 0

    for index, position in enumerate(steps):
        for direction in DIRECTIONS.values():
            if position + direction in positions:
                continue

            if (target_position := position + 2 * direction) not in positions:
                continue

            skip_step = step_map[target_position]

            saving = skip_step - index - 2

            if saving >= min_saving:
                valid_cheats += 1

    return valid_cheats
