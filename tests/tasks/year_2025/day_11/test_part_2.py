from aoc.common.storage import get_data_path
from aoc.tasks.year_2025.day_11.part_2 import go

TEST_PATH = get_data_path(__file__, "test_part2.txt")


def test_year_2025_day_11_part_2_go():
    assert go(TEST_PATH) == 2
