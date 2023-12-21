from __future__ import annotations

import json
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def handle_single(workflows: dict[str, list[str]], data: dict[str, int], value: str) -> bool:
    if value == "A":
        return True
    if value == "R":
        return False
    return evaluate(workflows, data, value)


def evaluate(workflows: dict[str, list[str]], data: dict[str, int], workflow_name: str) -> bool:
    current_workflow = workflows[workflow_name]

    for step in current_workflow:
        if ":" not in step:
            return handle_single(workflows, data, step)

        condition, response = step.split(":")

        if "<" in condition:
            l, r = condition.split("<")  # noqa E741
            if data[l] < int(r):
                return handle_single(workflows, data, response)

        if ">" in condition:
            l, r = condition.split(">")  # noqa E741
            if data[l] > int(r):
                return handle_single(workflows, data, response)

    return False


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    index = 0

    workflows = {}

    for index, line in enumerate(lines, start=1):
        if not line:
            break

        name, body = line[:-1].split("{")
        workflows[name] = body.split(",")

    total_accepted = 0
    for line in lines[index:]:
        data: dict[str, int] = json.loads(
            line.replace("=", ":").replace("x", '"x"').replace("m", '"m"').replace("a", '"a"').replace("s", '"s"')
        )
        value = evaluate(workflows, data, "in")
        if value:
            total_accepted += sum(data.values())

    return total_accepted
