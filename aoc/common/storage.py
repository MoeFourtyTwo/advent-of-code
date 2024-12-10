import pathlib

import numpy as np
from aocd import get_data

DATA_ROOT = pathlib.Path(__file__).parents[2] / "data"


def get_data_path(file: str, file_name: str = "input.txt") -> pathlib.Path:
    year = int(pathlib.Path(file).parent.parent.name.split("_")[-1])
    day = int(pathlib.Path(file).parent.name.split("_")[-1])

    return DATA_ROOT / f"year_{year}" / f"day_{day:02d}" / file_name


def get_lines(path: pathlib.Path, strip: bool = True, rstrip: bool = False) -> list[str]:
    if path.name == "input.txt":
        day = int(path.parent.name.removeprefix("day_"))
        year = int(path.parent.parent.name.removeprefix("year_"))
        data = get_data(day=day, year=year).splitlines()
    else:
        with open(path) as f:
            data = f.readlines()
    if strip:
        return list(map(str.strip, data))
    if rstrip:
        return list(map(str.rstrip, data))
    return data


def get_as_array(path: pathlib.Path) -> np.ndarray:
    if path.name == "input.txt":
        day = int(path.parent.name.removeprefix("day_"))
        year = int(path.parent.parent.name.removeprefix("year_"))
        data = get_data(day=day, year=year).splitlines()
    else:
        data = path
    return np.genfromtxt(data, dtype=int, delimiter=1)
