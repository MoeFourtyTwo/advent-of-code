from __future__ import annotations

import pathlib
from collections import defaultdict

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def check_page_list(page_list: list[int], rules: dict[int, set[int]]) -> int:
    left_set = set()
    for number in page_list:
        check_set = rules.get(number, set())

        if left_set & check_set:
            return 0

        left_set.add(number)

    return page_list[len(page_list) // 2]


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    sep_index = lines.index("")

    rules = defaultdict(set)

    for line in lines[:sep_index]:
        left, right = map(int, line.split("|"))
        rules[left].add(right)

    lists = [list(map(int, line.split(","))) for line in lines[sep_index + 1 :]]

    return sum(check_page_list(page_list, rules) for page_list in lists)
