from __future__ import annotations

import dataclasses
import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@dataclasses.dataclass
class Node:
    count: int


@dataclasses.dataclass
class Gap(Node):
    pass


@dataclasses.dataclass
class File(Node):
    file_id: int


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    [raw_line] = get_lines(path)

    nodes = []
    file_id = 0

    is_gap = False
    for value in map(int, raw_line):
        if is_gap:
            nodes.append(Gap(count=value))
        else:
            nodes.append(File(count=value, file_id=file_id))
            file_id += 1
        is_gap = not is_gap

    for index in range(len(nodes) - 1, 0, -1):
        if isinstance(nodes[index], Gap):
            continue

        for search_index in range(index):
            if not isinstance(nodes[search_index], Gap):
                continue

            if nodes[search_index].count >= nodes[index].count:
                missing_count = nodes[search_index].count - nodes[index].count
                nodes[search_index] = nodes[index]
                nodes[index] = Gap(count=nodes[index].count)

                if missing_count > 0:
                    nodes.insert(search_index + 1, Gap(count=missing_count))
                    index += 1  # to compensate for insert
                break

    checksum = 0
    index = 0
    for node in nodes:
        for _ in range(node.count):
            if isinstance(node, File):
                to_add = node.file_id * index
                checksum += to_add
            index += 1
    return checksum
