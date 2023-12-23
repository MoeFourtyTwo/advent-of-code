from __future__ import annotations

import pathlib

import networkx as nx

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    g = nx.DiGraph()

    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            match char:
                case "#":
                    continue
                case ".":
                    for row_offset, col_offset in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                        try:
                            neighbor = lines[row + row_offset][col + col_offset]
                        except IndexError:
                            continue

                        match neighbor, row_offset, col_offset:
                            case ".", _, _:
                                g.add_edge((row, col), (row + row_offset, col + col_offset))
                            case ">", 0, 1:
                                g.add_edge((row, col), (row + row_offset, col + col_offset))
                            case "<", 0, -1:
                                g.add_edge((row, col), (row + row_offset, col + col_offset))
                            case "v", 1, 0:
                                g.add_edge((row, col), (row + row_offset, col + col_offset))
                            case "^", -1, 0:
                                g.add_edge((row, col), (row + row_offset, col + col_offset))
                case ">":
                    g.add_edge((row, col), (row, col + 1))
                case "<":
                    g.add_edge((row, col), (row, col - 1))
                case "v":
                    g.add_edge((row, col), (row + 1, col))
                case "^":
                    g.add_edge((row, col), (row - 1, col))

    longest_path = max(nx.all_simple_paths(g, (0, 1), (len(lines) - 1, len(lines[-1]) - 2)), key=lambda x: len(x))
    return len(longest_path) - 1
