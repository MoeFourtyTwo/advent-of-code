import pathlib

import numpy as np

DATA_ROOT = pathlib.Path(__file__).parents[2] / "data"


def get_data_path(file: str, file_name: str = "input.txt") -> pathlib.Path:
    day = int(pathlib.Path(file).parent.name.split("_")[-1])

    return DATA_ROOT / f"day_{day:02d}" / file_name


def get_lines(path: pathlib.Path, strip: bool = True, rstrip: bool = False) -> list[str]:
    with open(path) as f:
        if strip:
            return list(map(str.strip, f.readlines()))
        if rstrip:
            return list(map(str.rstrip, f.readlines()))
        return f.readlines()


def get_as_array(path: pathlib.Path) -> np.ndarray:
    return np.genfromtxt(path, dtype=int, delimiter=1)
