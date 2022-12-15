from aoc.common.storage import get_data_path
from aoc.tasks.day_15.part_2 import Point, Sensor, go

TEST_PATH = get_data_path(__file__, "test.txt")


def test_day_15_part_2_go():
    assert go(TEST_PATH, max_value=20) == 56000011


def test_iterate_over_edge():
    sensor = Sensor(center=Point(x=0, y=0), beacon=Point(x=0, y=2))

    s = set(sensor.iterate_over_edge())
    assert len(s) == (1 + sensor.radius) * 4
