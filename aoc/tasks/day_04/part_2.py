from __future__ import annotations

import dataclasses

from loguru import logger

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@dataclasses.dataclass
class Assignment:
    from_inclusive: int
    to_inclusive: int

    @classmethod
    def parse(cls, line: str) -> tuple[Assignment, Assignment]:
        left, right = line.split(",")

        return cls._parse_single(left), cls._parse_single(right)

    @classmethod
    def _parse_single(cls, segment: str) -> Assignment:
        from_inclusive, to_inclusive = segment.split("-")
        return cls(from_inclusive=int(from_inclusive), to_inclusive=int(to_inclusive))

    def __contains__(self, item: Assignment) -> bool:
        return self.from_inclusive <= item.from_inclusive and self.to_inclusive >= item.to_inclusive

    def overlap(self, other: Assignment) -> bool:
        return (
            other.from_inclusive <= self.to_inclusive <= other.to_inclusive
            or self.from_inclusive <= other.to_inclusive <= self.to_inclusive
        )


@timeit
def go():
    lines = get_lines(DATA_PATH)

    total = sum(left.overlap(right) for left, right in [Assignment.parse(line) for line in lines])

    logger.info(f"{total=}")
