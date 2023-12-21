from __future__ import annotations

import functools
import pathlib

import networkx as nx
from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def parse_graph(lines: list[str]) -> None:

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

    for node_name, flow_rate in zip(node_name_list, flow_rate_list):
        GRAPH.add_node(node_name, flow_rate=int(flow_rate), is_open=False)

    for node_name, tunnels in zip(node_name_list, tunnels_list):
        for tunnel in tunnels.split(", "):
            GRAPH.add_edge(node_name, tunnel)


GRAPH = nx.Graph()


class Solver:
    def __init__(
        self, opened: set | None = None, starting_node: str = "AA", current_time: int = 0, total_time: int = 30
    ) -> None:
        self.current_minute = current_time
        self.max_minute = total_time

        self.current_node = starting_node
        self.opened = opened if opened is not None else set()

    def __hash__(self):
        return hash((self.current_minute, self.current_node, frozenset(self.opened)))

    @property
    def current_flow(self) -> int:
        return sum(node["flow_rate"] for node in GRAPH.nodes.values() if node in self.opened)

    def solve(self) -> int:
        return self.next_move()

    @functools.cache
    def next_move(self) -> int:
        candidates = self.find_closed_valves()
        paths = nx.shortest_path(GRAPH, source=self.current_node)
        relevant_paths = [
            path
            for target, path in paths.items()
            if target in candidates and len(path) <= self.max_minute - self.current_minute
        ]

        if len(relevant_paths) > 0:
            return max((self.compute_potential(path)) for path in relevant_paths)

        return 0

    def compute_potential(self, path: list[str]) -> int:
        flow_rate = GRAPH.nodes[path[-1]]["flow_rate"]
        open_time = self.max_minute - self.current_minute - len(path)
        return (
            open_time * flow_rate
            + Solver(
                self.opened | {path[-1]}, starting_node=path[-1], current_time=self.current_minute + len(path)
            ).next_move()
        )

    def find_closed_valves(self) -> set[str]:
        return {node for node, attr in GRAPH.nodes.items() if attr["flow_rate"] > 0} - self.opened


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    parse_graph(lines)

    solver = Solver()

    total_pressure_released = solver.solve()

    logger.info(f"{total_pressure_released=}")

    return total_pressure_released
