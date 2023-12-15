from __future__ import annotations

import enum
import pathlib

import numpy as np
import numpy.typing as npt
from tqdm import trange

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

TARGET_CYCLES = 1_000_000_000

DATA_PATH = get_data_path(__file__)


def order_col(data: npt.NDArray[int]) -> npt.NDArray[int]:
    [bolder_indexes] = np.where(data == 2)

    for lower, upper in zip(bolder_indexes, bolder_indexes[1:]):
        data[lower:upper] = np.sort(data[lower:upper])[::-1]

    return data


def hash_board(data: npt.NDArray[int]) -> int:
    return hash(tuple(map(tuple, np.where(data == 1))))


def order_board(data: npt.NDArray[int, int]) -> npt.NDArray[int, int]:
    for index in range(1, data.shape[1]):
        data[:, index] = order_col(data[:, index])

    return data


def cycle(data: npt.NDArray[int, int]) -> npt.NDArray[int, int]:
    for _ in range(4):
        data = order_board(data)
        data = np.rot90(data, k=3)
    return data


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    data = np.array([list(line.replace(".", "0").replace("O", "1").replace("#", "2")) for line in lines], dtype=int)
    data = np.pad(data, 1, constant_values=2)

    hash_value = hash_board(data)
    seen = {hash_value: 0}

    i = 0
    for i in range(1, TARGET_CYCLES):
        data = cycle(data)
        hash_value = hash_board(data)

        if hash_value in seen:
            break

        seen[hash_value] = i

    start = seen[hash_value]
    length = i - start
    next_i = start + (TARGET_CYCLES - start) // length * length

    for _ in range(next_i, TARGET_CYCLES):
        data = cycle(data)

    data = np.flip(data, axis=0)
    total_load = sum(np.where(data == 1)[0])
    return total_load


if __name__ == "__main__":
    go()
