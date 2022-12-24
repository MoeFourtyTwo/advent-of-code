from __future__ import annotations

import dataclasses
import enum
import functools
import heapq
import math
import pathlib
import typing

import tqdm
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

    def to_char(self) -> str:
        match self:
            case Direction.right:
                return ">"
            case Direction.down:
                return "v"
            case Direction.left:
                return "<"
            case Direction.up:
                return "^"


@dataclasses.dataclass(frozen=True)
class Field:
    clock: int
    width: int
    height: int
    start: complex
    target: complex

    blizzards: list[BLIZZARD]

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

    def next_field(self) -> Field:
        return dataclasses.replace(
            self, clock=self.clock + 1, blizzards=[self.update_blizzard(blizzard) for blizzard in self.blizzards]
        )

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

    @functools.cached_property
    def data(self) -> frozenset[complex]:
        return frozenset(blizzard[0] for blizzard in self.blizzards)

    def generate_options(self, option: Option) -> list[Option]:
        options = []

        if option.position not in self.data:
            options.append(option.stay())

        for direction in Direction:
            if (new_position := option + direction).in_bounds(self) and new_position.position not in self.data:
                options.append(new_position)

        for direction in [Direction.down, Direction.up]:
            if (new_position := option + direction).finished:
                options = [option for option in options if not option.finished]
                updated_option = new_position.flip()
                options.append(updated_option)

                if updated_option.fully_finished:
                    return [updated_option]

        return options


@dataclasses.dataclass(frozen=True, eq=True)
class Option:
    start: complex
    target: complex
    position: complex
    clock: int
    finish_counter: int = 0

    @property
    def priority(self) -> tuple[int, int, int]:
        return (
            -self.finish_counter,
            self.clock,
        )

    def __lt__(self, other: Option) -> bool:
        return self.priority < other.priority

    def __add__(self, other: Direction) -> Option:
        return dataclasses.replace(self, position=self.position + other, clock=self.clock + 1)

    def stay(self) -> Option:
        return dataclasses.replace(self, clock=self.clock + 1)

    def flip(self) -> Option:
        return dataclasses.replace(
            self,
            start=self.target,
            target=self.start,
            finish_counter=self.finish_counter + 1,
        )

    def in_bounds(self, field: Field) -> bool:
        if self.position == field.start or self.position == field.target:
            return True

        return 0 < int(self.position.real) < field.width - 1 and 0 < int(self.position.imag) < field.height - 1

    @property
    def finished(self) -> bool:
        return self.position == self.target

    @property
    def fully_finished(self) -> bool:
        return self.finish_counter == 3


def field_manager(initial_field: Field) -> typing.Callable[[int], Field]:
    fields = {0: initial_field}

    def inner(n: int) -> Field:
        if n in fields:
            return fields[n]

        for i in range(max(fields.keys()) + 1, n + 1):
            fields[i] = fields[i - 1].next_field()

        return fields[n]

    return inner


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    field_getter = field_manager(Field.parse_input(lines))

    heap = []
    start_option = Option(field_getter(0).start, field_getter(0).target, field_getter(0).start, 0)
    heapq.heappush(heap, start_option)
    known_states = {start_option}
    with tqdm.tqdm() as pbar:
        while heap:
            pbar.update()
            option: Option = heapq.heappop(heap)

            current_field = field_getter(option.clock + 1)
            next_options = current_field.generate_options(option)
            for next_option in next_options:
                if next_option not in known_states:
                    if next_option.finished:
                        known_states = {next_option}
                        heap = []
                        heapq.heappush(heap, next_option)
                        break
                    if next_option.fully_finished:
                        logger.info(f"{next_option.clock=}")
                        return next_option.clock
                    else:
                        known_states.add(next_option)
                        heapq.heappush(heap, next_option)