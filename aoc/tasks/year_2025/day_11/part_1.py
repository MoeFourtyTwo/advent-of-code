from __future__ import annotations

import pathlib

import networkx

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    graph = networkx.DiGraph()

    for line in lines:
        from_node, to_nodes = line.split(": ")
        for to_node in to_nodes.split(" "):
            graph.add_edge(from_node, to_node)

    return len(list(networkx.all_simple_paths(graph, "you", "out")))
