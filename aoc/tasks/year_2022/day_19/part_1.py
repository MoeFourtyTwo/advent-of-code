from __future__ import annotations

import dataclasses
import enum
import functools
import heapq
import operator
import pathlib
import typing

from loguru import logger
from tqdm import tqdm

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)

Robots = tuple[int, int, int, int]
Resources = tuple[int, int, int, int]
Cost = tuple[int, int, int, int]


class RockType(int, enum.Enum):
    ore = 0
    clay = 1
    obsidian = 2
    geode = 3


@dataclasses.dataclass(eq=True, frozen=True)
class SimulationState:
    remaining_time: int

    robots: Robots = (1, 0, 0, 0)
    resources: Resources = (0, 0, 0, 0)

    @property
    def priority(self) -> tuple[int, int, int, int]:
        return (
            -self.resources[RockType.geode],
            -self.resources[RockType.obsidian],
            -self.resources[RockType.clay],
            self.remaining_time,
        )

    def __lt__(self, other: SimulationState) -> bool:
        return self.priority < other.priority

    @property
    def max_geodes(self) -> int:
        return self.remaining_time * self.robots[RockType.geode] + self.resources[RockType.geode]

    @property
    def hypothetical_max_geodes(self) -> int:
        return self.max_geodes + self.remaining_time * (self.remaining_time - 1) // 2  # (sum(1...n) == n(n-1)

    def yield_next_states(self, blueprint: Blueprint) -> typing.Generator[SimulationState, None, None]:
        for rock in RockType:
            if rock != RockType.geode and self.robots[rock] >= blueprint.max_robots[rock]:
                # No longer required
                continue

            if any(
                self.robots[required_rock] == 0
                for required_rock in RockType
                if blueprint.robot_costs[rock][required_rock] > 0
            ):
                # No need to try to build a robot that we are missing resource
                continue

            time_needed = 1 + max(
                [
                    max(blueprint.robot_costs[rock][r] - self.resources[r] + self.robots[r] - 1, 0) // self.robots[r]
                    for r in RockType
                    if blueprint.robot_costs[rock][r] > 0
                ]
            )

            if time_needed >= self.remaining_time:
                continue

            # noinspection PyTypeChecker
            yield SimulationState(
                remaining_time=self.remaining_time - time_needed,
                robots=tuple(value + 1 if index == rock else value for index, value in enumerate(self.robots)),
                resources=tuple(
                    value + self.robots[index] * time_needed - blueprint.robot_costs[rock][index]
                    for index, value in enumerate(self.resources)
                ),
            )


@dataclasses.dataclass(eq=True, frozen=True)
class Blueprint:
    identifier: int

    robot_costs: tuple[Cost, Cost, Cost, Cost]
    max_robots: tuple[int, int, int, int]

    @classmethod
    def parse(cls, line: str) -> Blueprint:
        identifier_part, costs_part = line.split(":")
        identifier = int(identifier_part.split()[-1])
        parsed = list(map(cls._parse_robot, costs_part.split(". ")))
        robot_costs = tuple(parsed)
        max_robots = tuple(max(robot_costs, key=operator.itemgetter(i))[i] for i in range(3))
        return Blueprint(identifier, robot_costs, max_robots)

    @classmethod
    def _parse_robot(cls, cost_part: str) -> Cost:
        costs = cost_part.split("costs ")[1].split(" and ")
        parsed = {"ore": 0, "clay": 0, "obsidian": 0}
        for cost in costs:
            c, name = cost.split()
            parsed[name.removesuffix(".")] = int(c)
        return parsed["ore"], parsed["clay"], parsed["obsidian"], 0

    def simulate(self, n: int) -> int:
        heap = []
        initial_state = SimulationState(remaining_time=n)

        known_states = {initial_state}
        max_geodes = initial_state.max_geodes
        heapq.heappush(heap, initial_state)

        while heap:
            state: SimulationState = heapq.heappop(heap)

            for next_state in state.yield_next_states(self):
                if next_state not in known_states and next_state.hypothetical_max_geodes > max_geodes:
                    max_geodes = max(next_state.max_geodes, max_geodes)
                    known_states.add(next_state)
                    heapq.heappush(heap, next_state)

        return max_geodes


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    blueprints = list(map(Blueprint.parse, lines))

    summed = functools.reduce(
        operator.add, (index * blueprint.simulate(24) for index, blueprint in enumerate(tqdm(blueprints), start=1))
    )

    logger.info(f"{summed=}")

    return summed
