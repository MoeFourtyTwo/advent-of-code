from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def convert(number: int, maps: tuple[tuple[int, int, int], ...]) -> int:
    for destination, source, range_length in maps:
        if number in range(source, source + range_length):
            return destination + number - source
    return number


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    seeds = list(map(int, lines.pop(0).split(":")[1].strip().split()))
    lines.pop(0)
    lines.append("")

    maps = []
    current_map = []

    for line in lines:
        if ":" in line:
            continue

        if not line:
            maps.append(tuple(current_map))
            current_map = []
        else:
            current_map.append(tuple(map(int, line.split())))

    out_seed = []

    for seed in seeds:
        for current_map in maps:
            seed = convert(seed, current_map)
        out_seed.append(seed)

    return min(out_seed)
