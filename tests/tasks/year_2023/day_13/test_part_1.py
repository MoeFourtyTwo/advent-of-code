import pytest

from aoc.common.storage import get_data_path
from aoc.tasks.year_2023.day_13.part_1 import find_axis, go, transpose

TEST_PATH = get_data_path(__file__, "test.txt")


def test_year_2023_day_13_part_1_go():
    assert go(TEST_PATH) == 405


@pytest.mark.parametrize(
    "data, expected",
    [(["..#", "..#", "#.#"], 1), (["..#", "#.#", "#.#"], 2), (["..#", ".##", "#.#"], 0)],
)
def test_find_axis(data, expected):
    assert find_axis(data) == expected


def test_transpose():
    data = ["##", ".."]

    assert transpose(data) == ["#.", "#."]
