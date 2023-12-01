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


def move_cursor(
    grid: np.ndarray, current_position: POSITION, current_direction: Direction
) -> tuple[POSITION, Direction]:
    next_position = (current_position[0] + current_direction[0], current_position[1] + current_direction[1])

    if grid[next_position] != CellType.void:
        return next_position, current_direction

    match next_position:
        case 0, column if 50 < column <= 100:  # ------ A.1
            return (column + 100, 1), Direction.right
        case 0, column if 100 < column <= 150:  # ----- B.1
            return (200, column - 100), Direction.up
        case 51, column if 100 < column <= 150:  # ---- C.1
            return (column - 50, 100), Direction.left
        case 100, column if 0 < column <= 50:  # ------ D.1
            return (column + 50, 51), Direction.right
        case 151, column if 50 < column <= 100:  # ---- E.1
            return (column + 100, 50), Direction.left
        case 201, column if 0 < column <= 50:  # ------ B.2
            return (1, column + 100), Direction.down
        case row, 0 if 100 < row <= 150:  # ----------- F.1
            return (151 - row, 51), Direction.right
        case row, 0 if 150 < row <= 200:  # ----------- A.2
            return (1, row - 100), Direction.down
        case row, 50 if 0 < row <= 50:  # ------------- F.2
            return (151 - row, 1), Direction.right
        case row, 50 if 50 < row <= 100:  # ----------- D.2
            return (101, row - 50), Direction.down
        case row, 51 if 150 < row <= 200:  # ---------- E.2
            return (150, row - 100), Direction.up
        case row, 101 if 50 < row <= 100:  # ---------- C.2
            return (50, row + 50), Direction.up
        case row, 101 if 100 < row <= 150:  # --------- G.1
            return (151 - row, 150), Direction.left
        case row, 151 if 0 < row <= 50:  # ------------ G.2
            return (151 - row, 100), Direction.left
        case _:
            raise RuntimeError(f"Encountered invalid position: {next_position=}")


def walk(
    grid: np.ndarray, current_position: POSITION, current_direction: Direction, steps: int
) -> tuple[POSITION, Direction]:
    for _ in range(steps):
        new_position, new_direction = move_cursor(grid, current_position, current_direction)

        match grid[new_position]:
            case CellType.wall:
                return current_position, current_direction
            case CellType.walkable:
                current_position = new_position
                current_direction = new_direction
            case _:
                raise RuntimeError(f"Encountered invalid state {grid[new_position]=}")

    return current_position, current_direction


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
                position, direction = walk(grid, position, direction, steps)
            case str() as rotation_char:
                direction = direction.rotate(rotation_char)
            case _:
                raise RuntimeError(f"Invalid instruction {instruction}")

    password = 1000 * position[0] + 4 * position[1] + list(Direction).index(direction)

    logger.info(f"{password=}")

    return password
