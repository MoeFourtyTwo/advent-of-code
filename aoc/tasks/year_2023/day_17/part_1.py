from __future__ import annotations

import pathlib

import networkx as nx

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    graph = nx.DiGraph()

    combinations = {
        "up": ["left", "right"],
        "right": ["up", "down"],
        "down": ["left", "right"],
        "left": ["up", "down"],
    }

    offsets = {
        "up": ([-1, -2, -3], [0, 0, 0]),
        "right": ([0, 0, 0], [1, 2, 3]),
        "down": ([1, 2, 3], [0, 0, 0]),
        "left": ([0, 0, 0], [-1, -2, -3]),
    }

    for row_index, row in enumerate(lines):
        for col_index, c in enumerate(row):
            for source, targets in combinations.items():
                for target in targets:
                    cost = 0
                    for row_offset, col_offset in zip(*offsets[target]):
                        try:
                            cost += int(lines[row_index + row_offset][col_index + col_offset])
                        except IndexError:
                            continue

                        graph.add_edge(
                            f"{row_index},{col_index},{source}",
                            f"{row_index+row_offset},{col_index+col_offset},{target}",
                            cost=cost,
                        )

    for direction in combinations.keys():
        graph.add_edge("start", f"0,0,{direction}", cost=0)
        graph.add_edge(f"{len(lines) - 1},{len(lines[0]) - 1},{direction}", "target", cost=0)

    shortest_path = nx.shortest_path(graph, "start", "target", weight="cost")
    cost = nx.path_weight(graph, shortest_path, weight="cost")

    return cost


if __name__ == "__main__":
    go()
