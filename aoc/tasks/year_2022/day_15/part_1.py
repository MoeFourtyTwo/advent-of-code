from __future__ import annotations

import dataclasses
import functools
import pathlib

from loguru import logger
from tqdm import tqdm, trange

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def distance(self, other: Point) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    @classmethod
    def parse(cls, line: str) -> Point:
        x, y = map(int, line.replace("x=", "").replace("y=", "").split(", "))
        return Point(x=x, y=y)


@dataclasses.dataclass
class Sensor:
    center: Point
    beacon: Point

    @functools.cached_property
    def radius(self) -> int:
        return self.center.distance(self.beacon)

    def __contains__(self, item: Point) -> bool:
        return self.center.distance(item) <= self.radius

    @classmethod
    def parse(cls, line: str) -> Sensor:
        sensor_line, beacon_line = line.replace("Sensor at ", "").replace(" closest beacon is at ", "").split(":")
        return Sensor(center=Point.parse(sensor_line), beacon=Point.parse(beacon_line))


@timeit
def go(path: pathlib.Path = DATA_PATH, y: int = 2000000):
    lines = get_lines(path)

    sensors = [Sensor.parse(line) for line in tqdm(lines)]

    min_x = min(sensor.center.x - sensor.radius for sensor in tqdm(sensors))
    max_x = max(sensor.center.x + sensor.radius for sensor in tqdm(sensors))

    total_unavailable = sum(any(Point(x, y) in sensor for sensor in sensors) for x in trange(min_x, max_x + 1))
    offset = len(set(sensor.beacon for sensor in tqdm(sensors) if sensor.beacon.y == y))

    total_unavailable -= offset

    logger.info(f"{total_unavailable=}")
    return total_unavailable
