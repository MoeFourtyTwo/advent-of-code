from __future__ import annotations

import functools
import pathlib
from collections import Counter

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)

CARD_RANKS = {k: r for r, k in enumerate(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"])}
HAND_RANKS = [[5], [4, 1], [3, 2], [3, 1, 1], [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1, 1]]


def rank_hand(hand: str) -> int:
    hand_count = sorted(Counter(hand).values(), reverse=True)
    for index, hand_rank in enumerate(HAND_RANKS):
        if hand_count == hand_rank:
            return index
    raise ValueError(f"Unexpected input: {hand}.")


def compare(hand_x: str, hand_y: str) -> int:
    rank_x = rank_hand(hand_x)
    rank_y = rank_hand(hand_y)

    if rank_x != rank_y:
        return rank_x - rank_y

    for x, y in zip(hand_x, hand_y):
        if x != y:
            return CARD_RANKS[x] - CARD_RANKS[y]

    return 0


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    hand_bid_pairs = [line.split() for line in lines]
    hand_bid_pairs = sorted(hand_bid_pairs, key=lambda x: functools.cmp_to_key(compare)(x[0]))

    return sum(rank * int(bid) for rank, (_, bid) in enumerate(reversed(hand_bid_pairs), start=1))
