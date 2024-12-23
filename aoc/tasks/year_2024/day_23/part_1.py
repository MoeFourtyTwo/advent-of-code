from __future__ import annotations

import itertools
import pathlib

import networkx

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    graph = networkx.Graph()

    for line in lines:
        graph.add_edge(*line.split("-"))

    relevant_cliques = set()

    for clique in networkx.find_cliques(graph):
        if len(clique) < 3:
            continue

        for nodes in itertools.combinations(clique, 3):
            if not any(node.startswith("t") for node in nodes):
                continue

            if graph.subgraph(nodes).number_of_edges() != 3:
                continue

            relevant_cliques.add(frozenset(nodes))
    return len(relevant_cliques)
