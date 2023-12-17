from __future__ import annotations

import pathlib

import networkx as nx

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def build_graph(lines: list[str]) -> nx.DiGraph:
    graph = nx.DiGraph()

    combinations = {
        "up": ["left", "right"],
        "right": ["up", "down"],
        "down": ["left", "right"],
        "left": ["up", "down"],
    }
    offsets = {
        "up": (list(range(-1, -4, -1)), [0] * 3),
        "right": ([0] * 3, list(range(1, 4))),
        "down": (list(range(1, 4)), [0] * 3),
        "left": ([0] * 3, list(range(-1, -4, -1))),
    }

    min_offset = 4
    for row_index, row in enumerate(lines):
        for col_index, c in enumerate(row):
            for source, targets in combinations.items():
                for target in targets:
                    cost = 0
                    for row_offset, col_offset in zip(*offsets[target]):
                        target_row_index = row_index + row_offset
                        target_col_index = col_index + col_offset
                        if target_row_index not in range(len(lines)) or target_col_index not in range(
                            len(lines[target_row_index])
                        ):
                            continue

                        cost += int(lines[target_row_index][target_col_index])

                        graph.add_edge(
                            f"{row_index},{col_index},{source}",
                            f"{target_row_index},{target_col_index},{target}",
                            cost=cost,
                        )
    for direction in combinations.keys():
        graph.add_edge("start", f"0,0,{direction}", cost=0)
        graph.add_edge(f"{len(lines) - 1},{len(lines[0]) - 1},{direction}", "target", cost=0)

    return graph


@timeit
def calc_min_heat_loss(graph: nx.DiGraph) -> int:
    shortest_path = nx.shortest_path(graph, "start", "target", weight="cost")
    cost = nx.path_weight(graph, shortest_path, weight="cost")
    return cost


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    graph = build_graph(lines)
    loss = calc_min_heat_loss(graph)

    return loss


if __name__ == "__main__":
    go()
