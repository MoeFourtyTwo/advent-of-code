from __future__ import annotations

import itertools
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    points = [(int(x), int(y)) for x, y in [line.split(",") for line in lines]]

    max_area = 0

    for a, b in itertools.combinations(points, 2):
        max_area = max(max_area, (1 + abs(a[0] - b[0])) * (1 + abs(a[1] - b[1])))

    return max_area
