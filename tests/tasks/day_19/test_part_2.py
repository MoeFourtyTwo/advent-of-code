from aoc.common.storage import get_data_path
from aoc.tasks.day_19.part_2 import Blueprint

TEST_PATH = get_data_path(__file__, "test.txt")


def test_blue_print_simulation():
    blueprint = Blueprint.parse(
        "Blueprint 1: "
        "Each ore robot costs 4 ore. "
        "Each clay robot costs 2 ore. "
        "Each obsidian robot costs 3 ore and 14 clay. "
        "Each geode robot costs 2 ore and 7 obsidian."
    )

    assert blueprint.simulate() == 56
