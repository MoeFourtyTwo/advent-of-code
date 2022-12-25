from __future__ import annotations

import enum
import functools
import itertools
import pathlib
import typing

import numpy as np
from loguru import logger
from scipy.ndimage import convolve

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)
BLIZZARDS: typing.TypeAlias = tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
ELF_KERNEL = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0],
]


class Direction(enum.Enum):
    right = enum.auto()
    down = enum.auto()
    left = enum.auto()
    up = enum.auto()

    def to_char(self) -> str:
        match self:
            case self.right:
                return ">"
            case self.down:
                return "v"
            case self.left:
                return "<"
            case self.up:
                return "^"


@timeit
def parse_input(path: pathlib.Path) -> tuple[BLIZZARDS, np.ndarray]:
    lines = get_lines(path)
    # noinspection PyTypeChecker
    blizzards: BLIZZARDS = tuple(parse_blizzard(lines, direction.to_char()) for direction in Direction)
    walkable = np.array([[char != "#" for char in line] for line in lines])
    return blizzards, walkable


def parse_blizzard(lines: list[str], search_char: str) -> np.ndarray:
    return np.array([[char != search_char for char in line[1:-1]] for line in lines[1:-1]])


def generate_rotation_func(arrays: BLIZZARDS):
    @functools.cache
    def right(index: int) -> np.ndarray:
        return np.roll(arrays[0], index, axis=1)

    @functools.cache
    def down(index: int) -> np.ndarray:
        return np.roll(arrays[1], index, axis=0)

    @functools.cache
    def left(index: int) -> np.ndarray:
        return np.roll(arrays[2], -index, axis=1)

    @functools.cache
    def up(index: int) -> np.ndarray:
        return np.roll(arrays[3], -index, axis=0)

    def rotate_wind(clock: int) -> BLIZZARDS:
        return (
            right(clock % arrays[0].shape[1]),
            down(clock % arrays[0].shape[0]),
            left(clock % arrays[0].shape[1]),
            up(clock % arrays[0].shape[0]),
        )

    return rotate_wind


@timeit
def solve(wind_func, blizzards: BLIZZARDS, walkable, start, target) -> tuple[BLIZZARDS, int]:
    elves = np.zeros_like(walkable, dtype=bool)
    elves[start] = True
    minute = 0

    while not elves[target]:
        minute += 1
        blizzards = wind_func(minute)
        convolve(elves, ELF_KERNEL, output=elves, mode="constant", cval=False)
        np.logical_and(elves, walkable, out=elves)
        for blizzard in blizzards:
            np.logical_and(elves[1:-1, 1:-1], blizzard, out=elves[1:-1, 1:-1])

    return blizzards, minute


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    blizzards, walkable = parse_input(path)

    wind_func = generate_rotation_func(blizzards)

    blizzards, time_first_trip = solve(
        wind_func, blizzards, walkable, (0, 1), (walkable.shape[0] - 1, walkable.shape[1] - 2)
    )
    blizzards, time_second_trip = solve(
        wind_func, blizzards, walkable, (walkable.shape[0] - 1, walkable.shape[1] - 2), (0, 1)
    )
    _, time_third_trip = solve(wind_func, blizzards, walkable, (0, 1), (walkable.shape[0] - 1, walkable.shape[1] - 2))

    total_time = time_first_trip + time_second_trip + time_third_trip

    logger.info(f"{total_time}")
    return total_time
