from __future__ import annotations

import dataclasses
import enum
import heapq
import itertools
import operator
import pathlib

import networkx as nx
import numpy as np
import numpy.typing as npt

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


class Directions(complex, enum.Enum):
    UP = complex(-1, 0)
    RIGHT = complex(0, 1)
    DOWN = complex(1, 0)
    LEFT = complex(0, -1)


def get_value(data: npt.NDArray[int, int], position: complex) -> int:
    return int(data[int(position.real), int(position.imag)])


def set_value(data: npt.NDArray[int, int], position: complex, value: int) -> None:
    data[int(position.real), int(position.imag)] = value


def count_consecutive(path: list[Directions]) -> int:
    if not path:
        return 0
    last = path[-1]
    for i, p in enumerate(reversed(path)):
        if last != p:
            return i
    return len(path)


@dataclasses.dataclass
class Step:
    cost: int
    position: complex
    path: list[Directions]
    target: complex

    @property
    def consecutive(self) -> int:
        return count_consecutive(self.path)

    @property
    def last_direction(self) -> Directions | None:
        if not self.path:
            return None
        return self.path[-1]

    @property
    def estimated(self) -> int:
        return int(abs(self.position.real - self.target.real) + abs(self.position.imag - self.target.imag))

    def __lt__(self, other: Step):
        return (self.cost + self.estimated * 10) < (other.cost + other.estimated * 10)


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
