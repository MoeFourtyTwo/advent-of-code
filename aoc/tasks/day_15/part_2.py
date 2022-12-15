from __future__ import annotations

import dataclasses
import functools
import pathlib
import typing

from loguru import logger
from tqdm import tqdm

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

    def iterate_over_edge(self) -> typing.Generator[Point, None, None]:
        for offset in range(self.radius + 2):
            yield Point(x=self.center.x - self.radius - 1 + offset, y=self.center.y - offset)
            yield Point(x=self.center.x - self.radius - 1 + offset, y=self.center.y + offset)
            yield Point(x=self.center.x + self.radius + 1 - offset, y=self.center.y + offset)
            yield Point(x=self.center.x + self.radius + 1 - offset, y=self.center.y - offset)

    @classmethod
    def parse(cls, line: str) -> Sensor:
        sensor_line, beacon_line = line.replace("Sensor at ", "").replace(" closest beacon is at ", "").split(":")
        return Sensor(center=Point.parse(sensor_line), beacon=Point.parse(beacon_line))


def find_beacon(sensors: list[Sensor], max_value: int) -> Point:
    for sensor in tqdm(sensors):
        for point in tqdm(sensor.iterate_over_edge(), leave=False, total=(sensor.radius + 1) * 4):
            if 0 <= point.x <= max_value and 0 <= point.y <= max_value:
                if all(point not in sensor for sensor in sensors):
                    return point


@timeit
def go(path: pathlib.Path = DATA_PATH, max_value: int = 4000000):
    lines = get_lines(path)

    sensors = [Sensor.parse(line) for line in tqdm(lines)]

    beacon_position = find_beacon(sensors, max_value + 1)

    frequency = beacon_position.x * 4000000 + beacon_position.y

    logger.info(f"{frequency=}")
    return frequency
