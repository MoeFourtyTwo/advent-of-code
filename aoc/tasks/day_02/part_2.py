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
    def get(cls, index: int) -> Move:
        if index < 1:
            index += 3
        if index > 3:
            index -= 3

        return Move(index)

    @classmethod
    def parse(cls, value: str) -> Move:
        return {"A": Move.rock, "B": Move.paper, "C": Move.scissors}.get(value)

    def get_based_on_outcome(self, outcome: int) -> Move:
        if outcome == 0:
            return self
        return Move.get(self.value + outcome)


DECODE_MAP = {"X": -1, "Y": 0, "Z": 1}


@timeit
def go():
    lines = get_lines(DATA_PATH)

    score = 0

    for line in track(lines):
        opponent, player = line.split(" ")
        opponent_move = Move.parse(opponent)
        player_move = opponent_move.get_based_on_outcome(DECODE_MAP[player])

        score += player_move.match(opponent_move)
        score += player_move.score()

    logger.info(f"{score=}")
