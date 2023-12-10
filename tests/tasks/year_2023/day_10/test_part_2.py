from aoc.common.storage import get_data_path
from aoc.tasks.year_2023.day_10.part_2 import go

TEST_PATH = get_data_path(__file__, "test_p2.txt")


def test_year_2023_day_10_part_2_go():
    assert go(TEST_PATH) == 8
