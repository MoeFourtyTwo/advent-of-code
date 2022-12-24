from __future__ import annotations

import enum
import itertools
import pathlib
import typing

from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)

BLIZZARD: typing.TypeAlias = tuple[complex, complex]


class Direction(complex, enum.Enum):
    right = 1 + 0j
    down = 1j
    left = -1 + 0j
    up = -1j

    @classmethod
    def from_char(cls, char: str) -> Direction:
        match char:
            case ">":
                return Direction.right
            case "v":
                return Direction.down
            case "<":
                return Direction.left
            case "^":
                return Direction.up


class Field:
    def __init__(self, clock: int, width: int, height: int, start: complex, target: complex, blizzards: list[BLIZZARD]):
        self.clock = clock
        self.width = width
        self.height = height
        self.start = start
        self.target = target
        self.blizzards = blizzards
        self.elves = [self.start]

    @classmethod
    def parse_input(cls, lines: list[str]) -> Field:
        height = len(lines)
        width = len(lines[0])

        return Field(
            clock=0,
            width=width,
            height=height,
            start=1 + 0j,
            target=complex(width - 2, height - 1),
            blizzards=[
                (complex(x, y), Direction.from_char(char))
                for y, line in enumerate(lines)
                for x, char in enumerate(line)
                if char in ">v<^"
            ],
        )

    def solve(self) -> int:
        while self.target not in self.elves:
            self.next_field()
            self.iterate()
            self.clock += 1
        return self.clock

    def iterate(self) -> None:
        next_elves = set(itertools.chain.from_iterable(self.generate_options(elf) for elf in self.elves))
        self.elves = set(next_elves) - set(blizzard[0] for blizzard in self.blizzards)

    def next_field(self) -> None:
        self.blizzards = [self.update_blizzard(blizzard) for blizzard in self.blizzards]

    def update_blizzard(self, blizzard: BLIZZARD) -> BLIZZARD:
        position, direction = blizzard
        new_position = position + direction

        match direction:
            case Direction.right:
                if new_position.real >= self.width - 1:
                    return new_position - (self.width - 2), direction
                return new_position, direction
            case Direction.left:
                if new_position.real < 1:
                    return new_position + self.width - 2, direction
                return new_position, direction
            case Direction.down:
                if new_position.imag >= self.height - 1:
                    return new_position - complex(0, self.height - 2), direction
                return new_position, direction
            case Direction.up:
                if new_position.imag < 1:
                    return new_position + complex(0, self.height - 2), direction
                return new_position, direction

    def in_bounds(self, position: complex) -> bool:
        if position == self.start or position == self.target:
            return True

        return 0 < int(position.real) < self.width - 1 and 0 < int(position.imag) < self.height - 1

    def generate_options(self, position: complex) -> list[complex]:
        options = [position]

        for direction in Direction:
            if self.in_bounds(new_position := position + direction):
                options.append(new_position)

        return options


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    field = Field.parse_input(lines)

    min_time = field.solve()

    logger.info(f"{min_time=}")

    return min_time
