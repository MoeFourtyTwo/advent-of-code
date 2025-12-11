from __future__ import annotations

import pathlib
from collections import defaultdict

import networkx

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def count_paths_dag(graph, source, target):
    order = networkx.topological_sort(graph)
    dp = defaultdict(int)
    dp[source] = 1

    for u in order:
        for v in graph.successors(u):
            dp[v] += dp[u]
    return dp[target]


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    graph = networkx.DiGraph()

    for line in lines:
        from_node, to_nodes = line.split(": ")
        for to_node in to_nodes.split(" "):
            graph.add_edge(from_node, to_node)

    svr_to_fft = count_paths_dag(graph, "svr", "fft")
    fft_to_dac = count_paths_dag(graph, "fft", "dac")
    dac_to_out = count_paths_dag(graph, "dac", "out")
    svr_to_dac = count_paths_dag(graph, "svr", "dac")
    dac_to_fft = count_paths_dag(graph, "dac", "fft")
    fft_to_out = count_paths_dag(graph, "fft", "out")

    return svr_to_fft * fft_to_dac * dac_to_out + svr_to_dac * dac_to_fft * fft_to_out
