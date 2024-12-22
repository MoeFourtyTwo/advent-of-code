from __future__ import annotations

import pathlib
from collections import defaultdict

from rich.progress import track

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    seeds = list(map(int, lines))

    price_map: dict[tuple[int, int, int, int], int] = defaultdict(int)

    for seed in track(seeds):
        value = seed
        values = [value]

        for _ in range(2000):
            value = ((value * 64) ^ value) % 16777216
            value = ((value // 32) ^ value) % 16777216
            value = ((value * 2048) ^ value) % 16777216
            values.append(value)

        prices = [value % 10 for value in values]
        differences = [right - left for left, right in zip(prices, prices[1:])]

        seen = set()

        for i in range(3, len(differences)):
            key = (differences[i - 3], differences[i - 2], differences[i - 1], differences[i])

            if key in seen:
                continue

            price_map[key] += prices[i + 1]
            seen.add(key)

    return max(price_map.values())
