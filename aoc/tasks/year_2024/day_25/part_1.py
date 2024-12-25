from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)

KEY_TYPE = tuple[int, int, int, int, int]


def fits(key: KEY_TYPE, lock: KEY_TYPE) -> bool:
    return all(key_part + lock_part <= 5 for key_part, lock_part in zip(key, lock))


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    locks = []
    keys = []

    for index in range(0, len(lines), 8):
        if lines[index][0] == "#":  # is lock
            target = locks
        else:
            target = keys
        value = tuple(column[1:-1].count("#") for column in zip(*lines[index : index + 7]))
        target.append(value)

    total = 0

    while keys:
        key = keys.pop()
        total += sum(fits(key, lock) for lock in locks)

    return total
