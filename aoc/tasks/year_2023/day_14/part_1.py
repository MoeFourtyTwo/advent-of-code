from __future__ import annotations

import pathlib

import numpy as np
import numpy.typing as npt

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def order_col(data: npt.NDArray[int]) -> npt.NDArray[int]:
    [bolder_indexes] = np.where(data == 2)

    for lower, upper in zip(bolder_indexes, bolder_indexes[1:]):
        data[lower:upper] = np.sort(data[lower:upper])[::-1]

    return data


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    data = np.array([list(line.replace(".", "0").replace("O", "1").replace("#", "2")) for line in lines], dtype=int)
    data = np.pad(data, 1, constant_values=2)

    for index in range(1, data.shape[1]):
        data[:, index] = order_col(data[:, index])

    data = np.flip(data, axis=0)

    total_load = sum(np.where(data == 1)[0])
    return total_load
