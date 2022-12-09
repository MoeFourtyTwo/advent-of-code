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

    def update_position_from_line(self, line: str) -> None:
        match line.split():
            case ["L", steps]:
                self.position -= Position(x=int(steps), y=0)
            case ["R", steps]:
                self.position += Position(x=int(steps), y=0)
            case ["D", steps]:
                self.position -= Position(x=0, y=int(steps))
            case ["U", steps]:
                self.position += Position(x=0, y=int(steps))


class Tail:
    def __init__(self, head: Head):
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
        while self.wants_to_follow:
            self.step()


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    head = Head()
    tail = Tail(head)

    for line in lines:
        head.update_position_from_line(line)
        tail.follow()

    visited_position_count = len(tail.trail)

    logger.info(f"{visited_position_count=}")

    return visited_position_count
