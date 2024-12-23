from __future__ import annotations

import pathlib

import networkx

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> str:
    lines = get_lines(path)

    graph = networkx.Graph()

    for line in lines:
        graph.add_edge(*line.split("-"))

    max_clique = 0
    max_clique_nodes = []

    for clique in networkx.find_cliques(graph):
        if len(clique) > max_clique:
            max_clique = len(clique)
            max_clique_nodes = clique

    return ",".join(sorted(max_clique_nodes))
