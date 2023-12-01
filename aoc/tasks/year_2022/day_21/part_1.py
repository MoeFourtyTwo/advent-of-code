from __future__ import annotations

import dataclasses
import operator
import pathlib
import typing

from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)

TREE: typing.TypeAlias = dict[str, typing.Union["Value", "Node"]]


@dataclasses.dataclass
class Value:
    value: int

    def resolve(self, data: TREE) -> int:
        return self.value


@dataclasses.dataclass
class Node:
    first: str
    second: str
    operation: typing.Callable[[int, int], int]

    def resolve(self, data: TREE) -> int:
        return self.operation(data[self.first].resolve(data), data[self.second].resolve(data))


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    tree = {}

    for line in lines:
        name, value = line.split(": ")

        match value.split(" "):
            case [value]:
                tree[name] = Value(int(value))
            case [first, "+", second]:
                tree[name] = Node(first, second, operator.add)
            case [first, "-", second]:
                tree[name] = Node(first, second, operator.sub)
            case [first, "/", second]:
                tree[name] = Node(first, second, operator.floordiv)
            case [first, "*", second]:
                tree[name] = Node(first, second, operator.mul)

    root_value = tree["root"].resolve(tree)

    logger.info(f"{root_value=}")

    return root_value
