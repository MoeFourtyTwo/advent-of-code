from __future__ import annotations

import collections
import dataclasses
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def calc_hash(data: str) -> int:
    current_value = 0
    for char in data:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    [line] = get_lines(path)

    data = collections.defaultdict(collections.OrderedDict)

    for step in line.split(","):
        if step[-1] == "-":
            label = step[:-1]
            hash_value = calc_hash(label)

            try:
                del data[hash_value][label]
            except KeyError:
                pass

        else:
            label = step[:-2]
            hash_value = calc_hash(label)
            data[hash_value][label] = int(step[-1])

    total = sum(
        (box_number + 1) * slot * focal_length
        for box_number, value in data.items()
        for slot, focal_length in enumerate(value.values(), start=1)
    )

    return total
