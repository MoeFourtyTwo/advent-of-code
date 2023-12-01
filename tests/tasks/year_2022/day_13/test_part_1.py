import pytest

from aoc.common.storage import get_data_path
from aoc.tasks.year_2022.day_13.part_1 import compare, go

TEST_PATH = get_data_path(__file__, "test.txt")


def test_year_2022_day_13_part_1_go():
    assert go(TEST_PATH) == 13


@pytest.mark.parametrize(
    "left, right, expected",
    [
        [[1, 1, 3, 1, 1], [1, 1, 5, 1, 1], True],
        [[[1], [2, 3, 4]], [[1], 4], True],
        [[9], [[8, 7, 6]], False],
        [[[4, 4], 4, 4], [[4, 4], 4, 4, 4], True],
        [[7, 7, 7, 7], [7, 7, 7], False],
        [[], [3], True],
        [[[[]]], [[]], False],
        [[1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9], False],
    ],
)
def test_compare(left, right, expected):
    assert compare(left, right) == expected
