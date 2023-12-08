from __future__ import annotations

import pathlib
import typing

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)

INDEX_MAP = {"L": 0, "R": 1}


def instruction_generator(instructions: str) -> typing.Iterator[tuple[int, str]]:
    while True:
        for index, instruction in enumerate(instructions):
            yield index, instruction


def step_to_goal(current_node: str, graph: dict[str, list[str]], generator: typing.Iterator[tuple[int, str]]) -> int:
    steps = 0
    while current_node != "ZZZ":
        steps += 1
        index, instruction = next(generator)
        current_node = graph[current_node][INDEX_MAP[instruction]]

    return steps


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    instructions = lines.pop(0)
    lines.pop(0)
    graph = {}

    for line in lines:
        node, neighbors = line.split(" = ")
        graph[node] = neighbors[1:-1].split(", ")

    return step_to_goal("AAA", graph, instruction_generator(instructions))
