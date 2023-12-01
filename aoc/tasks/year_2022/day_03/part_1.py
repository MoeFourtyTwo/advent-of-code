from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


def score(value: set[str]) -> int:
    [actual_value] = value

    if actual_value.isupper():
        return ord(actual_value) - ord("A") + 27
    else:
        return ord(actual_value) - ord("a") + 1


@timeit
def go():
    lines = get_lines(DATA_PATH)
    total_priority = sum(score(set(line[: len(line) // 2]).intersection(line[len(line) // 2 :])) for line in lines)

    logger.info(f"{total_priority=}")
