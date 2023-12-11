from __future__ import annotations

import itertools
import pathlib

import numpy as np
from tqdm import tqdm

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


MULT_FACTOR = 999_999


def calc_distance(source: tuple[int, int], target: tuple[int, int], empty_rows: set[int], empty_cols: set[int]) -> int:
    row_range = range(min(source[0], target[0]), max(source[0], target[0]))
    col_range = range(min(source[1], target[1]), max(source[1], target[1]))

    empty_row_count = sum(empty_row in row_range for empty_row in empty_rows)
    empty_col_count = sum(empty_col in col_range for empty_col in empty_cols)

    distance = (
        abs(source[1] - target[1])
        + abs(source[0] - target[0])
        + empty_col_count * MULT_FACTOR
        + empty_row_count * MULT_FACTOR
    )

    return distance


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    data = np.array([list(line) for line in lines])

    empty_rows = set(np.where(np.all(data == ".", axis=1))[0])
    empty_cols = set(np.where(np.all(data == ".", axis=0))[0])

    positions = map(tuple, zip(*np.where(data == "#")))

    all_pairs = list(itertools.combinations(positions, 2))

    distance = sum(calc_distance(source, target, empty_rows, empty_cols) for source, target in tqdm(all_pairs))

    return distance
