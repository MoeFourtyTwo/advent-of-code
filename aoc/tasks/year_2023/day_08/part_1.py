from __future__ import annotations

import pathlib
import typing

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)

INDEX_MAP = {"L": 0, "R": 1}


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    instructions = lines.pop(0)
    lines.pop(0)
    graph = {}

    for line in lines:
        node, neighbors = line.split(" = ")
        graph[node] = neighbors[1:-1].split(", ")

    def instruction_generator() -> typing.Iterator[str]:
        while True:
            for instruction in instructions:
                yield instruction

    current_node = "AAA"
    steps = 0

    generator = instruction_generator()
    while current_node != "ZZZ":
        steps += 1
        instruction = next(generator)

        current_node = graph[current_node][INDEX_MAP[instruction]]

    return steps
