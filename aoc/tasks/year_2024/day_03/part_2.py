from __future__ import annotations

import pathlib
import re

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)
    line = "".join(lines)
    pattern = r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))"
    matches = re.findall(pattern, line)

    enabled = True  # mul is enabled by default
    total = 0

    for instr in matches:
        match instr:
            case ("do()", *_):
                enabled = True
            case ("don't()", *_):
                enabled = False
            case (_, x, y):
                if enabled:
                    total += int(x) * int(y)

    return total
