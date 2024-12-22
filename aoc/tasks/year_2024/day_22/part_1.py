from __future__ import annotations

import pathlib

from rich.progress import track

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    seeds = list(map(int, lines))

    result = 0
    print()
    for seed in track(seeds):
        value = seed

        for _ in range(2000):
            value = ((value * 64) ^ value) % 16777216
            value = ((value // 32) ^ value) % 16777216
            value = ((value * 2048) ^ value) % 16777216

        result += value
    return result
