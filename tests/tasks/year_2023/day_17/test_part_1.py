import pytest

from aoc.common.storage import get_data_path
from aoc.tasks.year_2023.day_17.part_1 import Directions, count_consecutive, go

TEST_PATH = get_data_path(__file__, "test.txt")


def test_year_2023_day_17_part_1_go():
    assert go(TEST_PATH) == 102


@pytest.mark.parametrize(
    "path, count",
    [
        ([Directions.UP, Directions.UP, Directions.UP], 3),
        ([Directions.UP, Directions.UP, Directions.DOWN], 1),
        ([Directions.UP, Directions.DOWN, Directions.DOWN], 2),
        ([], 0),
    ],
)
def test_count_consecutive(path, count):
    assert count_consecutive(path) == count
