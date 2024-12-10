from __future__ import annotations

import pathlib
from collections import defaultdict

import numpy as np
from numpy.typing import NDArray

from aoc.common.decorators import timeit
from aoc.common.storage import get_as_array, get_data_path

DATA_PATH = get_data_path(__file__)

Point = tuple[int, int]


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    grid = get_as_array(path)

    grid = np.pad(grid, pad_width=1, mode="constant", constant_values=-2)

    score = 0

    known = defaultdict(set)
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            find_reachable_peaks(grid, known, (i, j))

            if grid[i, j] == 0:
                score += len(known[(i, j)])

    return score


def find_reachable_peaks(grid: NDArray[Point, np.int_], known: defaultdict[Point, set[Point]], position: Point) -> None:
    if position in known:
        return

    if grid[position] == 9:
        known[position].add(position)
        return

    for direction in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        new_position = (position[0] + direction[0], position[1] + direction[1])
        gradient = grid[new_position] - grid[position]

        if gradient != 1:
            continue

        if new_position not in known:
            find_reachable_peaks(grid, known, new_position)

        known[position].update(known[new_position])
