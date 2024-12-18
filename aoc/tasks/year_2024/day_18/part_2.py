from __future__ import annotations

import pathlib

import networkx

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH, size: int = 70) -> str:
    lines = get_lines(path)

    start = 0, 0
    goal = size, size

    # noinspection PyTypeChecker
    obstacles: list[tuple[int, int]] = [tuple(map(int, line.split(","))) for line in lines]

    graph = networkx.grid_graph((size + 1, size + 1))
    shortest_path = networkx.shortest_path(graph, start, goal)

    for step, obstacle in enumerate(obstacles):
        graph.remove_node(obstacle)

        if obstacle not in shortest_path:
            continue

        try:
            shortest_path = networkx.shortest_path(graph, start, goal)
        except networkx.NetworkXNoPath:
            return lines[step]

    raise ValueError("Something went wrong")
