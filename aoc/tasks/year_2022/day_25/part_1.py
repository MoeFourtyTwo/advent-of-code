from __future__ import annotations

import math
import pathlib

from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)

SNAFU_TABLE = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}


def convert_to_int(snafu_number: str) -> int:
    total = 0
    for i, char in enumerate(reversed(snafu_number)):
        total += SNAFU_TABLE[char] * 5**i
    return total


def convert_to_snafu(number: int) -> str:
    l = round(math.log(number, 5))  # noqa E741

    snafu_digits = ""
    int_value = 0

    for index in range(l, -1, -1):
        target = number - int_value

        current_digit = ""
        diff = math.inf

        for snafu, digit in SNAFU_TABLE.items():
            value = abs(digit * 5**index - target)

            if value < diff:
                current_digit = snafu
                diff = value

        snafu_digits += current_digit
        filled = snafu_digits.ljust(l + 1, "0")
        int_value = convert_to_int(filled)

    return snafu_digits


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)
    total_snafu = convert_to_snafu(sum(map(convert_to_int, lines)))

    logger.info(f"{total_snafu=}")

    return total_snafu
