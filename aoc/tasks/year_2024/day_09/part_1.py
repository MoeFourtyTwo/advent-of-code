from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    [raw_line] = get_lines(path)
    line = list(map(int, raw_line))

    check_sum = 0
    index = 0

    file_id_left = 0
    file_id_right = len(line) // 2

    take_left = True

    while line:
        if take_left:
            count = line.pop(0)
            file_id = file_id_left

            for _ in range(count):
                check_sum += file_id * index
                index += 1

            file_id_left += 1
            take_left = False

        else:
            while line[0] > 0 and line[-1] > 0:
                check_sum += file_id_right * index
                index += 1
                line[-1] -= 1
                line[0] -= 1

            if line[0] == 0 and line[-1] == 0:
                file_id_right -= 1
                take_left = True
                line.pop(0)
                line.pop()
                line.pop()  # remove gap as well
            elif line[0] > 0:
                # right is empty, gap not yet filled
                file_id_right -= 1
                take_left = False  # Still have to take from right
                line.pop()
                line.pop()  # remove gap as well
            else:
                # gap is filled, right still left
                take_left = True
                line.pop(0)

    return check_sum
