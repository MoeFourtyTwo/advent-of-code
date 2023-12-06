import pytest

from aoc.common.storage import get_data_path
from aoc.tasks.year_2023.day_05.part_1 import convert, go

TEST_PATH = get_data_path(__file__, "test.txt")


def test_year_2023_day_05_part_1_go():
    assert go(TEST_PATH) == 35


@pytest.mark.parametrize(
    "source, target",
    [
        (79, 81),
        (14, 14),
        (55, 57),
        (13, 13),
    ],
)
def test_convert(source: int, target: int):
    assert convert(source, ((50, 98, 2), (52, 50, 48))) == target
