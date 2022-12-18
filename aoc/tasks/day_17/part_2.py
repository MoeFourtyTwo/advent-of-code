from __future__ import annotations

import pathlib
import typing

import numpy as np
from loguru import logger
from tqdm import trange

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def jet_stream_generator(line: str) -> typing.Generator[tuple[int, int], None, None]:
    while True:
        for index, char in enumerate(line):
            if char == "<":
                yield index, -1
            if char == ">":
                yield index, 1


def rock_generator() -> typing.Generator[tuple[int, np.ndarray], None, None]:
    while True:
        yield 0, np.array([[1, 1, 1, 1]])
        yield 1, np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
        yield 2, np.array([[0, 0, 1], [0, 0, 1], [1, 1, 1]])
        yield 3, np.array([[1], [1], [1], [1]])
        yield 4, np.array([[1, 1], [1, 1]])


def generate_rows(n: int = 1) -> np.ndarray:
    return np.array([[1, 0, 0, 0, 0, 0, 0, 0, 1]] * n)


def check_collision(field: np.ndarray, rock: np.ndarray, x: int, y: int) -> bool:
    relevant_section = field[y : y + rock.shape[0], x : x + rock.shape[1]]
    return np.any(relevant_section & rock)


def hash_field(field: np.ndarray, rock_index: int, stream_index: int) -> tuple[int, int]:
    empty_rows = count_empty_rows(field)
    height = field.shape[0] - empty_rows - 1
    relevant_depth = max(np.argmax(field, axis=0))
    section = field[empty_rows:relevant_depth, 1:-1]
    hash_value = hash((section.data.tobytes(), rock_index, stream_index))
    return hash_value, height


def count_empty_rows(field: np.ndarray) -> int:
    empty_rows = 0
    for r in field:
        if all(r[1:-1] == 0):
            empty_rows += 1
        else:
            break
    return empty_rows


def prepare_field(field: np.ndarray, rock: np.ndarray) -> tuple[np.ndarray, int, int]:
    empty_rows = count_empty_rows(field)
    rock_height = rock.shape[0]
    required_lines = rock_height + 3

    new_lines = required_lines - empty_rows
    if new_lines > 0:
        new_rows = generate_rows(new_lines)
        field = np.concatenate((new_rows, field), axis=0)

    return field, 3, (max(0, -new_lines))


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    [line] = get_lines(path)

    jet_stream_iterator = jet_stream_generator(line)
    rock_iterator = rock_generator()

    field = np.array([[1] * 9])
    hashed_fields = {}
    previous_hash = None

    target_rock_index = 1000000000000
    for i in range(target_rock_index):
        rock_index, rock = next(rock_iterator)
        field, x, y = prepare_field(field, rock)

        while True:
            jet_stream_index, jet_stream = next(jet_stream_iterator)
            if not check_collision(field, rock, x + jet_stream, y):
                x += jet_stream

            collides = check_collision(field, rock, x, y + 1)

            if collides:
                field[y : y + rock.shape[0], x : x + rock.shape[1]] += rock

                hash_value, height = hash_field(field, rock_index, jet_stream_index)

                if hash_value not in hashed_fields:
                    hashed_fields[hash_value] = (height, previous_hash, i)
                    previous_hash = hash_value
                    break  # Go to next rock

                # Cycle detected
                height_at_cycle_start, _, rock_index_at_cycle_start = hashed_fields[hash_value]
                rock_count_in_cycle = i - rock_index_at_cycle_start
                cycle_count = (target_rock_index - rock_index_at_cycle_start) // rock_count_in_cycle + 1
                overshoot_height = height_at_cycle_start + cycle_count * (height - height_at_cycle_start)
                overshoot_rock_index = rock_index_at_cycle_start + cycle_count * rock_count_in_cycle

                # Track back to target rock
                while overshoot_rock_index > target_rock_index:
                    previous_hash = hashed_fields[previous_hash][1]
                    overshoot_rock_index -= 1

                # Adjust height
                total_height = overshoot_height - height + hashed_fields[previous_hash][0]
                logger.info(f"{total_height}")
                return total_height

            y += 1
