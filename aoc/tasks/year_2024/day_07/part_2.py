from __future__ import annotations

import math
import pathlib

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


def concat(left: int, right: int) -> int:
    return 10 ** (math.floor(math.log10(right)) + 1) * left + right


def eval_calibration(target: int, current: int, operands: list[int], index: int = 0) -> bool:
    if len(operands) == index:
        return target == current

    if current > target:
        return False

    return (
        eval_calibration(target, current + operands[index], operands, index + 1)
        or eval_calibration(target, current * operands[index], operands, index + 1)
        or eval_calibration(target, concat(current, operands[index]), operands, index + 1)
    )
