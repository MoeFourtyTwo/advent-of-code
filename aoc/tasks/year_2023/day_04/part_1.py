from __future__ import annotations

import math
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def parse_line(line: str) -> int:
    _, numbers = line.split(":")
    winning_numbers, drawn_numbers = numbers.strip().split("|")

    return int(math.pow(2, len(set(winning_numbers.split()).intersection(set(drawn_numbers.split()))) - 1))


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)
    return sum(parse_line(line) for line in lines)
