from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go():
    [line] = get_lines(DATA_PATH)

    index = 0
    l = 4  # noqa E741
    for index in range(l, len(line)):
        s = set(line[index - l : index])
        if len(s) == l:
            break

    logger.info(f"{index=}")
