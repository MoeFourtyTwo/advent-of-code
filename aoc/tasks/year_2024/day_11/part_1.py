from __future__ import annotations

import pathlib
from collections import Counter, defaultdict

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    [line] = get_lines(path)
    numbers = Counter(map(int, line.split()))

    for _ in range(25):
        new_numbers = defaultdict(int)
        for number, count in numbers.items():
            if number == 0:
                new_numbers[1] += count
            elif (length := len(str(number))) % 2 == 0:
                left = str(number)[: length // 2]
                right = str(number)[length // 2 :]
                new_numbers[int(left)] += count
                new_numbers[int(right)] += count
            else:
                new_numbers[number * 2024] += count
        numbers = new_numbers

    return sum(numbers.values())
