from aoc.common.storage import get_data_path
from aoc.tasks.year_2024.day_03.part_1 import go

TEST_PATH = get_data_path(__file__, "test.txt")


def test_year_2024_day_03_part_1_go():
    assert go(TEST_PATH) == 161
