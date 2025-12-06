from __future__ import annotations

import functools
import operator
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


OPERATOR_MAP = {"+": operator.add, "*": operator.mul}


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    number_lists = [list(map(int, line.split())) for line in lines[:-1]]

    operator_list = lines[-1].split()

    total = 0

    for op, numbers in zip(operator_list, zip(*number_lists)):
        total += functools.reduce(OPERATOR_MAP[op], numbers)

    return total
