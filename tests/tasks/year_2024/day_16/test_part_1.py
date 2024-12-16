import pytest

from aoc.common.storage import get_data_path
from aoc.tasks.year_2024.day_16.part_1 import go


@pytest.mark.parametrize(
    "test_file_name,expected",
    [
        ("test.txt", 7036),
        ("test2.txt", 11048),
    ],
)
def test_year_2024_day_16_part_1_go(test_file_name: str, expected: int):
    assert go(get_data_path(__file__, test_file_name)) == expected
