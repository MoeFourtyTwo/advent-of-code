import pytest

from aoc.common.storage import get_data_path
from aoc.tasks.year_2024.day_16.part_2 import go

TEST_PATH = get_data_path(__file__, "test.txt")


@pytest.mark.parametrize(
    "test_file_name,expected",
    [
        ("test.txt", 45),
        ("test2.txt", 64),
    ],
)
def test_year_2024_day_16_part_1_go(test_file_name: str, expected: int):
    assert go(get_data_path(__file__, test_file_name)) == expected
