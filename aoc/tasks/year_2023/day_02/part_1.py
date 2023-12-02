from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


MAX_CUBES = {"red": 12, "green": 13, "blue": 14}


def is_valid_game(game: list[dict]) -> bool:
    return all(all(sequence.get(key, 0) <= value for key, value in MAX_CUBES.items()) for sequence in game)


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

    return sum(game["id"] for game in games if is_valid_game(game["results"]))
