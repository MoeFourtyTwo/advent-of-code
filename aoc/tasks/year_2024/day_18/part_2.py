from __future__ import annotations

import pathlib

import networkx
from rich.progress import track

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

    graph = networkx.DiGraph()

    for x in range(size + 1):
        for y in range(size + 1):
            graph.add_node((x, y))

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                if 0 <= x + dx <= size and 0 <= y + dy <= size:
                    graph.add_edge((x, y), (x + dx, y + dy))

    for step, obstacle in track(enumerate(obstacles)):
        graph.remove_node(obstacle)

        if not networkx.has_path(graph, start, goal):
            return lines[step]

    raise ValueError("Something went wrong")
