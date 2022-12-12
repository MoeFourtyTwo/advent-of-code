from __future__ import annotations

import dataclasses
import functools
import heapq
import operator
import pathlib
from collections import defaultdict
from typing import Callable

from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@dataclasses.dataclass
class Monkey:
    operation: Callable[[int], int]
    test_value: int
    pass_monkey_identifier: int
    fail_monkey_identifier: int
    monkey_map: dict[int, Monkey]
    items: list[int] = dataclasses.field(default_factory=list)

    inspection_counter: int = 0

    @classmethod
    def parse_lines(cls, lines: list[str], monkey_map: dict[int, Monkey]) -> Monkey:
        _, item_line, operation_line, test_line, pass_line, fail_line = lines

        return Monkey(
            items=cls._parse_item_line(item_line),
            operation=cls._parse_operation_line(operation_line),
            test_value=cls._extract_numbers(test_line),
            pass_monkey_identifier=cls._extract_numbers(pass_line),
            fail_monkey_identifier=cls._extract_numbers(fail_line),
            monkey_map=monkey_map,
        )

    @classmethod
    def _parse_item_line(cls, line: str) -> list[int]:
        return list(map(int, line.strip().removeprefix("Starting items: ").split(", ")))

    @classmethod
    def _parse_operation_line(cls, line: str) -> Callable[[int], int]:
        line = line.strip().removeprefix("Operation: new = ")
        unsafe_lambda = eval(f"lambda old: {line}")
        return unsafe_lambda

    @classmethod
    def _extract_numbers(cls, line: str) -> int:
        return int("".join(char for char in line if char.isdigit()))

    def catch(self, item: int) -> None:
        self.items.append(item)

    def step(self) -> None:
        while len(self.items) > 0:
            self.inspect_item(self.items.pop(0))

    def inspect_item(self, item: int):
        item = self.operation(item)
        item //= 3

        if item % self.test_value == 0:
            self.monkey_map[self.pass_monkey_identifier].catch(item)
        else:
            self.monkey_map[self.fail_monkey_identifier].catch(item)

        self.inspection_counter += 1


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    subsets = defaultdict(list)
    index = 0
    for line in lines:
        if line != "":
            subsets[index].append(line)
        else:
            index += 1
    monkey_map = {}

    for index, lines in subsets.items():
        monkey_map[index] = Monkey.parse_lines(lines, monkey_map)

    for _ in range(20):
        for monkey in monkey_map.values():
            monkey.step()

    monkey_business = int(
        functools.reduce(operator.mul, heapq.nlargest(2, [monkey.inspection_counter for monkey in monkey_map.values()]))
    )

    logger.info(f"{monkey_business=}")

    return monkey_business
