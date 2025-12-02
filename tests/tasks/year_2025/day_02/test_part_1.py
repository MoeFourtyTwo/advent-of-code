import pytest

from aoc.common.storage import get_data_path
from aoc.tasks.year_2025.day_02.part_1 import go, sum_invalid_ids

TEST_PATH = get_data_path(__file__, "test.txt")


@pytest.mark.parametrize(
    "lower_bound,upper_bound,expected",
    [
        (11, 22, 33),
        (95, 115, 99),
        (998, 1012, 1010),
        (1188511880, 1188511890, 1188511885),
        (222220, 222224, 222222),
        (1698522, 1698528, 0),
        (446443, 446449, 446446),
        (38593856, 38593862, 38593859),
        (565653, 565659, 0),
        (824824821, 824824827, 0),
        (2121212118, 21212121240, 0),
    ],
)
def test_sum_invalid_ids(lower_bound: int, upper_bound: int, expected: int):
    assert sum_invalid_ids(lower_bound, upper_bound) == expected


def test_year_2025_day_02_part_1_go():
    assert go(TEST_PATH) == 1227775554
