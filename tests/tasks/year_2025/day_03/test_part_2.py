import pytest

from aoc.common.storage import get_data_path
from aoc.tasks.year_2025.day_03.part_2 import extract_joltage, go

TEST_PATH = get_data_path(__file__, "test.txt")


@pytest.mark.parametrize(
    "line,expected",
    [
        ("987654321111111", 987654321111),
        ("811111111111119", 811111111119),
        ("234234234234278", 434234234278),
        ("818181911112111", 888911112111),
    ],
)
def test_extract_joltage(line: str, expected: int):
    assert extract_joltage(line) == expected


def test_year_2025_day_03_part_2_go():
    assert go(TEST_PATH) == 3121910778619
