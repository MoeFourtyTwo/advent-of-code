from __future__ import annotations

import pathlib

import numpy as np
from rich.progress import track
from scipy.stats import entropy

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH, x_max: int = 101, y_max: int = 103) -> int:
    lines = get_lines(path)

    data = []
    for line in lines:
        init_x, init_y, v_x, v_y = map(int, line[2:].replace("v=", ",").split(","))
        data.append((init_x, init_y, v_x, v_y))

    positions = []

    for t in track(range(10000)):
        positions.append(set())
        for init_x, init_y, v_x, v_y in data:
            final_pos = simulate(init_x, init_y, v_x, v_y, x_max, y_max, t)
            positions[t].add(final_pos)

    entropies = []

    for positions_set in track(positions):
        grid = np.zeros((x_max, y_max))
        for pos in positions_set:
            grid[pos] = 1

        flattened = grid.flatten()
        values, counts = np.unique(flattened, return_counts=True)
        probabilities = counts / counts.sum()
        shannon_entropy = entropy(probabilities, base=2)

        entropies.append(shannon_entropy)

    timestep = int(np.argmax(entropies))

    return timestep


def simulate(init_x: int, init_y: int, v_x: int, v_y: int, x_max: int, y_max: int, step: int) -> tuple[int, int]:
    final_x = (init_x + step * v_x) % x_max
    final_y = (init_y + step * v_y) % y_max

    return final_x, final_y
