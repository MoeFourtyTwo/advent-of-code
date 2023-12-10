from __future__ import annotations

import pathlib

import numpy as np

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    data = np.array([list(line) for line in lines])
    data = np.pad(data, 1, constant_values=".")

    ([row], [column]) = np.where(data == "S")

    last_row, last_column = row, column
    distance = 0

    from_left = ("L", "-", "F")
    from_right = ("L", "-", "F")
    from_top = ("|", "L", "J")
    from_bot = ("7", "|", "F")

    while data[row, column] != "S" or distance == 0:
        current_pos_cache = (row, column)
        distance += 1
        match data[row, column]:
            case "|":
                row += row - last_row
            case "-":
                column += column - last_column
            case "L":
                if last_column == column:
                    column += 1
                else:
                    row -= 1
            case "J":
                if last_column == column:
                    column -= 1
                else:
                    row -= 1
            case "7":
                if last_column == column:
                    column -= 1
                else:
                    row += 1
            case "F":
                if last_column == column:
                    column += 1
                else:
                    row += 1
            case "S":
                if data[row + 1, column] in from_top:
                    row += 1
                elif data[row, column + 1] in from_right:
                    column += 1
                elif data[row, column - 1] in from_left:
                    column -= 1
                else:
                    row -= 1
        last_row, last_column = current_pos_cache

    return distance // 2
