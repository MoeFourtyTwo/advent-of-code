from __future__ import annotations

import pathlib
from typing import Annotated

import numpy as np
from numpy.typing import NDArray

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)

Array2DInt = Annotated[NDArray[np.int_], (..., ...)]


class Solver:
    def __init__(self, width: int, height: int, shapes: dict[int, Array2DInt]) -> None:
        self.grid: Array2DInt = np.zeros((width, height), dtype=int)

    def reset(self) -> None:
        self.grid.fill(0)

    def solve(self, number_of_shapes: list[int]) -> bool:
        always_fit = self.grid.shape[0] // 3 * self.grid.shape[1] // 3

        if sum(number_of_shapes) <= always_fit:
            return True

        return False


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    shapes = {}

    current_shape = []
    current_id = 0

    targets = []

    for line in lines:
        if not line:
            shapes[current_id] = np.array(current_shape)
            current_shape = []
            continue

        if "x" in line:
            targets.append(line)
            continue

        if line[0].isdigit():
            current_id = int(line.replace(":", ""))
            continue

        current_shape.append([0 if char == "." else 1 for char in line])

    count = 0
    for target in targets:
        left, right = target.split(": ")
        width, height = map(int, left.split("x"))
        number_of_shapes = list(map(int, right.split(" ")))

        solver = Solver(width, height, shapes)

        if solver.solve(number_of_shapes):
            count += 1

    return count
