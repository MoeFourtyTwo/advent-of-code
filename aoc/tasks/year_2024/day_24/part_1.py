from __future__ import annotations

import operator
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    known_values = {}

    while True:
        line = lines.pop(0)
        if line:
            key, value = line.split(": ")
            known_values[key] = bool(int(value))
        else:
            break

    tasks = []

    operations = {"XOR": operator.xor, "OR": operator.or_, "AND": operator.and_}

    for line in lines:
        left, output = line.split(" -> ")
        source_1, operation, source_2 = left.split()
        tasks.append((source_1, source_2, operations[operation], output))

    while tasks:
        task = tasks.pop(0)
        source_1, source_2, operation, output = task
        if source_1 not in known_values or source_2 not in known_values:
            tasks.append(task)
            continue
        value_1 = known_values[source_1]
        value_2 = known_values[source_2]

        known_values[output] = operation(value_1, value_2)

    z_keys = sorted([key for key in known_values if key.startswith("z")], reverse=True)
    return int("".join(str(int(known_values[key])) for key in z_keys), 2)
