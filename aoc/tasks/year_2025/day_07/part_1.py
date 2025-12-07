from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


DOWN = complex(0, 1)
LEFT = complex(-1, 0)
RIGHT = complex(1, 0)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    splitters = set()
    seen_splitters = set()
    last_visited = set()

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "^":
                splitters.add(complex(x, y))
            if char == "S":
                last_visited.add(complex(x, y))

    for _ in range(len(lines)):
        new_positions = set()
        for pos in last_visited:
            if pos + DOWN in splitters:
                seen_splitters.add(pos)
                new_positions.add(pos + DOWN + LEFT)
                new_positions.add(pos + DOWN + RIGHT)
            else:
                new_positions.add(pos + DOWN)

        last_visited = new_positions

    return len(seen_splitters)
