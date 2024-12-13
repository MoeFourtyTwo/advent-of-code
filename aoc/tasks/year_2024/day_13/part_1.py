from __future__ import annotations

import pathlib

import z3

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    total_cost = 0

    for i in range(0, len(lines), 4):
        block = lines[i : i + 4]

        ax, ay = map(int, block[0][len("Button A: X+") :].split(", Y+"))
        bx, by = map(int, block[1][len("Button B: X+") :].split(", Y+"))
        tx, ty = map(int, block[2][len("Prize: X=") :].split(", Y="))

        total_cost += solve(ax, bx, ay, by, tx, ty)

    return total_cost


def solve(ax: int, bx: int, ay: int, by: int, tx: int, ty: int) -> int:
    solver = z3.Optimize()

    a = z3.Int("a")
    b = z3.Int("b")
    cost = z3.Int("cost")

    solver.add(a * ax + b * bx == tx)
    solver.add(a * ay + b * by == ty)
    solver.add(a >= 0)
    solver.add(b >= 0)
    solver.add(cost == a * 3 + b * 1)
    # solver.minimize(cost)

    if solver.check() == z3.unsat:
        return 0

    model = solver.model()
    return model[cost].as_long()
