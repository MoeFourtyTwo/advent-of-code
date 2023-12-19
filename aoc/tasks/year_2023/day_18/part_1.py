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
        direction, distance, _ = line.split()
        distance = int(distance)
        circum += distance
        match direction:
            case "R":
                points.append((points[-1][0], points[-1][1] + distance))
            case "D":
                points.append((points[-1][0] + distance, points[-1][1]))
            case "L":
                points.append((points[-1][0], points[-1][1] - distance))
            case "U":
                points.append((points[-1][0] - distance, points[-1][1]))

    points = points[:-1]

    # Shoelace formula
    n = len(points)
    area = 0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        area += x1 * y2 - x2 * y1

    area = abs(area) / 2 + circum / 2 + 1
    return int(area)
