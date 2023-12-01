from aoc.common.storage import get_data_path
from aoc.tasks.year_2022.day_10.part_2 import go

TEST_PATH = get_data_path(__file__, "test.txt")


def test_year_2022_day_10_part_2_go():
    go(TEST_PATH)
