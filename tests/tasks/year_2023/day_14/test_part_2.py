from aoc.common.storage import get_data_path
from aoc.tasks.year_2023.day_14.part_2 import go

TEST_PATH = get_data_path(__file__, "test.txt")


def test_year_2023_day_14_part_2_go():
    assert go(TEST_PATH) == 64
