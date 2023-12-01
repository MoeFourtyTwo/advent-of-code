from __future__ import annotations

import dataclasses
from collections import defaultdict, deque

from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

STACKS_TYPE = dict[int, deque]
DATA_PATH = get_data_path(__file__)


def parse_stacks(lines: list[str]) -> STACKS_TYPE:

    index_row, *lines = reversed(lines)

    stacks = defaultdict(deque)

    for x_index, char in enumerate(index_row):
        if char.isnumeric():
            char_index = int(char)
            for row in lines:
                try:
                    crate = row[x_index]
                    if crate.isalpha():
                        stacks[char_index].append(crate)
                except IndexError:
                    break
    return stacks


@dataclasses.dataclass
class Move:
    from_stack: int
    to_stack: int
    count: int

    def apply(self, stacks: STACKS_TYPE) -> STACKS_TYPE:
        for _ in range(self.count):
            stacks[self.to_stack].append(stacks[self.from_stack].pop())
        return stacks

    @classmethod
    def parse(cls, line: str) -> Move:
        count, from_stack, to_stack = map(
            int, line.replace("move ", "").replace(" from ", " ").replace(" to ", " ").split()
        )
        return Move(from_stack=from_stack, to_stack=to_stack, count=count)


@timeit
def go():
    lines = get_lines(DATA_PATH, strip=False, rstrip=True)

    index = 0
    for index, line in enumerate(lines):
        if line == "":
            break

    stacks = parse_stacks(lines[:index])
    for move_line in lines[index + 1 :]:
        stacks = Move.parse(move_line).apply(stacks)

    answer = "".join(stacks[index][-1] for index in range(1, max(stacks.keys()) + 1))

    logger.info(f"{answer=}")
