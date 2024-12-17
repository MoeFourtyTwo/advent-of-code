from __future__ import annotations

import pathlib

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


@timeit
def go(path: pathlib.Path = DATA_PATH) -> int:
    lines = get_lines(path)

    program = list(map(int, lines[4][len("Program: ") :].split(",")))

    i = 1
    while True:
        registers = {"a": i, "b": int(lines[1][len("Register B: ") :]), "c": int(lines[2][len("Register C: ") :])}
        out_values = []

        instruction_pointer = 0
        while instruction_pointer < len(program):
            op, operand = program[instruction_pointer], program[instruction_pointer + 1]
            instruction_pointer, registers, out_value = op_map[op](instruction_pointer, registers, operand)
            if out_value is not None:
                out_values.append(out_value)

        if all(goal_value == out_value for goal_value, out_value in zip(reversed(program), reversed(out_values))):
            if len(program) == len(out_values):
                return i
            i *= 8
        else:
            i += 1


def get_combo_operand(registers: dict[str, int], op: int) -> int:
    match op:
        case literal if 0 <= literal <= 3:
            return literal
        case 4:
            return registers["a"]
        case 5:
            return registers["b"]
        case 6:
            return registers["c"]
        case 7:
            raise ValueError("Invalid op")


def adv(instruction_pointer: int, registers: dict[str, int], operand: int) -> tuple[int, dict[str, int], int | None]:
    combo_operand = get_combo_operand(registers, operand)
    registers["a"] = int(registers["a"] / 2**combo_operand)
    return instruction_pointer + 2, registers, None


def bxl(instruction_pointer: int, registers: dict[str, int], operand: int) -> tuple[int, dict[str, int], int | None]:
    registers["b"] = registers["b"] ^ operand

    return instruction_pointer + 2, registers, None


def bst(instruction_pointer: int, registers: dict[str, int], operand: int) -> tuple[int, dict[str, int], int | None]:
    combo_operand = get_combo_operand(registers, operand)
    registers["b"] = combo_operand % 8

    return instruction_pointer + 2, registers, None


def jnz(instruction_pointer: int, registers: dict[str, int], operand: int) -> tuple[int, dict[str, int], int | None]:
    if registers["a"] == 0:
        return instruction_pointer + 2, registers, None

    return operand, registers, None


def bxc(instruction_pointer: int, registers: dict[str, int], operand: int) -> tuple[int, dict[str, int], int | None]:
    registers["b"] = registers["b"] ^ registers["c"]
    return instruction_pointer + 2, registers, None


def out(instruction_pointer: int, registers: dict[str, int], operand: int) -> tuple[int, dict[str, int], int | None]:
    combo_operand = get_combo_operand(registers, operand)
    out_value = combo_operand % 8

    return instruction_pointer + 2, registers, out_value


def bdv(instruction_pointer: int, registers: dict[str, int], operand: int) -> tuple[int, dict[str, int], int | None]:
    combo_operand = get_combo_operand(registers, operand)
    registers["b"] = int(registers["a"] / 2**combo_operand)
    return instruction_pointer + 2, registers, None


def cdv(instruction_pointer: int, registers: dict[str, int], operand: int) -> tuple[int, dict[str, int], int | None]:
    combo_operand = get_combo_operand(registers, operand)
    registers["c"] = int(registers["a"] / 2**combo_operand)
    return instruction_pointer + 2, registers, None


op_map = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}
