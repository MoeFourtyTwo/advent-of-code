from aoc.common.storage import get_data_path
from aoc.tasks.year_2024.day_22.part_2 import go

TEST_PATH = get_data_path(__file__, "test2.txt")


def test_year_2024_day_22_part_2_go():
    assert go(TEST_PATH) == 23
