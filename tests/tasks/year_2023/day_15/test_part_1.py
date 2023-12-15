from aoc.common.storage import get_data_path
from aoc.tasks.year_2023.day_15.part_1 import calc_hash, go

TEST_PATH = get_data_path(__file__, "test.txt")


def test_year_2023_day_15_part_1_go():
    assert go(TEST_PATH) == 1320


def test_calc_hash():
    assert calc_hash("HASH") == 52
