import pytest

from aoc.common.storage import get_data_path
from aoc.tasks.day_09.part_1 import Head, Position, Tail, go

TEST_PATH = get_data_path(__file__, "test.txt")


def test_go():
    assert go(TEST_PATH) == 13


@pytest.mark.parametrize(
    "position_a, position_b, expected",
    [
        [Position(x=1, y=1), Position(x=1, y=1), True],
        [Position(x=1, y=3), Position(x=1, y=1), False],
        [Position(x=3, y=1), Position(x=1, y=1), False],
        [Position(x=1, y=1), Position(x=2, y=2), True],
    ],
)
def test_is_touching(position_a: Position, position_b: Position, expected: bool):
    assert position_a.is_touching(position_b) == expected
    assert position_b.is_touching(position_a) == expected


def test_clip():
    position = Position(2, -2)
    clipped = position.clip(-1, 1)
    assert clipped == Position(1, -1)


def test_wants_to_follow():
    head = Head()
    tail = Tail(head)

    head.position = Position(3, 3)

    assert tail.wants_to_follow == True


def test_step():
    head = Head()
    tail = Tail(head)
    head.position = Position(1, 3)
    tail.step()
    assert tail.position == Position(1, 1)
    tail.step()
    assert tail.position == Position(1, 2)
    head.position = Position(-1, 4)
    tail.step()
    assert tail.position == Position(0, 3)
