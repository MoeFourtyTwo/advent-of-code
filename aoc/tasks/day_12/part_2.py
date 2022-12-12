from __future__ import annotations

import pathlib

import networkx as nx
from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def convert_height(height_char: str) -> int:
    if height_char == "S":
        height_char = "a"
    if height_char == "E":
        height_char = "z"

    return ord(height_char) - ord("a")


def within_range(height: int, other_height: int) -> bool:
    return abs(height - other_height) <= 1


def generate_graph(lines: list[str]) -> tuple[nx.DiGraph, tuple[int, int], tuple[int, int]]:
    graph = nx.DiGraph()
    start_node = (0, 0)
    end_node = (0, 0)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            height = convert_height(char)
            graph.add_node((x, y), height=height, char=char)

            if x > 0:
                if graph.nodes[(x - 1, y)]["height"] >= height - 1:
                    graph.add_edge((x - 1, y), (x, y), length=1)

                if height >= graph.nodes[(x - 1, y)]["height"] - 1:
                    graph.add_edge((x, y), (x - 1, y), length=1)

            if y > 0 and within_range(height, graph.nodes[(x, y - 1)]["height"]):
                if graph.nodes[(x, y - 1)]["height"] >= height - 1:
                    graph.add_edge((x, y - 1), (x, y), length=1)

                if height >= graph.nodes[(x, y - 1)]["height"] - 1:
                    graph.add_edge((x, y), (x, y - 1), length=1)

            if char == "S":
                start_node = (x, y)
            if char == "E":
                end_node = (x, y)
    return graph, start_node, end_node


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)
    graph, start_node, end_node = generate_graph(lines)

    paths = nx.shortest_path(graph, target=end_node, weight="length")

    lowest_nodes = [node for node, attrs in graph.nodes.data() if attrs["height"] == 0]
    shortest_valid_path = next(len(path) - 1 for path in paths.values() if path[0] in lowest_nodes)

    logger.info(f"{shortest_valid_path=}")

    return shortest_valid_path
