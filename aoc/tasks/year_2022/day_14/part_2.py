from __future__ import annotations

import pathlib

import numpy as np
from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    segments = [[tuple(map(int, segment.split(","))) for segment in line.split(" -> ")] for line in lines]

    max_x = max(max(point[0] for point in segment) for segment in segments)
    max_y = max(max(point[1] for point in segment) for segment in segments)

    segments.append([(0, max_y + 2), (2 * max_x, max_y + 2)])

    chart = np.zeros(shape=(2 * max_x + 1, max_y + 3))

    for segment in segments:
        for from_point, to_point in zip(segment, segment[1:]):
            chart[
                min(from_point[0], to_point[0]) : max(from_point[0], to_point[0]) + 1,
                min(from_point[1], to_point[1]) : max(from_point[1], to_point[1]) + 1,
            ] = 1

    sand_counter = 0

    while True:
        try:
            x, y = 500, 0
            while True:
                if chart[x, y + 1] == 0:
                    y += 1
                    continue

                if chart[x - 1, y + 1] == 0:
                    x -= 1
                    y += 1
                    continue

                if chart[x + 1, y + 1] == 0:
                    x += 1
                    y += 1
                    continue

                if chart[x, y] == 1:
                    raise IndexError

                chart[x, y] = 1

                break

            sand_counter += 1
        except IndexError:
            break

    logger.info(f"{sand_counter=}")

    return sand_counter
