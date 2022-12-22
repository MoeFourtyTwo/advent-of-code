from __future__ import annotations

import enum
import pathlib
import typing

import numpy as np
from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)

POSITION: typing.TypeAlias = tuple[int, int]


class Direction(tuple, enum.Enum):
    right = (0, 1)
    down = (1, 0)
    left = (0, -1)
    up = (-1, 0)

    def rotate(self, char: str) -> Direction:
        current_index = list(Direction).index(self)
        desired_index = (current_index + (1 if char == "R" else -1)) % 4
        return list(Direction)[desired_index]


class CellType(int, enum.Enum):
    void = -1
    walkable = 0
    wall = 1

    @classmethod
    def from_char(cls, char: str) -> CellType:
        match char:
            case " ":
                return CellType.void
            case ".":
                return CellType.walkable
            case "#":
                return CellType.wall


def convert_to_numpy(grid: list[str]) -> np.ndarray:
    width = len(max(grid, key=len))
    grid = [[CellType.from_char(char) for char in row.ljust(width, " ")] for row in grid]

    return np.pad(np.array(grid), 1, constant_values=CellType.void)


def find_start_position(grid: np.ndarray) -> POSITION:
    position = np.argwhere(grid[1, :] == CellType.walkable)[0][0]
    return 1, position


def parse_instructions(instructions_string: str) -> list[str | int]:
    split = instructions_string.replace("R", ";R;").replace("L", ";L;").split(";")
    return [int(instruction) if i % 2 == 0 else instruction for i, instruction in enumerate(split)]


def move_cursor(grid: np.ndarray, current_position: POSITION, direction: Direction) -> POSITION:
    return tuple((current_position[axis] + direction[axis]) % grid.shape[axis] for axis in (0, 1))


def walk(grid: np.ndarray, current_position: POSITION, direction: Direction, steps: int) -> POSITION:
    for _ in range(steps):
        new_position = move_cursor(grid, current_position, direction)

        match grid[new_position]:
            case CellType.wall:
                return current_position
            case CellType.walkable:
                current_position = new_position
            case CellType.void:
                while grid[new_position] == CellType.void:
                    new_position = move_cursor(grid, new_position, direction)
                match grid[new_position]:
                    case CellType.wall:
                        return current_position
                    case CellType.walkable:
                        current_position = new_position

    return current_position


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    *grid_strings, _, instructions_string = get_lines(path, strip=False, rstrip=True)

    grid = convert_to_numpy(grid_strings)
    instructions = parse_instructions(instructions_string)

    position = find_start_position(grid)
    direction = Direction.right

    for instruction in instructions:
        match instruction:
            case int() as steps:
                position = walk(grid, position, direction, steps)
            case str() as rotation_char:
                direction = direction.rotate(rotation_char)

    password = 1000 * position[0] + 4 * position[1] + list(Direction).index(direction)

    logger.info(f"{password=}")

    return password
