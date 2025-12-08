from __future__ import annotations

import functools
import operator
import pathlib

import networkx
import numpy as np

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH, k: int = 1000) -> int:
    lines = get_lines(path)

    points = np.array([list(map(int, row.split(","))) for row in lines], dtype=np.int64)
    n = points.shape[0]

    sq = np.sum(points * points, axis=1)
    dist_sq = sq[:, None] + sq[None, :] - 2 * (points @ points.T)

    triu_i, triu_j = np.triu_indices(n, k=1)
    flat = dist_sq[triu_i, triu_j]

    idx = np.argsort(flat)[:k]
    i_pairs = triu_i[idx]
    j_pairs = triu_j[idx]

    graph = networkx.Graph()
    for i in range(n):
        graph.add_node(i)

    for i, j in zip(i_pairs, j_pairs):
        graph.add_edge(i, j)

    return functools.reduce(
        operator.mul, list(sorted(map(len, networkx.connected_components(graph)), reverse=True))[:3]
    )
