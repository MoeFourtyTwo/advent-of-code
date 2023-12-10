from __future__ import annotations

import pathlib
import sys

import numpy as np
import numpy.typing as npt

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def expand(path: npt.NDArray[np.int_, np.int_], x: int, y: int) -> None:
    try:
        if path[x, y] == 0:
            path[x, y] = -1
            expand(path, x - 1, y - 1)
            expand(path, x - 1, y)
            expand(path, x - 1, y + 1)
            expand(path, x, y - 1)
            expand(path, x, y + 1)
            expand(path, x + 1, y - 1)
            expand(path, x + 1, y)
            expand(path, x + 1, y + 1)

    except IndexError:
        pass


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    data = np.array([list(line) for line in lines])
    data = np.pad(data, 1, constant_values=".")

    ([row], [column]) = np.where(data == "S")

    path = np.zeros_like(data, dtype=int)

    last_row, last_column = row, column
    distance = 0

    while data[row, column] != "S" or distance == 0:
        current_pos_cache = (row, column)
        distance += 1
        path[row, column] = 1
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
                if data[row + 1, column] in ("|", "L", "J"):
                    row += 1
                elif data[row, column + 1] in ("-", "J", "7"):
                    column += 1
                elif data[row - 1, column] in ("-", "L", "F"):
                    row -= 1
                else:
                    column -= 1
        last_row, last_column = current_pos_cache

    sys.setrecursionlimit(142 * 142)
    expand(path, 0, 0)

    cleaned_data = np.zeros_like(data, dtype=str)
    cleaned_data[path == 1] = data[path == 1]

    positions = np.where(path == 0)

    inner_count = 0
    for row, column in zip(*positions):
        prev = "".join(cleaned_data[:row, column])
        prev = prev.replace("|", "")
        prev = prev.replace("FL", "")
        prev = prev.replace("7J", "")
        prev = prev.replace("FJ", "-")
        prev = prev.replace("7L", "-")
        prev = prev.replace("7L", "-")
        inner_count += len(prev) % 2

    return inner_count
