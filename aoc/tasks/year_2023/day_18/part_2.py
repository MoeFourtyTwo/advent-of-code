from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    points = [(0, 0)]

    circum = 0

    for line in lines:
        *_, code = line.split()

        distance = int(code[2:-2], 16)
        direction = code[-2]

        distance = int(distance)
        circum += distance
        match direction:
            case "0":  # R
                points.append((points[-1][0], points[-1][1] + distance))
            case "1":  # D
                points.append((points[-1][0] + distance, points[-1][1]))
            case "2":  # L
                points.append((points[-1][0], points[-1][1] - distance))
            case "3":  # U
                points.append((points[-1][0] - distance, points[-1][1]))

    points = points[:-1]

    n = len(points)
    area = 0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        area += x1 * y2 - x2 * y1

    area = abs(area) / 2 + circum / 2 + 1
    return int(area)
