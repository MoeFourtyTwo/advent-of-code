from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

GRID = dict[complex, str]

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
            line = line.replace(".", "..").replace("#", "##").replace("O", "[]").replace("@", "@.")
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

        if instruction in ("<", ">"):
            grid, pos = push_horizontal(grid, instruction, pos)
        else:
            grid, pos = push_vertical(grid, instruction, pos)

    result = 0
    for pos, value in grid.items():
        if value != "[":
            continue

        result += 100 * pos.imag + pos.real

    return int(result)


def push_vertical(grid: GRID, instruction: str, pos: complex) -> tuple[GRID, complex]:
    new_pos = pos + DIRECTIONS[instruction]

    to_check = {
        new_pos,
        new_pos + (DIRECTIONS[">"] if grid[new_pos] == "[" else DIRECTIONS["<"]),
    }

    to_move = set()

    while to_check:
        to_check_pos = to_check.pop()
        to_move.add(to_check_pos)
        neighbour = to_check_pos + DIRECTIONS[instruction]
        if neighbour not in grid:
            # gap
            continue

        if grid[neighbour] == "#":
            # stone detected, impossible
            return grid, pos

        to_check.add(neighbour)
        to_check.add(neighbour + (DIRECTIONS[">"] if grid[neighbour] == "[" else DIRECTIONS["<"]))

    # overall gaps
    to_move = list(to_move)
    content = [grid[p] for p in to_move]

    # clean up dict
    for p in to_move:
        del grid[p]

    # move up
    for p, c in zip(to_move, content):
        grid[p + DIRECTIONS[instruction]] = c

    return grid, new_pos


def push_horizontal(grid: GRID, instruction: str, pos: complex) -> tuple[GRID, complex]:
    new_pos = pos + DIRECTIONS[instruction]
    possible_gap = new_pos
    to_move = [new_pos]
    while True:
        possible_gap = possible_gap + DIRECTIONS[instruction]
        if possible_gap not in grid:
            # gap found:
            content = []
            for p in to_move:
                content.append(grid[p])

                del grid[p]
            for p, c in zip(to_move, content):
                grid[p + DIRECTIONS[instruction]] = c

            pos = new_pos
            break

        if possible_gap in grid and grid[possible_gap] == "#":
            # no gap and pushing impossible
            break

        to_move.append(possible_gap)
    return grid, pos
