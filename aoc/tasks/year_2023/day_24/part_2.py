from __future__ import annotations

import pathlib

import z3

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)
    x, y, z = z3.Reals("x y z")
    vx, vy, vz = z3.Reals("vx vy vz")

    solver = z3.Solver()

    for i, line in enumerate(lines[:3]):  # only need 3 lines here
        p, v = line.split(" @ ")
        h_x, h_y, h_z = map(float, p.split(", "))
        h_vx, h_vy, h_vz = map(float, v.split(", "))

        t = z3.Real(f"t{i}")
        solver.add(t >= 0.0)
        solver.add(x + vx * t == h_x + h_vx * t)
        solver.add(y + vy * t == h_y + h_vy * t)
        solver.add(z + vz * t == h_z + h_vz * t)

    assert solver.check() == z3.sat

    model = solver.model()

    solution = model[x].as_long() + model[y].as_long() + model[z].as_long()
    return solution
