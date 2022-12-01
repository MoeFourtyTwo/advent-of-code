from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go():
    data = get_lines(DATA_PATH)

    calorie_list = [0]
    index = 0

    for line in data:
        if len(line) > 0:
            calorie_list[index] += int(line)
        else:
            index += 1
            calorie_list.append(0)

    logger.info(f"{max(calorie_list)=}")
