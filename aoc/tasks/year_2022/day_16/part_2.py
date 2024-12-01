from __future__ import annotations

import functools
import itertools
import math
import pathlib
import typing
from collections import defaultdict

from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def parse_graph(lines: list[str]) -> tuple[dict[str, int], dict[str, list[str]]]:
    node_name_list, flow_rate_list, tunnels_list = zip(
        *[
            line.removeprefix("Valve ")
            .replace(" has flow rate=", ";")
            .replace(" tunnels lead to valves ", "")
            .replace(" tunnel leads to valve ", "")
            .split(";")
            for line in lines
        ]
    )

    return (
        {node_name: int(flow_rate) for node_name, flow_rate in zip(node_name_list, flow_rate_list)},
        {node_name: tunnels.split(", ") for node_name, tunnels in zip(node_name_list, tunnels_list)},
    )


def compute_distances(nodes: typing.Iterable[str], edges: dict[str, list[str]]) -> dict[str, dict[str, int]]:
    adj_matrix = defaultdict(lambda: defaultdict(lambda: math.inf))

    for edge, tunnels in edges.items():
        adj_matrix[edge][edge] = 0
        for tunnel in tunnels:
            adj_matrix[edge][tunnel] = 1

    for k, i, j in itertools.product(nodes, nodes, nodes):
        adj_matrix[i][j] = min(adj_matrix[i][j], adj_matrix[i][k] + adj_matrix[k][j])

    return adj_matrix


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    nodes, edges = parse_graph(lines)

    adj_matrix = compute_distances(nodes, edges)

    candidates = frozenset({node for node, flow_rate in nodes.items() if flow_rate > 0})

    @functools.cache
    def find_flow_rate(
        current_node: str,
        remaining_time: int,
        remaining_candidates: frozenset,
        two_agents: bool,
    ) -> int:
        return max(
            [
                nodes[next_node] * (remaining_time - distance)
                + find_flow_rate(
                    current_node=next_node,
                    remaining_time=remaining_time - distance,
                    remaining_candidates=remaining_candidates - {next_node},
                    two_agents=two_agents,
                )
                for next_node in remaining_candidates
                if (distance := adj_matrix[current_node][next_node] + 1) <= remaining_time
            ]
            + [
                find_flow_rate(
                    current_node="AA",
                    remaining_time=26,
                    remaining_candidates=remaining_candidates,
                    two_agents=False,
                )
                if two_agents
                else 0
            ]
        )

    total_pressure_released = find_flow_rate(
        current_node="AA",
        remaining_time=26,
        remaining_candidates=candidates,
        two_agents=True,
    )

    logger.info(f"{total_pressure_released=}")

    return total_pressure_released
