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
    *numbers, operators = get_lines(path, strip=False, rstrip=True)

    total = 0

    current_op = None
    current_numbers = []

    expected_len = max(len(number_list) for number_list in numbers)

    numbers = [f"{{:<{expected_len}}}".format(number_list) for number_list in numbers]
    operators = f"{{:<{expected_len}}}".format(operators)

    for index, op in enumerate(operators):
        if op in OPERATOR_MAP:
            if current_op is not None:
                total += functools.reduce(OPERATOR_MAP[current_op], current_numbers)
            current_op = op
            current_numbers = []

        current_number = 0
        for number_list in numbers:
            digit = number_list[index]

            if digit != " ":
                current_number = current_number * 10 + int(digit)

        if current_number != 0:
            current_numbers.append(current_number)

    total += functools.reduce(OPERATOR_MAP[current_op], current_numbers)

    return total
