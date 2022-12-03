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

    total_priority = sum(
        score(set(lines[i]).intersection(lines[i + 1]).intersection(lines[i + 2])) for i in range(0, len(lines), 3)
    )

    logger.info(f"{total_priority=}")
