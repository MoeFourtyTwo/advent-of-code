import pathlib

import numpy as np
from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_as_array, get_data_path

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    data = get_as_array(path)
    result = np.ones_like(data, dtype=bool)

    for row in range(data.shape[0]):
        compared = data[row, :][np.newaxis, ...] <= data
        subset_left = compared[:row, :]
        subset_right = compared[row + 1 :, :]
        result[row, :] = result[row, :] & np.any(subset_left, axis=0) & np.any(subset_right, axis=0)

    for col in range(data.shape[1]):
        compared = data[:, col][..., np.newaxis] <= data
        subset_left = compared[:, :col]
        subset_right = compared[:, col + 1 :]
        result[:, col] = result[:, col] & np.any(subset_left, axis=1) & np.any(subset_right, axis=1)

    total_visible = int(np.sum(~result))

    logger.info(f"{total_visible=}")

    return total_visible
