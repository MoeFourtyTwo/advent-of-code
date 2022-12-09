from aoc.common.storage import get_data_path
from aoc.tasks.day_08.part_1 import go

TEST_PATH = get_data_path(__file__, "test.txt")


def test_go():
    assert go(path=TEST_PATH) == 21
