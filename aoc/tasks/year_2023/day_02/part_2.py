from __future__ import annotations

import functools
import operator
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


COLORS = ["red", "green", "blue"]


def calculate_power(game: list[dict]) -> int:
    return int(functools.reduce(operator.mul, [max(result.get(color, 0) for result in game) for color in COLORS]))


def parse_line(line: str) -> dict:
    left, right = line.split(":")
    game_id = int(left.removeprefix("Game "))
    subsets = right.split(";")

    results = []
    for subset in subsets:
        result = {}
        for cube in subset.split(","):
            count, value = cube.strip().split()
            result[value] = int(count)
        results.append(result)

    return {"id": game_id, "results": results}


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    games = [parse_line(line) for line in lines]

    return sum(calculate_power(game["results"]) for game in games)
