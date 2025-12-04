from __future__ import annotations

import pathlib

import numpy as np
from scipy.signal import convolve2d

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)
    data = np.array([list(line.replace(".", "0").replace("@", "1")) for line in lines], dtype=int)

    kernel = np.array([[-1, -1, -1], [-1, 4, -1], [-1, -1, -1]])
    conv = convolve2d(data, kernel, mode="same", boundary="fill", fillvalue=0)
    result = (conv >= 1).astype(int)

    return np.sum(result)
