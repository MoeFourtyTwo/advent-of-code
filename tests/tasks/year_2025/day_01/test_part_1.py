import typing

import pytest

from aoc.common.storage import get_data_path
from aoc.tasks.year_2025.day_01.part_1 import go, rotate

TEST_PATH = get_data_path(__file__, "test.txt")


@pytest.mark.parametrize(
    "initial_value,steps,direction,expected_value",
    [
        (11, 8, "R", 19),
        (19, 19, "L", 0),
        (0, 1, "L", 99),
        (99, 1, "R", 0),
    ],
)
def test_rotate(initial_value: int, steps: int, direction: typing.Literal["L", "R"], expected_value: int):
    assert rotate(initial_value, steps, direction) == expected_value


def test_year_2025_day_01_part_1_go():
    assert go(TEST_PATH) == 3
