from __future__ import annotations

import pathlib

import networkx

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH, size: int = 70, steps: int = 1024) -> int:
    lines = get_lines(path)

    start = 0, 0
    goal = size, size

    # noinspection PyTypeChecker
    obstacles: list[tuple[int, int]] = [tuple(map(int, line.split(","))) for line in lines[:steps]]

    graph = networkx.DiGraph()

    for x in range(size + 1):
        for y in range(size + 1):
            if (x, y) in obstacles:
                continue

            graph.add_node((x, y))

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                if (
                    (x + dx, y + dy) not in obstacles
                    and x + dx >= 0
                    and y + dy >= 0
                    and x + dx <= size
                    and y + dy <= size
                ):
                    graph.add_edge((x, y), (x + dx, y + dy))

    shortest_path = networkx.shortest_path(graph, start, goal)

    return len(shortest_path) - 1
