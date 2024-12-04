from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def count_patterns(grid: list[str], pattern: list[str]) -> int:
    grid_rows = len(grid)
    grid_cols = len(grid[0])

    pattern_rows = len(pattern)
    pattern_cols = len(pattern[0])

    count = 0
    for r in range(grid_rows - pattern_rows + 1):
        for c in range(grid_cols - pattern_cols + 1):
            if check_at_position(grid, (r, c), pattern):
                count += 1
    return count


def check_at_position(grid: list[str], position: tuple[int, int], pattern: list[str]) -> bool:
    for pr in range(len(pattern)):
        for pc in range(len(pattern[0])):
            if pattern[pr][pc] != "." and grid[position[0] + pr][position[1] + pc] != pattern[pr][pc]:
                return False
    return True


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    grid = get_lines(path)

    count = 0
    count += count_patterns(grid, ["M.S", ".A.", "M.S"])
    count += count_patterns(grid, ["M.M", ".A.", "S.S"])
    count += count_patterns(grid, ["S.M", ".A.", "S.M"])
    count += count_patterns(grid, ["S.S", ".A.", "M.M"])

    return count
