from __future__ import annotations

import pathlib

import z3
from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    split_lines = [tuple(line.split(": ")) for line in lines]
    variables = {name: z3.Real(name) for name, _ in split_lines}

    s = z3.Solver()
    for name, constraint in split_lines:
        match [name] + constraint.split(" "):
            case ["root", l, _, r]:
                s.add(variables[l] == variables[r])
            case ["humn", _]:
                pass
            case [n, v]:
                s.add(variables[n] == int(v))
            case [n, l, "+", r]:
                s.add(variables[n] == variables[l] + variables[r])
            case [n, l, "-", r]:
                s.add(variables[n] == variables[l] - variables[r])
            case [n, l, "/", r]:
                s.add(variables[n] == variables[l] / variables[r])
            case [n, l, "*", r]:
                s.add(variables[n] == variables[l] * variables[r])

    assert s.check() == z3.sat
    solution = s.model()
    human_value = solution[variables["humn"]].as_long()
    logger.info(f"{human_value}")

    return human_value
