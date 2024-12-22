from __future__ import annotations

import pathlib

from rich.progress import track

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    seeds = list(map(int, lines))

    price_maps: list[dict[tuple[int, int, int, int], int]] = []
    all_sequences: set[tuple[int, int, int, int]] = set()

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

        price_map = {}

        for i in range(3, len(differences)):
            key = (differences[i - 3], differences[i - 2], differences[i - 1], differences[i])

            if key in price_map:
                continue

            price_map[key] = prices[i + 1]
            all_sequences.add(key)

        price_maps.append(price_map)

    max_profit = 0

    for sequence in track(all_sequences):
        profit = 0

        for price_map in price_maps:
            profit += price_map.get(sequence, 0)

        max_profit = max(max_profit, profit)

    return max_profit
