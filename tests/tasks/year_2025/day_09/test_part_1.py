from aoc.common.storage import get_data_path
from aoc.tasks.year_2025.day_09.part_1 import go

TEST_PATH = get_data_path(__file__, "test.txt")


def test_year_2025_day_09_part_1_go():
    assert go(TEST_PATH) == 50
