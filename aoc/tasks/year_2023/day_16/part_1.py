from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


class Solver:
    def __init__(self, board: list[str]):
        self.visited = set()
        self.board = board

        self.valid_row_range = range(0, len(board))
        self.valid_col_range = range(0, len(board[0]))

    def step(self, movement: tuple[int, int, int, int]) -> set[tuple[int, int, int, int]]:
        if movement in self.visited:
            return set()
        row, col, direction_row, direction_col = movement
        if row not in self.valid_row_range or col not in self.valid_col_range:
            return set()

        self.visited.add(movement)

        match self.board[row][col], direction_row, direction_col:
            case ".", _, _:
                return {(row + direction_row, col + direction_col, direction_row, direction_col)}
            case "/", 1, _:
                return {(row, col - 1, 0, -1)}
            case "/", -1, _:
                return {(row, col + 1, 0, 1)}
            case "/", _, 1:
                return {(row - 1, col, -1, 0)}
            case "/", _, -1:
                return {(row + 1, col, 1, 0)}
            case "\\", 1, _:
                return {(row, col + 1, 0, 1)}
            case "\\", -1, _:
                return {(row, col - 1, 0, -1)}
            case "\\", _, 1:
                return {(row + 1, col, 1, 0)}
            case "\\", _, -1:
                return {(row - 1, col, -1, 0)}
            case "-", 0, _:
                return {(row + direction_row, col + direction_col, direction_row, direction_col)}
            case "-", _, _:
                return {(row, col + 1, 0, 1), (row, col - 1, 0, -1)}
            case "|", _, 0:
                return {(row + direction_row, col + direction_col, direction_row, direction_col)}
            case "|", _, _:
                return {(row + 1, col, 1, 0), (row - 1, col, -1, 0)}

    def count_energized_tiles(self) -> int:
        return len({(x, y) for x, y, _, _ in self.visited})

    @classmethod
    def solve(cls, data: list[str], init_position: tuple[int, int, int, int]) -> int:
        solver = cls(data)
        open_positions = {init_position}

        while open_positions:
            open_positions |= solver.step(open_positions.pop())

        return solver.count_energized_tiles()


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    data = get_lines(path)

    return Solver.solve(data, (0, 0, 0, 1))
