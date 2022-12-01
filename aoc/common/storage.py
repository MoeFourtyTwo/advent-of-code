import pathlib

DATA_ROOT = pathlib.Path(__file__).parents[2] / "data"


def get_data_path(file: str) -> pathlib.Path:
    part = int(pathlib.Path(file).stem.split("_")[-1])
    day = int(pathlib.Path(file).parent.name.split("_")[-1])

    return DATA_ROOT / f"day_{day:02d}" / f"part_{part:1d}" / "input.txt"


def get_lines(path: pathlib.Path, strip: bool = True) -> list[str]:
    with open(path) as f:
        if strip:
            return list(map(str.strip, f.readlines()))
        return f.readlines()
