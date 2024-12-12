from __future__ import annotations

import pathlib
from collections import defaultdict

import numpy as np

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    grid = np.genfromtxt(lines, delimiter=1, dtype=str)
    grid = np.pad(grid, pad_width=1, mode="constant", constant_values=".")

    visited = np.zeros_like(grid, dtype=bool)

    result = 0

    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            if visited[i, j]:
                continue

            visited[i, j] = True

            value = grid[i, j]
            area_size = 1
            perimeters = defaultdict(list)

            to_check = [(i + di, j + dj, (dj, di)) for di, dj in [(1, 0), (0, 1), (-1, 0), (0, -1)]]

            while to_check:
                x, y, d = to_check.pop()

                if grid[x, y] != value:
                    perimeters[d].append((x, y))
                    continue

                if visited[x, y]:
                    continue

                visited[x, y] = True
                area_size += 1
                to_check.extend([(x + di, y + dj, (dj, di)) for di, dj in [(1, 0), (0, 1), (-1, 0), (0, -1)]])

            result += area_size * count_edges(perimeters)

    return result


def count_edges(perimeters: dict[tuple[int, int], list[tuple[int, int]]]) -> int:
    edges = 0

    for (di, dj), values in perimeters.items():
        directions = {(di, dj), (-di, dj), (di, -dj), (-di, -dj)}

        while values:
            edges += 1
            x, y = values.pop()
            to_check = [(x + dx, y + dy) for dx, dy in directions]

            while to_check:
                x_, y_ = to_check.pop()
                if (x_, y_) in values:
                    values.remove((x_, y_))
                    to_check.extend([(x_ + dx, y_ + dy) for dx, dy in directions])
    return edges
