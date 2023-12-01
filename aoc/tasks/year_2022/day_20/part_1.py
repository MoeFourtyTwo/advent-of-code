from __future__ import annotations

import pathlib

from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


class EncryptedList:
    def __init__(self, data: list[int]) -> None:
        self.data = [(i, value) for i, value in enumerate(data)]

    def __getitem__(self, index: int) -> int:
        return self.data[index % (len(self.data))][1]

    def move(self, from_index: int, to_index: int) -> None:
        value = self.data.pop(from_index)
        self.data.insert(to_index, value)

    def decrypt(self) -> None:
        for value in self.data.copy():
            current_index = self.data.index(value)
            desired_index = (current_index + value[1]) % (len(self.data) - 1)
            self.move(current_index, desired_index)

    @property
    def grove_coordinates(self) -> int:
        data_reduced = [value for _, value in self.data]
        zero_index = data_reduced.index(0)
        return sum([self[zero_index + n] for n in (1000, 2000, 3000)])


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    file = list(map(int, lines))

    enc_list = EncryptedList(file)
    enc_list.decrypt()

    logger.info(f"{enc_list.grove_coordinates=}")

    return enc_list.grove_coordinates
