import pytest

from aoc.common.storage import get_data_path
from aoc.tasks.year_2025.day_03.part_1 import extract_joltage, go

TEST_PATH = get_data_path(__file__, "test.txt")


@pytest.mark.parametrize(
    "line,expected",
    [
        ("987654321111111", 98),
        ("811111111111119", 89),
        ("234234234234278", 78),
        ("818181911112111", 92),
    ],
)
def test_extract_joltage(line: str, expected: int):
    assert extract_joltage(line) == expected


def test_year_2025_day_03_part_1_go():
    assert go(TEST_PATH) == 357
