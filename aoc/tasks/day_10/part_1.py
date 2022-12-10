from __future__ import annotations

import pathlib

from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    next_x = 1
    register_values = []

    for line in lines:
        match line.split():
            case ["noop"]:
                register_values += [next_x]
            case ["addx", value]:
                register_values += [next_x, next_x]
                next_x += int(value)

    probes = [20, 60, 100, 140, 180, 220]

    signal_strength_sum = sum(register_values[probe - 1] * probe for probe in probes)

    logger.info(f"{signal_strength_sum=}")

    return signal_strength_sum
