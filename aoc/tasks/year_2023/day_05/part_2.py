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


def step(ranges: set[tuple[int, int]], maps: list[tuple[int, int, int], ...]) -> set[tuple[int, int]]:
    out_ranges = set()

    for destination, source_lower, source_upper in maps:
        new_ranges = set()
        while ranges:
            lower, upper = ranges.pop()
            left_chunk_lower = lower
            left_chunk_upper = min(source_lower, upper)
            middle_chunk_lower = max(lower, source_lower)
            middle_chunk_upper = min(upper, source_upper)
            right_chunk_lower = max(lower, source_upper)
            right_chunk_upper = upper

            if left_chunk_lower < left_chunk_upper:
                new_ranges.add((left_chunk_lower, left_chunk_upper))
            if right_chunk_lower < right_chunk_upper:
                new_ranges.add((right_chunk_lower, right_chunk_upper))
            if middle_chunk_lower < middle_chunk_upper:
                out_ranges.add(
                    (destination + middle_chunk_lower - source_lower, destination + middle_chunk_upper - source_lower)
                )

        ranges = new_ranges

    return out_ranges | ranges


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)
    lines.append("")

    seeds = map(int, lines.pop(0).split(":")[1].strip().split())
    seed_ranges = set(map(lambda x: (x[0], x[0] + x[1]), zip(seeds, seeds)))

    lines.pop(0)

    maps = []
    current_map = []

    for line in lines:
        if ":" in line:
            continue

        if not line:
            maps.append(current_map)
            current_map = []
        else:
            destination, source, range_length = line.split()
            current_map.append((int(destination), int(source), int(source) + int(range_length)))

    for current_map in maps:
        seed_ranges = step(seed_ranges, current_map)
    return min(seed_ranges)[0]


if __name__ == "__main__":
    go()
