from __future__ import annotations

import ast
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


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    matches = [[]]
    index = 0
    for line in lines:
        if line == "":
            matches.append([])
            index += 1
        else:
            matches[index].append(ast.literal_eval(line))

    total_sum = 0

    for index, (left, right) in enumerate(matches, start=1):
        if compare(left, right):
            total_sum += index

    logger.info(f"{total_sum=}")

    return total_sum
