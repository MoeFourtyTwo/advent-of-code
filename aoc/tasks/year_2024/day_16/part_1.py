from __future__ import annotations

import dataclasses
import heapq
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)

DIRECTIONS = {
    "N": complex(0, -1),
    "E": complex(1, 0),
    "S": complex(0, 1),
    "W": complex(-1, 0),
}

CLOCKWISE = {
    DIRECTIONS["N"]: DIRECTIONS["E"],
    DIRECTIONS["E"]: DIRECTIONS["S"],
    DIRECTIONS["S"]: DIRECTIONS["W"],
    DIRECTIONS["W"]: DIRECTIONS["N"],
}
COUNTER_CLOCKWISE = {last: first for first, last in CLOCKWISE.items()}


@dataclasses.dataclass
class Node:
    position: complex
    cost: int
    direction: complex

    def __lt__(self, other: Node) -> bool:
        return self.cost < other.cost


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    grid = {}

    start = complex(0, 0)
    goal = complex(0, 0)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                grid[complex(x, y)] = char
            if char == "S":
                start = complex(x, y)
            if char == "E":
                goal = complex(x, y)

    known_cost = {}

    open_positions = [Node(start, 0, DIRECTIONS["E"])]

    while open_positions:
        node = heapq.heappop(open_positions)
        key = (node.position, node.direction)

        if key in known_cost and known_cost[key] <= node.cost:
            continue

        known_cost[key] = node.cost

        if node.position == goal:
            return node.cost

        if node.position + node.direction not in grid:
            heapq.heappush(open_positions, Node(node.position + node.direction, node.cost + 1, node.direction))

        heapq.heappush(open_positions, Node(node.position, node.cost + 1000, CLOCKWISE[node.direction]))
        heapq.heappush(open_positions, Node(node.position, node.cost + 1000, COUNTER_CLOCKWISE[node.direction]))
