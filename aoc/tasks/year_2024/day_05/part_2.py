from __future__ import annotations

import functools
import pathlib
from collections import defaultdict

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def check_page_list(page_list: list[int], rules: dict[int, set[int]]) -> bool:
    left_set = set()
    for number in page_list:
        check_set = rules.get(number, set())

        if left_set & check_set:
            return False

        left_set.add(number)

    return True


def sort_page_list(page_list: list[int], rules: dict[int, set[int]]) -> list[int]:
    def compare(x, y):
        if y in rules.get(x, set()):
            return -1
        if x in rules.get(y, set()):
            return 1
        return 0

    return sorted(page_list, key=functools.cmp_to_key(compare))


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    sep_index = lines.index("")

    rules = defaultdict(set)

    for line in lines[:sep_index]:
        left, right = map(int, line.split("|"))
        rules[left].add(right)

    lists = [list(map(int, line.split(","))) for line in lines[sep_index + 1 :]]

    result = 0
    for page_list in lists:
        if check_page_list(page_list, rules):
            continue

        sorted_list = sort_page_list(page_list, rules)
        result += sorted_list[len(sorted_list) // 2]

    return result
