import datetime
import importlib
import pathlib
import shutil

import fire
from loguru import logger

from aoc.common.storage import DATA_ROOT

_TASK_ROOT = pathlib.Path(__file__).parent / "tasks"
_TEMPLATE_PATH = _TASK_ROOT / "_template_day"


def _parse_task(day, part):
    if day <= 0:
        day = datetime.datetime.now().day
        logger.info(f"Defaulting to {day=}")

    if part not in (1, 2):
        part = 1
        logger.info(f"Defaulting to {part=}")

    return day, part


def run(day: int = -1, part: int = -1) -> None:
    day, part = _parse_task(day, part)
    try:
        mod = importlib.import_module(f"aoc.tasks.day_{day:02d}.part_{part}")
        mod.go()
    except ImportError as e:
        logger.error(f"Received import error: {e}. Did you run generate?")


def generate(day: int = -1) -> None:
    day, _ = _parse_task(day, 1)

    try:
        shutil.copytree(_TEMPLATE_PATH, _TASK_ROOT / f"day_{day:02d}")
    except FileExistsError:
        logger.warning("Already created Python code.")

    for part in (1, 2):
        path = DATA_ROOT / f"day_{day:02d}" / f"part_{part}"
        path.mkdir(parents=True)
        with open(path / "input.txt", "w+"):
            pass


def main():
    fire.Fire({"run": run, "generate": generate})


if __name__ == "__main__":
    main()
