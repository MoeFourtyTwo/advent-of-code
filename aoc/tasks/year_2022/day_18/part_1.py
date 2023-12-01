from __future__ import annotations

import pathlib
from operator import itemgetter

import numpy as np
from loguru import logger
from scipy.ndimage import convolve

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)
    points = [tuple(map(int, line.split(","))) for line in lines]
    x_max, y_max, z_max = [max(points, key=itemgetter(i))[i] for i in range(3)]
    cubes = np.zeros(shape=(x_max + 1, y_max + 1, z_max + 1))

    for point in points:
        cubes[*point] = 1

    kernel = [
        [[0, 0, 0], [0, -1, 0], [0, 0, 0]],
        [[0, -1, 0], [-1, 6, -1], [0, -1, 0]],
        [[0, 0, 0], [0, -1, 0], [0, 0, 0]],
    ]
    surfaces = np.clip(convolve(cubes, kernel, mode="constant", cval=0), 0, 6)

    total_surface = int(np.sum(surfaces, axis=None))
    logger.info(f"{total_surface=}")
    return total_surface
