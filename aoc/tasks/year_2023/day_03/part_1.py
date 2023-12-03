from __future__ import annotations

import itertools
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def is_special(lines: list[str], x: int, y: int) -> bool:
    try:
        return not lines[y][x].isdigit() and not lines[y][x] == "."
    except IndexError:
        return False


def check_perimeter(width: int, lines: list[str], x: int, y: int) -> bool:
    return any(
        itertools.chain(
            [is_special(lines, x, y), is_special(lines, x - width - 1, y)],
            (is_special(lines, x_cursor, y - 1) for x_cursor in range(x - width - 1, x + 1)),
            (is_special(lines, x_cursor, y + 1) for x_cursor in range(x - width - 1, x + 1)),
        )
    )


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    total = 0

    current_number_string = ""
    found_digit = False

    for y, line in enumerate(lines):
        for x, char in enumerate(line + "."):
            if char.isdigit():
                current_number_string += char
                found_digit = True
            elif found_digit:
                if check_perimeter(len(current_number_string), lines, x, y):
                    total += int(current_number_string)

                current_number_string = ""
                found_digit = False

    return total
