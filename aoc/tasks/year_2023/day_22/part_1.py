from __future__ import annotations

import dataclasses
import operator
import pathlib

import numpy as np
import numpy.typing as npt

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@dataclasses.dataclass(frozen=True, eq=True)
class Brick:
    x_min: int
    y_min: int
    z_min: int
    x_max: int
    y_max: int
    z_max: int

    @classmethod
    def from_line(cls, line: str) -> Brick:
        lower, upper = line.split("~")
        x_min, y_min, z_min = map(int, lower.split(","))
        x_max, y_max, z_max = map(int, upper.split(","))
        return cls(x_min, y_min, z_min, x_max + 1, y_max + 1, z_max + 1)

    def __lt__(self, other: Brick) -> bool:
        return self.z_min < other.z_min

    def move(self, delta_x: int = 0, delta_y: int = 0, delta_z: int = 0) -> Brick:
        return Brick(
            x_min=self.x_min + delta_x,
            x_max=self.x_max + delta_x,
            y_min=self.y_min + delta_y,
            y_max=self.y_max + delta_y,
            z_min=self.z_min + delta_z,
            z_max=self.z_max + delta_z,
        )

    def intersect_x(self, other: Brick) -> bool:
        return self.x_max > other.x_min and self.x_min < other.x_max

    def intersect_y(self, other: Brick) -> bool:
        return self.y_max > other.y_min and self.y_min < other.y_max


def init_ground(bricks: list[Brick]) -> tuple[npt.NDArray[int, int], list[Brick]]:
    global_x_min = min(bricks, key=operator.attrgetter("x_min")).x_min
    global_y_min = min(bricks, key=operator.attrgetter("y_min")).y_min
    global_x_max = max(bricks, key=operator.attrgetter("x_max")).x_max
    global_y_max = max(bricks, key=operator.attrgetter("y_max")).y_max

    bricks = [brick.move(delta_x=-global_x_min, delta_y=-global_y_min) for brick in bricks]

    global_x_max -= global_x_min
    global_y_max -= global_y_min
    ground = np.zeros((global_x_max, global_y_max), dtype=int)
    return ground, bricks


def settle_bricks(bricks: list[Brick]) -> list[Brick]:
    ground, bricks = init_ground(bricks)
    settled_bricks = []

    for brick in bricks:
        ground_max_z = np.max(ground[brick.x_min : brick.x_max, brick.y_min : brick.y_max])
        settled_brick = brick.move(delta_z=-(brick.z_min - ground_max_z))
        ground[settled_brick.x_min : settled_brick.x_max, settled_brick.y_min : settled_brick.y_max] = (
            settled_brick.z_max
        )
        settled_bricks.append(settled_brick)

    return settled_bricks


def find_connections(bricks: list[Brick]) -> tuple[dict[Brick, list[Brick]], dict[Brick, list[Brick]]]:
    supported_by = {}
    supporting = {}

    for brick in bricks:
        supported_by[brick] = []
        supporting[brick] = []

        intersecting_bricks = [
            other_brick
            for other_brick in bricks
            if brick != other_brick and brick.intersect_x(other_brick) and brick.intersect_y(other_brick)
        ]

        for intersecting_brick in intersecting_bricks:
            if intersecting_brick.z_max == brick.z_min:
                supported_by[brick].append(intersecting_brick)
            if intersecting_brick.z_min == brick.z_max:
                supporting[brick].append(intersecting_brick)

    return supported_by, supporting


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)
    bricks = list(sorted(map(Brick.from_line, lines)))
    bricks = settle_bricks(bricks)
    supported_by_map, supporting_map = find_connections(bricks)

    safe_to_disintegrate_count = 0

    for brick in bricks:
        if all(len(supported_by_map[supporting_brick]) > 1 for supporting_brick in supporting_map[brick]):
            safe_to_disintegrate_count += 1

    return safe_to_disintegrate_count


if __name__ == "__main__":
    go()
