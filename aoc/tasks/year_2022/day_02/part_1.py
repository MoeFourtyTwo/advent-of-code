from __future__ import annotations

import enum

from loguru import logger
from rich.progress import track

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)

SCORE_MAP = {"A": 1, "B": 2, "C": 3}


class Move(int, enum.Enum):
    rock = 1
    paper = 2
    scissors = 3

    def match(self, other: Move) -> int:
        if self == other:
            return 3

        if self == Move.rock:
            if other == Move.paper:
                return 0
            if other == Move.scissors:
                return 6
        if self == Move.paper:
            if other == Move.scissors:
                return 0
            if other == Move.rock:
                return 6
        if self == Move.scissors:
            if other == Move.rock:
                return 0
            if other == Move.paper:
                return 6

        raise ValueError(f"Invalid input! {self=}  {other=}")

    def score(self) -> int:
        return self.value

    @classmethod
    def parse(cls, value: str) -> Move:
        return {"A": Move.rock, "B": Move.paper, "C": Move.scissors}.get(value)


DECODE_MAP = {"X": "A", "Y": "B", "Z": "C"}


@timeit
def go():
    lines = get_lines(DATA_PATH)

    score = 0

    for line in track(lines):
        opponent, player = line.split(" ")
        player = Move.parse(DECODE_MAP[player])
        score += player.match(Move.parse(opponent))
        score += player.score()

    logger.info(f"{score=}")
