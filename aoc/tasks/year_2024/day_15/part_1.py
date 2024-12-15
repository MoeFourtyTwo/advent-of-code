from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


DIRECTIONS = {"<": complex(-1, 0), ">": complex(1, 0), "^": complex(0, -1), "v": complex(0, 1)}


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    grid = {}

    pos = complex(-1, -1)

    instructions = ""

    parse_grid = True
    for y, line in enumerate(lines):
        if not line:
            parse_grid = False
            continue

        if parse_grid:
            for x, char in enumerate(line):
                if char == "@":
                    pos = complex(x, y)
                elif char != ".":
                    grid[complex(x, y)] = char
        else:
            instructions += line

    for instruction in instructions:
        new_pos = pos + DIRECTIONS[instruction]

        if new_pos not in grid:
            pos = new_pos
            continue

        if grid[new_pos] == "#":
            continue

        possible_gap = new_pos
        while True:
            possible_gap = possible_gap + DIRECTIONS[instruction]
            if possible_gap not in grid:
                # gap found:
                grid[possible_gap] = "O"
                del grid[new_pos]
                pos = new_pos
                break

            if possible_gap in grid and grid[possible_gap] == "#":
                # no gap and pushing impossible
                break

    result = 0
    for pos, value in grid.items():
        if value != "O":
            continue

        result += 100 * pos.imag + pos.real

    return int(result)
