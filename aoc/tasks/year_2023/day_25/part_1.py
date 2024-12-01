from __future__ import annotations

import itertools
import math
import pathlib

import networkx as nx

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)
    g = nx.Graph()
    for line in lines:
        node, other_nodes = line.split(": ")
        for other_node in other_nodes.split():
            g.add_edge(node, other_node)

    h = nx.algorithms.connectivity.build_auxiliary_edge_connectivity(g)
    r = nx.algorithms.flow.build_residual_network(h, "capacity")

    for u, v in itertools.combinations(g, 2):
        cut = nx.algorithms.connectivity.minimum_st_edge_cut(g, u, v, auxiliary=h, residual=r)
        if len(cut) != 3:
            continue

        g.remove_edges_from(cut)
        return math.prod(map(len, nx.connected_components(g)))

    raise ValueError("No solution found")
