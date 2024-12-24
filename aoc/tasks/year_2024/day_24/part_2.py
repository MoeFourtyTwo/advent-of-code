from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> str:
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

    all_outputs = set()

    for line in lines:
        left, output = line.split(" -> ")
        source_1, operation, source_2 = left.split()
        all_outputs.add(output)
        tasks.append((source_1, source_2, operation, output))

    t = []

    for key in all_outputs:
        if key.startswith("z"):
            t.append(key)

    last_z = max(t)

    suspicious = set()
    for op1, op2, op, res in tasks:
        # last op must be XOR except for the last z
        if res[0] == "z" and op != "XOR" and res != last_z:
            suspicious.add(res)
        # XOR must have at least one input from x, y, z
        if (
            op == "XOR"
            and res[0] not in ["x", "y", "z"]
            and op1[0] not in ["x", "y", "z"]
            and op2[0] not in ["x", "y", "z"]
        ):
            suspicious.add(res)

        # Check for AND operations not involving 'x00'
        if op == "AND" and "x00" not in [op1, op2]:
            for sub_op1, sub_op2, sub_op, sub_res in tasks:
                if (res == sub_op1 or res == sub_op2) and sub_op != "OR":
                    suspicious.add(res)

        # Check for XOR operations followed by OR operations
        if op == "XOR":
            for sub_op1, sub_op2, sub_op, sub_res in tasks:
                if (res == sub_op1 or res == sub_op2) and sub_op == "OR":
                    suspicious.add(res)

    return ",".join(sorted(suspicious))
