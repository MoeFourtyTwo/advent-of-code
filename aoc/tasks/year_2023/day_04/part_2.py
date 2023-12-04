from __future__ import annotations

import pathlib
from collections import defaultdict

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def parse_line(line: str) -> int:
    _, numbers = line.split(":")
    winning_numbers, drawn_numbers = numbers.strip().split("|")

    return int(len(set(winning_numbers.split()).intersection(set(drawn_numbers.split()))))


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    counts = defaultdict(lambda: 0)
    for i in range(len(lines)):
        winner_count = parse_line(lines[i])
        counts[i] += 1
        for j in range(winner_count):
            counts[i + j + 1] += counts[i]

    return sum(counts.values())
