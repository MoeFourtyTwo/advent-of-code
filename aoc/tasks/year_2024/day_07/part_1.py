from __future__ import annotations

import functools
import operator
import pathlib
import typing

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    result = 0
    for target, current, operands in map(parse_line, lines):
        if eval_calibration(target, current, operands):
            result += target

    return result


def parse_line(line: str) -> tuple[int, int, list[int]]:
    target, operands = line.split(":")
    operands = list(map(int, operands.strip().split()))
    return int(target), operands[0], operands[1:]


def eval_calibration(target: int, current: int, operands: list[int]) -> bool:
    if len(operands) == 0:
        return target == current

    if target < calc_lower_bound(current, operands):
        return False

    if target > calc_upper_bound(current, operands):
        return False

    for op in [operator.add, operator.mul]:
        if eval_calibration(target, op(current, operands[0]), operands[1:]):
            return True

    return False


def collapse(op: typing.Callable[[int, int], int], current: int, operands: list[int]) -> int:
    return functools.reduce(op, operands, current)


def calc_upper_bound(current: int, operands: list[int]) -> int:
    for operand in operands:
        current = max(current + operand, current * operand)
    return current


def calc_lower_bound(current: int, operands: list[int]) -> int:
    for operand in operands:
        current = min(current + operand, current * operand)
    return current
