from aoc.common.storage import get_data_path
from aoc.tasks.year_2022.day_08.part_2 import go


def test_year_2022_day_08_part_2_go():
    assert go(path=get_data_path(__file__, "test.txt")) == 8
