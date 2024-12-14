from __future__ import annotations

import functools
import operator
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH, x_max: int = 101, y_max: int = 103) -> int:
    lines = get_lines(path)

    positions = []

    for line in lines:
        init_x, init_y, v_x, v_y = map(int, line[2:].replace("v=", ",").split(","))
        final_pos = simulate(init_x, init_y, v_x, v_y, x_max, y_max, 100)
        positions.append(final_pos)

    quadrant_counts = [0, 0, 0, 0]

    x_mid = x_max // 2
    y_mid = y_max // 2

    for pos in positions:
        if pos[0] < x_mid:
            if pos[1] < y_mid:
                quadrant_counts[0] += 1
            elif pos[1] > y_mid:
                quadrant_counts[1] += 1
        elif pos[0] > x_mid:
            if pos[1] < y_mid:
                quadrant_counts[2] += 1
            elif pos[1] > y_mid:
                quadrant_counts[3] += 1

    return functools.reduce(operator.mul, quadrant_counts, 1)


def simulate(init_x: int, init_y: int, v_x: int, v_y: int, x_max: int, y_max: int, step: int) -> tuple[int, int]:
    final_x = (init_x + step * v_x) % x_max
    final_y = (init_y + step * v_y) % y_max

    return final_x, final_y
