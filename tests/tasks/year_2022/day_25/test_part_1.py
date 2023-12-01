import pytest

from aoc.common.storage import get_data_path
from aoc.tasks.year_2022.day_25.part_1 import convert_to_int, convert_to_snafu, go

TEST_PATH = get_data_path(__file__, "test.txt")


def test_year_2022_day_25_part_1_go():
    assert go(TEST_PATH) == "2=-1=0"


@pytest.mark.parametrize(
    "snafu, number",
    [
        ("1=-0-2", 1747),
        ("12111", 906),
        ("2=0=", 198),
        ("21", 11),
        ("2=01", 201),
        ("111", 31),
        ("20012", 1257),
        ("112", 32),
        ("1=-1=", 353),
        ("1-12", 107),
        ("12", 7),
        ("1=", 3),
        ("122", 37),
        ("1-", 4),
        ("1", 1),
    ],
)
def test_snafu_to_int(snafu: str, number: int):
    assert convert_to_int(snafu) == number


@pytest.mark.parametrize(
    "snafu, number",
    [
        ("1=-0-2", 1747),
        ("12111", 906),
        ("2=0=", 198),
        ("21", 11),
        ("2=01", 201),
        ("111", 31),
        ("20012", 1257),
        ("112", 32),
        ("1=-1=", 353),
        ("1-12", 107),
        ("12", 7),
        ("1=", 3),
        ("122", 37),
        ("1-", 4),
        ("1", 1),
    ],
)
def test_int_to_snafu(snafu: str, number: int):
    assert convert_to_snafu(number) == snafu
