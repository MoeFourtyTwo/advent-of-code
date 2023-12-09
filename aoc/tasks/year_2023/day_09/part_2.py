from __future__ import annotations

import pathlib

import numpy as np
import numpy.typing as npt

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def extrapolate(array: npt.NDArray[np.int_]) -> int:
    if np.all(array == 0):
        return 0

    return array[0] - extrapolate(array[1:] - array[:-1])


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    sequences = [np.array(line.split(), dtype=int) for line in lines]

    return sum(map(extrapolate, sequences))
