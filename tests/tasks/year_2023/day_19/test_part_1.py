from aoc.common.storage import get_data_path
from aoc.tasks.year_2023.day_19.part_1 import go

TEST_PATH = get_data_path(__file__, "test.txt")


def test_year_2023_day_19_part_1_go():
    assert go(TEST_PATH) == 19114
