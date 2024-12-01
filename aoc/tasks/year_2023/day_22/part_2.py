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

    assert global_x_min == 0 and global_y_min == 0
    ground = np.zeros((global_x_max, global_y_max), dtype=int)
    return ground, bricks


def settle_bricks(bricks: list[Brick]) -> tuple[list[Brick], int]:
    ground, bricks = init_ground(bricks)
    settled_bricks = []

    moved = 0

    for brick in bricks:
        ground_max_z = np.max(ground[brick.x_min : brick.x_max, brick.y_min : brick.y_max])
        settled_brick = brick.move(delta_z=-(brick.z_min - ground_max_z))

        if (brick.z_min - ground_max_z) > 0:
            moved += 1

        ground[settled_brick.x_min : settled_brick.x_max, settled_brick.y_min : settled_brick.y_max] = (
            settled_brick.z_max
        )
        settled_bricks.append(settled_brick)

    return settled_bricks, moved


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)
    bricks = list(sorted(map(Brick.from_line, lines)))
    bricks, _ = settle_bricks(bricks)
    bricks = sorted(bricks)

    total_moved_count = 0

    for i, brick in enumerate(bricks):
        new_bricks = bricks.copy()
        new_bricks.pop(i)
        _, moved_count = settle_bricks(new_bricks)
        total_moved_count += moved_count

    return total_moved_count


if __name__ == "__main__":
    go()
