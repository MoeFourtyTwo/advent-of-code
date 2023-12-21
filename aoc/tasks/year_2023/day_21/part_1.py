from __future__ import annotations

import pathlib

import numpy as np

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH, steps: int = 64):
    lines = get_lines(path)

    data = np.array([list(line.replace(".", "0").replace("#", "1").replace("S", "2")) for line in lines], dtype=int)
    data = np.pad(data, 1, constant_values=1)

    ([start_row], [start_col]) = np.where(data == 2)

    visited = {(start_row, start_col)}
    reachable_even_step = {(start_row, start_col)}
    reachable_odd_step = set()
    border = {(start_row, start_col)}

    for i in range(1, steps + 1):
        possible_locations = set(
            (new_row, new_col)
            for row, col in border
            for row_offset, col_offset in ((-1, 0), (1, 0), (0, -1), (0, 1))
            if data[new_row := row + row_offset][new_col := col + col_offset] != 1 and (new_row, new_col) not in visited
        )

        if i % 2 == 0:
            reachable_even_step.update(possible_locations)
        else:
            reachable_odd_step.update(possible_locations)

        visited.update(possible_locations)
        border = possible_locations

    return len(reachable_even_step) if steps % 2 == 0 else len(reachable_odd_step)
