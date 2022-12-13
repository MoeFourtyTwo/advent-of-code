from __future__ import annotations

import ast
import functools
import operator
import pathlib

from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


SIGNAL_TYPE = list[list["SIGNAL_TYPE"] | int]


def compare(left: SIGNAL_TYPE, right: SIGNAL_TYPE) -> bool | None:
    left_gen = iter(left)
    right_gen = iter(right)

    result = None

    while True:
        try:
            next_left = next(left_gen)
        except StopIteration:
            try:
                next(right_gen)
                return True
            except StopIteration:
                return None
        try:
            next_right = next(right_gen)
        except StopIteration:
            return False

        match next_left, next_right:
            case [list(), list()]:
                result = result or compare(next_left, next_right)
            case [list(), int()]:
                result = result or compare(next_left, [next_right])
            case [int(), list()]:
                result = result or compare([next_left], next_right)
            case [int(), int()]:
                if next_left < next_right:
                    return True
                if next_left > next_right:
                    return False

        if result is not None:
            return result


@functools.cmp_to_key
def compare_for_comparator(left: SIGNAL_TYPE, right: SIGNAL_TYPE) -> int:
    result = compare(left, right)
    if result is None:
        return 0
    elif result:
        return -1
    else:
        return 1


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    matches = []
    for line in lines:
        if line != "":
            matches.append(ast.literal_eval(line))

    matches.append([[2]])
    matches.append([[6]])

    matches = sorted(matches, key=compare_for_comparator)

    decoder_key = functools.reduce(
        operator.mul, [index for index, row in enumerate(matches, start=1) if row in ([[2]], [[6]])]
    )

    logger.info(f"{decoder_key=}")

    return decoder_key
