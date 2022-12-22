from aoc.common.storage import get_data_path
from aoc.tasks.day_22.part_1 import go

TEST_PATH = get_data_path(__file__, "test.txt")


def test_day_22_part_1_go():
    assert go(TEST_PATH) == 6032
