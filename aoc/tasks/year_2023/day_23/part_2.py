from __future__ import annotations

import pathlib

import networkx as nx
from tqdm import tqdm

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    g = nx.DiGraph()

    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                continue

            for row_offset, col_offset in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                try:
                    neighbor = lines[row + row_offset][col + col_offset]
                except IndexError:
                    continue

                if neighbor == "#":
                    continue
                g.add_edge((row, col), (row + row_offset, col + col_offset), weight=1)

    nodes_to_remove = []
    for node in g.nodes():
        predecessors = list(g.predecessors(node))
        successors = list(g.successors(node))

        if len(predecessors) == 2 and set(predecessors) == set(successors):
            node_a, node_b = predecessors
            new_weight = g.get_edge_data(node_a, node)["weight"] + g.get_edge_data(node, node_b)["weight"]
            g.remove_edge(node_a, node)
            g.remove_edge(node, node_b)
            g.remove_edge(node_b, node)
            g.remove_edge(node, node_a)
            nodes_to_remove.append(node)
            g.add_edge(node_a, node_b, weight=new_weight)
            g.add_edge(node_b, node_a, weight=new_weight)

    for node in nodes_to_remove:
        g.remove_node(node)

    longest_path = max(
        tqdm(nx.all_simple_paths(g, (0, 1), (len(lines) - 1, len(lines[-1]) - 2))),
        key=lambda x: nx.path_weight(g, x, weight="weight"),
    )
    return nx.path_weight(g, longest_path, weight="weight")


if __name__ == "__main__":
    go()
