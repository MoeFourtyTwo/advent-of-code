from __future__ import annotations

import itertools
import pathlib
from collections import defaultdict

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    antenna_locations = defaultdict(list)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == ".":
                continue

            antenna_locations[char].append(complex(x, y))

    antinodes = set()

    max_x = len(lines[0])
    max_y = len(lines)

    for frequency, locations in antenna_locations.items():
        for antenna_a, antenna_b in itertools.combinations(locations, 2):
            for location in resonate(antenna_a, antenna_b):
                if 0 <= location.real < max_x and 0 <= location.imag < max_y:
                    antinodes.add(location)

    return len(antinodes)


def resonate(antenna_a: complex, antenna_b: complex) -> tuple[complex, complex]:
    diff = antenna_a - antenna_b

    return antenna_a + diff, antenna_a - 2 * diff
