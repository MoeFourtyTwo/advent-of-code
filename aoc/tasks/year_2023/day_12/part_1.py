from __future__ import annotations

import functools
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@functools.cache
def count(line: str, groups: tuple[int, ...]) -> int:
    if len(line) == 0:
        return int(len(groups) == 0)

    match line[0]:
        case ".":
            return count(line[1:], groups)
        case "?":
            return count(line[1:], groups) + count("#" + line[1:], groups)
        case "#":
            if len(groups) == 0:
                return 0

            if len(line) < groups[0]:
                return 0

            if "." in line[: groups[0]]:
                return 0

            if len(groups) > 1:
                if len(line) < groups[0] + 1 or line[groups[0]] == "#":
                    return 0
                return count(line[groups[0] + 1 :], groups[1:])
            else:
                return count(line[groups[0] :], groups[1:])


def parse_line(line: str) -> tuple[str, tuple[int, ...]]:
    line, damage_groups = line.split()
    return line + ".", tuple(map(int, damage_groups.split(",")))


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    return sum(count(*parse_line(line)) for line in lines)
