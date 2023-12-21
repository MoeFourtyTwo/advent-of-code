from __future__ import annotations

import pathlib

import numpy as np
import numpy.typing as npt

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


class RepeatingList(list):
    def __getitem__(self, index):
        if index >= len(self):
            return self[(index - len(self)) % 2 - 2]
        return super().__getitem__(index)


def solve(data: npt.NDArray[int, int], start_col: int, start_row: int) -> RepeatingList[int]:
    padded_data = np.pad(data, 1, constant_values=1)
    w = data.shape[0]
    start_col += 1
    start_row += 1
    visited = {(start_row, start_col)}
    reachable_even_step = {(start_row, start_col)}
    reachable_odd_step = set()
    border = {(start_row, start_col)}

    results = RepeatingList([0, 1])

    for i in range(1, 2 * w - 1):
        possible_locations = set(
            (new_row, new_col)
            for row, col in border
            for row_offset, col_offset in ((-1, 0), (1, 0), (0, -1), (0, 1))
            if padded_data[new_row := row + row_offset][new_col := col + col_offset] != 1
            and (new_row, new_col) not in visited
        )
        if i % 2 == 0:
            reachable_even_step.update(possible_locations)
            results.append(len(reachable_even_step))
        else:
            reachable_odd_step.update(possible_locations)
            results.append(len(reachable_odd_step))

        visited.update(possible_locations)
        border = possible_locations

    return results


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)
    total_steps = 26501365

    data = np.array([list(line.replace(".", "0").replace("#", "1").replace("S", "2")) for line in lines], dtype=int)

    w = data.shape[0]
    n = (total_steps - (w // 2)) // w

    step_diag = total_steps % w
    step_side = (total_steps - w // 2) % w

    center = solve(data, w // 2, w // 2)

    odd_filled = (n - 1) ** 2 * center[total_steps + 1 + n % 2]
    even_filled = n**2 * center[total_steps + 2 + n % 2]

    diag_from_t_l = solve(data, 0, 0)
    value_diag_from_t_l = n * diag_from_t_l[step_diag] + (n - 1) * diag_from_t_l[w + step_diag]

    diag_from_b_l = solve(data, w - 1, 0)
    value_diag_from_b_l = n * diag_from_b_l[step_diag] + (n - 1) * diag_from_b_l[w + step_diag]

    diag_from_t_r = solve(data, 0, w - 1)
    value_diag_from_t_r = n * diag_from_t_r[step_diag] + (n - 1) * diag_from_t_r[w + step_diag]

    diag_from_b_r = solve(data, w - 1, w - 1)
    value_diag_from_b_r = n * diag_from_b_r[step_diag] + (n - 1) * diag_from_b_r[w + step_diag]

    side_from_l = solve(data, w // 2, 0)
    value_side_from_l = side_from_l[step_side] + side_from_l[w + step_side]

    side_from_t = solve(data, 0, w // 2)
    value_side_from_t = side_from_t[step_side] + side_from_t[w + step_side]

    side_from_b = solve(data, w // 2, w - 1)
    value_side_from_b = side_from_b[step_side] + side_from_b[w + step_side]

    side_from_r = solve(data, w - 1, w // 2)
    value_side_from_r = side_from_r[step_side] + side_from_r[w + step_side]

    total = (
        even_filled
        + odd_filled
        + value_diag_from_t_l
        + value_diag_from_b_l
        + value_diag_from_t_r
        + value_diag_from_b_r
        + value_side_from_l
        + value_side_from_t
        + value_side_from_b
        + value_side_from_r
    )

    return total


if __name__ == "__main__":
    go()
