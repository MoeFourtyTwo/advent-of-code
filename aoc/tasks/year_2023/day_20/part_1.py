from __future__ import annotations

import abc
import dataclasses
import enum
import pathlib
import typing

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


class Pulse(enum.Enum):
    LOW = enum.auto()
    HIGH = enum.auto()


@dataclasses.dataclass
class Stats:
    low_pulse_count: int = 0
    high_pulse_count: int = 0

    def register(self, pulse: Pulse, count: int = 1) -> None:
        match pulse:
            case Pulse.LOW:
                self.low_pulse_count += count
            case Pulse.HIGH:
                self.high_pulse_count += count

    def count(self) -> int:
        return self.low_pulse_count * self.high_pulse_count

    def __add__(self, other: Stats) -> Stats:
        return Stats(
            low_pulse_count=self.low_pulse_count + other.low_pulse_count,
            high_pulse_count=self.high_pulse_count + other.high_pulse_count,
        )


class Machine:
    def __init__(self) -> None:
        self.modules: dict[str:Module] = {}
        self.queue: list[tuple[str, str, Pulse]] = []
        self.stats: Stats = Stats()

    def __getitem__(self, item: str) -> Module:
        if item in self.modules:
            return self.modules[item]

        self[item] = NullModule(self, item)
        return self[item]

    def __setitem__(self, key: str, value: Module) -> None:
        self.modules[key] = value

    def push(self, destination: str, source: str, pulse: Pulse) -> None:
        self.queue.append((destination, source, pulse))

    def items(self) -> typing.ItemsView[str, Module]:
        return self.modules.items()

    def press_button(self) -> Stats:
        self["broadcaster"]("button", Pulse.LOW)
        self.stats.register(Pulse.LOW, 1)

        while self.queue:
            destination, source, pulse = self.queue.pop(0)
            self[destination](source, pulse)

        return self.stats

    @classmethod
    def parse(cls, lines: list[str]) -> Machine:
        to_wire = []

        machine = Machine()

        for line in lines:
            source, targets = line.split(" -> ")
            destinations = targets.split(", ")

            match source[0]:
                case "b":
                    machine[source] = BroadcasterModule(machine, source, destinations)
                case "%":
                    machine[source[1:]] = FlipFlopModule(machine, source[1:], destinations)
                case "&":
                    conjunction_module = ConjunctionModule(machine, source[1:], destinations)
                    machine[source[1:]] = conjunction_module
                    to_wire.append(conjunction_module.wire_inputs)

        for to_wire_call in to_wire:
            to_wire_call()

        return machine


class Module(abc.ABC):
    def __init__(self, machine: Machine, identifier: str, destinations: list[str]) -> None:
        self.machine = machine
        self.destinations = destinations
        self.identifier = identifier

    @abc.abstractmethod
    def __call__(self, source: str, pulse: Pulse) -> None:
        ...

    def send_pulse(self, pulse: Pulse) -> None:
        self.machine.stats.register(pulse, len(self.destinations))

        for destination in self.destinations:
            self.machine.push(destination, self.identifier, pulse)


class FlipFlopModule(Module):
    def __init__(self, machine: Machine, identifier: str, destinations: list[str]) -> None:
        super().__init__(machine, identifier, destinations)
        self.is_on = False

    def __call__(self, source: str, pulse: Pulse) -> None:
        if pulse == Pulse.HIGH:
            return

        self.is_on = not self.is_on

        self.send_pulse(Pulse.HIGH if self.is_on else Pulse.LOW)


class ConjunctionModule(Module):
    def __init__(self, machine: Machine, identifier: str, destinations: list[str]) -> None:
        super().__init__(machine, identifier, destinations)
        self.received_pulses = {}

    def wire_inputs(self) -> None:
        for name, module in self.machine.items():
            if self.identifier in module.destinations:
                self.received_pulses[name] = Pulse.LOW

    def __call__(self, source: str, pulse: Pulse) -> None:
        self.received_pulses[source] = pulse

        if all(received_pulse == Pulse.HIGH for received_pulse in self.received_pulses.values()):
            self.send_pulse(Pulse.LOW)
        else:
            self.send_pulse(Pulse.HIGH)


class BroadcasterModule(Module):
    def __init__(self, machine: Machine, identifier: str, destinations: list[str]) -> None:
        super().__init__(machine, identifier, destinations)

    def __call__(self, source: str, pulse: Pulse) -> None:
        self.send_pulse(pulse)


class NullModule(Module):
    def __init__(self, machine: Machine, identifier: str) -> None:
        super().__init__(machine, identifier, [])

    def __call__(self, source: str, pulse: Pulse) -> None:
        pass


@timeit
def go(path: pathlib.Path = DATA_PATH):
    lines = get_lines(path)

    machine = Machine.parse(lines)

    for _ in range(1000):
        machine.press_button()
    return machine.stats.count()
