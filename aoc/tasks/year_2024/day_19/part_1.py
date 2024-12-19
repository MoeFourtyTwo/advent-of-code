from __future__ import annotations

import functools
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    available_patterns = frozenset(lines[0].split(", "))
    min_pattern_len = min(map(len, available_patterns))
    max_pattern_len = max(map(len, available_patterns))

    return sum(solve(line, available_patterns, min_pattern_len, max_pattern_len) for line in lines[2:])


@functools.cache
def solve(search_string: str, available_patterns: frozenset[str], min_pattern_len: int, max_pattern_len: int) -> bool:
    if not search_string:
        return True

    for split_len in range(min_pattern_len, min(len(search_string), max_pattern_len) + 1):
        left, right = search_string[:split_len], search_string[split_len:]

        if left in available_patterns and solve(right, available_patterns, min_pattern_len, max_pattern_len):
            return True

    return False
