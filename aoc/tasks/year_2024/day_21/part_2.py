from __future__ import annotations

import functools
import itertools
import pathlib
from collections import defaultdict
from enum import StrEnum

import networkx

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


class Direction(StrEnum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


def prune_path(path: list[str]) -> bool:
    return not (path == sorted(path) or path == list(sorted(path, reverse=True)))


def precompute_paths(data: list[list[str]]) -> dict[str, dict[str, list[Direction]]]:
    graph = networkx.DiGraph()
    directions = {(-1, 0): Direction.UP, (1, 0): Direction.DOWN, (0, -1): Direction.LEFT, (0, 1): Direction.RIGHT}

    for i, row in enumerate(data):
        for j, key in enumerate(row):
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < len(data) and 0 <= nj < len(data[ni]):
                    neighbor = data[ni][nj]
                    graph.add_edge(key, neighbor, direction=directions[(di, dj)])
    graph.remove_node("_")

    precomputed_paths = defaultdict(lambda: defaultdict(list))

    for node in graph.nodes:
        for other_node in graph.nodes:
            if node != other_node:
                paths = networkx.all_shortest_paths(graph, node, other_node)
                direction_paths = []

                for path in paths:
                    direction_path = []
                    for d_node, d_other_node in zip(path, path[1:]):
                        direction_path.append(graph.get_edge_data(d_node, d_other_node)["direction"])

                    if prune_path(direction_path):
                        continue

                    direction_paths.append(direction_path)

                for path in direction_paths:
                    precomputed_paths[node][other_node].append(path + ["A"])
                precomputed_paths[node][other_node] = sorted(precomputed_paths[node][other_node], key=lambda x: len(x))
            else:
                precomputed_paths[node][other_node] = [["A"]]

    return precomputed_paths


NUMPAD_PATHS = precompute_paths([["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["_", "0", "A"]])
KEYPAD_PATHS = precompute_paths([["_", Direction.UP, "A"], [Direction.LEFT, Direction.DOWN, Direction.RIGHT]])


def generate_possible_paths(
    precomputed_paths: dict[str, dict[str, list[Direction]]], target: str | list[str]
) -> list[list[Direction]]:
    state = "A"
    possible_paths = []

    for char in target:
        paths = precomputed_paths[state][char]

        possible_paths.append(paths)
        state = char

    all_possible_paths = []
    for elements in itertools.product(*possible_paths):
        all_possible_paths.append(list(itertools.chain(*elements)))

    return sorted(all_possible_paths, key=lambda x: len(x))


def solve_numpad(target: str) -> int:
    possible_paths = generate_possible_paths(NUMPAD_PATHS, target)

    cost = min(sum(min_cost(left, right, 25) for left, right in zip(["A"] + path, path)) for path in possible_paths)

    return cost


@functools.cache
def min_cost(source: str, target: str, depth: int) -> int:
    if depth == 0:
        return 1

    paths = KEYPAD_PATHS[source][target]

    cost = min(sum(min_cost(left, right, depth - 1) for left, right in zip(["A"] + path, path)) for path in paths)
    return cost


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    return sum(solve_numpad(line) * int(line[:-1]) for line in lines)
