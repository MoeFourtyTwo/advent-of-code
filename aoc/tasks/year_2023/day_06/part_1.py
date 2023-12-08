from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def calc_distance(hold_time: int, max_time: int) -> int:
    return (max_time - hold_time) * hold_time


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    max_times = map(int, lines[0].split(":")[1].strip().split())
    distances = map(int, lines[1].split(":")[1].strip().split())

    races = list(zip(max_times, distances))

    result = 1

    for max_time, distance in races:
        result *= sum(calc_distance(i, max_time) > distance for i in range(1, max_time - 1))

    return result
