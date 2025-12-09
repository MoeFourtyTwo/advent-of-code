from __future__ import annotations

import itertools
import pathlib

from shapely import Polygon
from shapely.geometry import box
from shapely.ops import unary_union

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)

POINT = tuple[int, int]


def cell_perimeter_to_polygon(cell_points: list[POINT]):
    boxes = []
    for a, b in zip(cell_points, cell_points[1:] + [cell_points[0]]):
        lower_x = min(a[0], b[0])
        upper_x = max(a[0], b[0])
        lower_y = min(a[1], b[1])
        upper_y = max(a[1], b[1])
        boxes.append(box(lower_x, lower_y, upper_x + 1, upper_y + 1))

    union = Polygon(unary_union(boxes).exterior).simplify(1e-8)
    return union


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    points = [(int(x), int(y)) for x, y in [line.split(",") for line in lines]]

    polygon = cell_perimeter_to_polygon(points)

    boxes = []
    for a, b in itertools.combinations(points, 2):
        lower_x = min(a[0], b[0])
        upper_x = max(a[0], b[0]) + 1
        lower_y = min(a[1], b[1])
        upper_y = max(a[1], b[1]) + 1
        area = (upper_x - lower_x) * (upper_y - lower_y)
        boxes.append((area, lower_x, lower_y, upper_x, upper_y))

    boxes = sorted(boxes, reverse=True)

    for area, lower_x, lower_y, upper_x, upper_y in boxes:
        if polygon.covers(box(lower_x, lower_y, upper_x, upper_y)):
            return area

    return 0
