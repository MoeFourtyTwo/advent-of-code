from aoc.common.storage import get_data_path
from aoc.tasks.day_09.part_2 import go


def test_go():
    assert go(get_data_path(__file__, "test.txt")) == 1


def test_go():
    assert go(get_data_path(__file__, "test_large.txt")) == 36
