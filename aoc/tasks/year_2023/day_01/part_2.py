from __future__ import annotations

import pathlib
import stringprep

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    translation_table = [
        ("zero", "z0o"),
        ("one", "o1e"),
        ("two", "t2o"),
        ("three", "t3e"),
        ("four", "f4r"),
        ("five", "f5e"),
        ("six", "s6x"),
        ("seven", "s7n"),
        ("eight", "e8t"),
        ("nine", "n9e"),
    ]

    def translate(string: str) -> str:
        for a, b in translation_table:
            string = string.replace(a, b)
        return string

    return sum(
        map(
            lambda s: int(next(filter(str.isdigit, s)) + next(filter(str.isdigit, reversed(s)))),
            map(translate, lines),
        )
    )
