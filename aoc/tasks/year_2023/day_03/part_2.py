from __future__ import annotations

import itertools
import pathlib
from collections import defaultdict

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def is_gear(lines: list[str], x: int, y: int) -> tuple[bool, tuple[int, int]]:
    try:
        return lines[y][x] == "*", (x, y)
    except IndexError:
        return False, (-1, -1)


def check_perimeter(width: int, lines: list[str], x: int, y: int) -> tuple[bool, tuple[int, int]]:
    for gear, position in itertools.chain(
        [is_gear(lines, x, y), is_gear(lines, x - width - 1, y)],
        (is_gear(lines, x_cursor, y - 1) for x_cursor in range(x - width - 1, x + 1)),
        (is_gear(lines, x_cursor, y + 1) for x_cursor in range(x - width - 1, x + 1)),
    ):
        if gear:
            return gear, position
    return False, (-1, -1)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    current_number_string = ""
    found_digit = False

    found_gear_ratios = defaultdict(list)

    for y, line in enumerate(lines):
        for x, char in enumerate(line + "."):
            if char.isdigit():
                current_number_string += char
                found_digit = True
            elif found_digit:
                gear, position = check_perimeter(len(current_number_string), lines, x, y)
                if gear:
                    found_gear_ratios[position].append(int(current_number_string))

                current_number_string = ""
                found_digit = False

    total = sum([x[0] * x[1] for x in found_gear_ratios.values() if len(x) == 2])

    return total
