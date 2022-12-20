from aoc.common.storage import get_data_path
from aoc.tasks.day_19.part_1 import Blueprint, go

TEST_PATH = get_data_path(__file__, "test.txt")


def test_day_19_part_1_go():
    assert go(TEST_PATH) == 33


def test_blue_print_simulation():
    blueprint = Blueprint.parse(
        "Blueprint 1: "
        "Each ore robot costs 4 ore. "
        "Each clay robot costs 2 ore. "
        "Each obsidian robot costs 3 ore and 14 clay. "
        "Each geode robot costs 2 ore and 7 obsidian."
    )

    best_state = blueprint.simulate()

    assert best_state.geode_count == 9


def test_blue_print_2_simulation():
    blueprint = Blueprint.parse(
        "Blueprint 1: "
        "Each ore robot costs 2 ore. "
        "Each clay robot costs 3 ore. "
        "Each obsidian robot costs 3 ore and 8 clay. "
        "Each geode robot costs 3 ore and 12 obsidian."
    )

    best_state = blueprint.simulate()

    assert best_state.geode_count == 12
