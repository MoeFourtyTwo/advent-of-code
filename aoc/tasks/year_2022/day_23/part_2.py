from __future__ import annotations

import collections
import pathlib
import typing
from operator import attrgetter

from tqdm import tqdm

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)

SURROUND = [-1 - 1j, -1, -1 + 1j, -1j, 1j, 1 - 1j, 1, 1 + 1j]

DIRECTIONS_LIST_TYPE: typing.TypeAlias = list[tuple[complex, tuple[complex, complex, complex]]]


def determine_next_move(
    elf_position: complex, directions_list: DIRECTIONS_LIST_TYPE, static_elves: set[complex]
) -> complex:
    if any(elf_position + offset in static_elves for offset in SURROUND):
        for elf_offset, directions in directions_list:
            if all(elf_position + offset not in static_elves for offset in directions):
                return elf_position + elf_offset

    return elf_position


def visualize(elves: list[complex]) -> None:
    min_x = int(min(elves, key=attrgetter("real")).real)
    max_x = int(max(elves, key=attrgetter("real")).real)
    min_y = int(min(elves, key=attrgetter("imag")).imag)
    max_y = int(max(elves, key=attrgetter("imag")).imag)

    field = [["."] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]

    for elf in elves:
        field[int(elf.imag) + min_y][int(elf.real) + min_x] = "#"

    print()
    for row in field:
        print("".join(row))


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)
    elves = [complex(x, y) for y, line in enumerate(lines) for x, char in enumerate(line) if char == "#"]

    directions_list = [
        (-1j, (-1 - 1j, -1j, 1 - 1j)),  # NORTH
        (1j, (-1 + 1j, 1j, 1 + 1j)),  # SOUTH
        (-1 + 0j, (-1 - 1j, -1 + 0j, -1 + 1j)),  # WEST
        (1 + 0j, (1 - 1j, 1 + 0j, 1 + 1j)),  # EAST
    ]

    static_elves = frozenset(elves)
    last_hash = hash(static_elves)
    round = 1
    with tqdm() as pbar:
        while True:
            pbar.update(1)
            proposed_moves = [
                determine_next_move(elf_position, directions_list, static_elves) for elf_position in elves
            ]

            counts = collections.Counter(proposed_moves)

            elves = [
                proposed_move if counts[proposed_move] == 1 else original_position
                for original_position, proposed_move in zip(elves, proposed_moves)
            ]

            directions_list = directions_list[1:] + directions_list[:1]
            static_elves = frozenset(elves)
            new_hash = hash(static_elves)

            if new_hash == last_hash:
                return round
            else:
                round += 1
                last_hash = new_hash
