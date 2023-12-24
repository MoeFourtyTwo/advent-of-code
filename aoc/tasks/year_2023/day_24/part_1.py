from __future__ import annotations

import dataclasses
import itertools
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@dataclasses.dataclass
class HailstonePath:
    p_x: float
    p_y: float
    p_z: float
    v_x: float
    v_y: float
    v_z: float

    @classmethod
    def from_str(cls, line: str) -> HailstonePath:
        p, v = line.split(" @ ")
        p_x, p_y, p_z = map(float, p.split(", "))
        v_x, v_y, v_z = map(float, v.split(", "))
        return cls(p_x, p_y, p_z, v_x, v_y, v_z)


def calc_intersection_time(a: HailstonePath, b: HailstonePath):
    return ((a.p_y - b.p_y) * a.v_x - (a.p_x - b.p_x) * a.v_y) / (a.v_x * b.v_y - b.v_x * a.v_y)


def is_valid(a: HailstonePath, b: HailstonePath, area_range: tuple[float, float]) -> bool:
    try:
        t_1 = calc_intersection_time(b, a)
        t_2 = calc_intersection_time(a, b)
    except ZeroDivisionError:
        return False

    x = b.p_x + t_2 * b.v_x
    y = b.p_y + t_2 * b.v_y
    return t_1 >= 0.0 and t_2 >= 0 and area_range[0] <= x <= area_range[1] and area_range[0] <= y <= area_range[1]


@timeit
def go(path: pathlib.Path = DATA_PATH, area_range: tuple[float, float] = (200000000000000.0, 400000000000000.0)) -> int:
    lines = get_lines(path)
    paths = list(map(HailstonePath.from_str, lines))

    return sum(is_valid(a, b, area_range) for a, b in itertools.combinations(paths, 2))
