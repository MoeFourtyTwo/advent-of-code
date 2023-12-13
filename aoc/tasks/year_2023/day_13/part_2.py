from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def count_errors(left: str, right: str) -> int:
    return sum(l != r for l, r in zip(left, right))


def check_axis(data: list[str], index: int) -> bool:
    total_errors = 0
    for index_a, index_b in zip(range(index - 1, -1, -1), range(index, len(data))):
        total_errors += count_errors(data[index_a], data[index_b])

        if total_errors > 1:
            return False

    return total_errors == 1


def find_axis(data: list[str]) -> int:
    for i in range(len(data)):
        if check_axis(data, i):
            return i
    return 0


def transpose(data: list[str]) -> list[str]:
    return ["".join(row[i] for row in data) for i in range(len(data[0]))]


def score_board(data: list[str]) -> int:
    return 100 * find_axis(data) + find_axis(transpose(data))


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path) + [""]

    arrays = []
    current_array = []
    for line in lines:
        if line:
            current_array.append(line)
        else:
            arrays.append(current_array)
            current_array = []

    return sum(score_board(board) for board in arrays)
