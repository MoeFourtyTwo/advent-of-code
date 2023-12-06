import datetime
import importlib
import pathlib
import shutil
from string import Template

import fire
from loguru import logger

from aoc.common.storage import DATA_ROOT

_TASK_ROOT = pathlib.Path(__file__).parent / "tasks"
_TEST_TASK_ROOT = pathlib.Path(__file__).parent.parent / "tests" / "tasks"
_TEMPLATE_PATH = _TASK_ROOT / "_template_day"
_TEST_TEMPLATE_PATH = _TEST_TASK_ROOT / "_template_day" / "test_template.txt"


def _parse_task(year, day, part):
    if not isinstance(year, int) or year <= 0:
        year = datetime.datetime.now().year
        logger.info(f"Defaulting to {year=}")

    if not isinstance(day, int) or day <= 0:
        day = datetime.datetime.now().day
        logger.info(f"Defaulting to {day=}")

    if part not in (1, 2):
        if _TASK_ROOT.joinpath(f"year_{year}").joinpath(f"day_{day:02d}").joinpath(f"part_2.py").exists():
            part = 2
        elif _TASK_ROOT.joinpath(f"year_{year}").joinpath(f"day_{day:02d}").joinpath(f"part_1.py").exists():
            part = 1
        else:
            part = -1
        logger.info(f"Defaulting to {part=}")

    return year, day, part


def run(year: int = -1, day: int = -1, part: int = -1) -> None:
    year, day, part = _parse_task(year, day, part)
    try:
        mod = importlib.import_module(f"aoc.tasks.year_{year}.day_{day:02d}.part_{part}")
        output = mod.go()
        logger.info(f"{output = }")
    except ImportError as e:
        logger.error(f"Received import error: {e}. Did you run generate?")


def generate(year: int = -1, day: int = -1, part: int = -1) -> None:
    year, day, part = _parse_task(year, day, part)

    with open(_TEST_TEMPLATE_PATH) as f:
        src = Template(f.read())
        result = src.substitute(
            {"year": f"year_{year}", "day": f"day_{day:02d}", "part": f"part_{ 1 if part < 1 else 2}"}
        )
    test_file_path = _TEST_TASK_ROOT / f"year_{year}" / f"day_{day:02d}" / f"test_part_{ 1 if part < 1 else 2}.py"

    test_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(test_file_path, "w+") as f:
        f.write(result)

    if part < 1:
        try:
            shutil.copytree(_TEMPLATE_PATH, _TASK_ROOT / f"year_{year}" / f"day_{day:02d}")
        except FileExistsError:
            logger.warning("Already created Python code.")

        path = DATA_ROOT / f"year_{year}" / f"day_{day:02d}"
        path.mkdir(parents=True, exist_ok=True)
        with open(path / "input.txt", "w+"):
            pass
        with open(path / "test.txt", "w+"):
            pass
    elif part == 1:
        try:
            shutil.copy(
                _TASK_ROOT / f"year_{year}" / f"day_{day:02d}" / f"part_1.py",
                _TASK_ROOT / f"year_{year}" / f"day_{day:02d}" / f"part_2.py",
            )
        except FileExistsError:
            logger.warning("Already created Python code.")


def main():
    fire.Fire({"run": run, "generate": generate})


if __name__ == "__main__":
    main()
