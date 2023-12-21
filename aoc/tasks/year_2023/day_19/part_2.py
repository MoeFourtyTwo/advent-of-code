from __future__ import annotations

import dataclasses
import functools
import operator
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def calculate_valid_input_ranges(workflows: dict[str, list[str]]) -> list[InputRange]:
    all_ranges = []
    for node, index in find_accept_states(workflows):
        predecessors = find_predecessors(workflows, node)
        input_range = find_valid_input(workflows, predecessors | {(node, index)})
        all_ranges.append(input_range)

    return all_ranges


def find_accept_states(workflows: dict[str, list[str]]) -> set[tuple[str, int]]:
    accept_states = set()
    for name, workflow in workflows.items():
        for index, step in enumerate(workflow):
            if outcome(step) == "A":
                accept_states.add((name, index))

    return accept_states


def outcome(step: str) -> str:
    return step.split(":")[-1]


def find_predecessors(workflows: dict[str, list[str]], node: str) -> set[tuple[str, int]]:
    predecessors = set()
    for name, workflow in workflows.items():
        for index, step in enumerate(workflow):
            if outcome(step) == node:
                predecessors.add((name, index))

    return predecessors | functools.reduce(
        operator.or_, [find_predecessors(workflows, n) for n, _ in predecessors], set()
    )


def find_valid_input(workflows: dict[str, list[str]], path: set[tuple[str, int]]) -> InputRange:
    failed_conditions = []
    passed_conditions = []
    for name, index in path:
        failed_conditions += workflows[name][:index]
        passed = workflows[name][index]
        if ":" in passed:
            passed_conditions += [passed]

    passed_conditions += [inverted_condition(step) for step in failed_conditions]

    input_range = InputRange()

    for passed_condition in passed_conditions:
        condition = passed_condition.split(":")[0]
        input_range.update_value(condition[0], condition[1], int(condition[2:]))

    return input_range


def inverted_condition(step: str) -> str:
    condition, _ = step.split(":")

    if "<" in condition:
        l, r = condition.split("<")  # noqa E741
        return l + ">" + str(int(r) - 1)

    if ">" in condition:
        l, r = condition.split(">")  # noqa E741
        return l + "<" + str(int(r) + 1)


@dataclasses.dataclass
class InputRange:
    x_min: int = 1
    x_max: int = 4001
    m_min: int = 1
    m_max: int = 4001
    a_min: int = 1
    a_max: int = 4001
    s_min: int = 1
    s_max: int = 4001

    def update_value(self, char: str, operation: str, value: int) -> None:
        if operation == "<":
            current_value = getattr(self, f"{char}_max")
            if value < current_value:
                setattr(self, f"{char}_max", value)
        elif operation == ">":
            value += 1
            current_value = getattr(self, f"{char}_min")
            if value > current_value:
                setattr(self, f"{char}_min", value)
        else:
            raise ValueError("Invalid input")

    def __len__(self) -> int:
        return max(
            (self.x_max - self.x_min)
            * (self.m_max - self.m_min)
            * (self.a_max - self.a_min)
            * (self.s_max - self.s_min),
            0,
        )

    def intersect(self, other: InputRange) -> InputRange:
        return InputRange(
            x_min=max(self.x_min, other.x_min),
            x_max=min(self.x_max, other.x_max),
            m_min=max(self.m_min, other.m_min),
            m_max=min(self.m_max, other.m_max),
            a_min=max(self.a_min, other.a_min),
            a_max=min(self.a_max, other.a_max),
            s_min=max(self.s_min, other.s_min),
            s_max=min(self.s_max, other.s_max),
        )


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    workflows = {}

    for index, line in enumerate(lines, start=1):
        if not line:
            break

        name, body = line[:-1].split("{")
        steps = body.split(",")
        workflows[name] = steps

    input_ranges = calculate_valid_input_ranges(workflows)

    total = sum(map(len, input_ranges))
    return total


if __name__ == "__main__":
    go()
