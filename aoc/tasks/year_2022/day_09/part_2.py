from __future__ import annotations

import dataclasses
import pathlib

from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@dataclasses.dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: Position) -> Position:
        return Position(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Position) -> Position:
        return Position(x=self.x - other.x, y=self.y - other.y)

    def is_touching(self, other: Position) -> bool:
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1

    def clip(self, min_value: int, max_value: int) -> Position:
        return Position(x=min(max(self.x, min_value), max_value), y=min(max(self.y, min_value), max_value))


class Head:
    def __init__(self):
        self.position = Position(x=0, y=0)

    def update_position_from_direction(self, direction: str) -> None:
        match direction:
            case "L":
                self.position -= Position(x=1, y=0)
            case "R":
                self.position += Position(x=1, y=0)
            case "D":
                self.position -= Position(x=0, y=1)
            case "U":
                self.position += Position(x=0, y=1)


class Tail:
    def __init__(self, head: Head | Tail):
        self.position = head.position
        self.head = head
        self.trail = {self.position}

    @property
    def wants_to_follow(self) -> bool:
        return not self.position.is_touching(self.head.position)

    def step(self) -> None:
        diff = (self.head.position - self.position).clip(-1, 1)
        self.position += diff
        self.trail.add(self.position)

    def follow(self) -> None:
        if self.wants_to_follow:
            self.step()


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    head = Head()

    last_tail = head
    tails = []
    for _ in range(9):
        tail = Tail(last_tail)
        last_tail = tail
        tails.append(tail)

    for line in lines:
        direction, count = line.split()

        for _ in range(int(count)):
            head.update_position_from_direction(direction)
            for tail in tails:
                tail.follow()

    visited_position_count = len(last_tail.trail)

    logger.info(f"{visited_position_count=}")

    return visited_position_count
