from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    return sum(map(lambda s: int(next(filter(str.isdigit, s)) + next(filter(str.isdigit, reversed(s)))), lines))
