import pathlib

import numpy as np
from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_as_array, get_data_path

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    data = get_as_array(path)
    result = np.pad(
        np.ones((data.shape[0] - 2, data.shape[1] - 2), dtype=int), 1, mode="constant", constant_values=False
    )

    for row in range(1, data.shape[0] - 1):
        compared = data[row, :][np.newaxis, ...] > data
        subset_left = np.pad(compared[:row, :], ((1, 0), (0, 0)), mode="constant", constant_values=False)
        subset_right = np.pad(compared[row + 1 :, :], ((0, 1), (0, 0)), mode="constant", constant_values=False)
        result[row, :] = (
            result[row, :]
            * np.clip(np.argmin(np.flip(subset_left, axis=0), axis=0) + 1, 0, subset_left.shape[0] - 1)
            * np.clip(np.argmin(subset_right, axis=0) + 1, 0, subset_right.shape[0] - 1)
        )

    for col in range(1, data.shape[1] - 1):
        compared = data[:, col][..., np.newaxis] > data
        subset_left = np.pad(compared[:, :col], ((0, 0), (1, 0)), mode="constant", constant_values=False)
        subset_right = np.pad(compared[:, col + 1 :], ((0, 0), (0, 1)), mode="constant", constant_values=False)
        result[:, col] = (
            result[:, col]
            * np.clip(np.argmin(np.flip(subset_left, axis=1), axis=1) + 1, 0, subset_left.shape[1] - 1)
            * np.clip(np.argmin(subset_right, axis=1) + 1, 0, subset_right.shape[1] - 1)
        )

    max_score = np.max(result)

    logger.info(f"{max_score=}")

    return max_score
