from __future__ import annotations

import dataclasses

from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@dataclasses.dataclass
class Node:
    name: str
    children: dict[str, Node] = dataclasses.field(default_factory=dict)
    parent: Node | None = None

    def __len__(self) -> int:
        return sum(len(child) for child in self.children.values())

    def __getitem__(self, item: str) -> Node:
        if item == "..":
            return self.parent
        return self.children[item]

    def __setitem__(self, key: str, value: Node) -> None:
        value.parent = self
        self.children[key] = value

    def __iter__(self):
        return iter(self.children.values())

    @property
    def is_directory(self) -> bool:
        return True


@dataclasses.dataclass
class File(Node):
    size: int = 0

    def __len__(self) -> int:
        return self.size

    @property
    def is_directory(self) -> bool:
        return False


def parse_output(lines: list[str]) -> Node:
    root = Node(name="/")
    current_node = root

    for line in lines:
        match line.split():
            case ["$", "ls"]:
                pass
            case ["$", "cd", "/"]:
                current_node = root
            case ["$", "cd", target]:
                current_node = current_node[target]
            case ["dir", name]:
                current_node[name] = Node(name)
            case [size, name]:
                current_node[name] = File(name, size=int(size))
    return root


@timeit
def go():
    lines = get_lines(DATA_PATH)
    root = parse_output(lines)

    targets = []

    def find_largest(node: Node):
        for child in node:
            if child.is_directory:
                if len(child) <= 100_000:
                    targets.append(child)
                find_largest(child)

    find_largest(root)

    total_size = sum(len(node) for node in targets)

    logger.info(f"{total_size=}")
