from __future__ import annotations

import abc
import enum
import math
import pathlib
import typing

from tqdm import tqdm

from aoc.common.decorators import timeit
from aoc.common.storage import get_data_path, get_lines

DATA_PATH = get_data_path(__file__)


class Pulse(enum.Enum):
    LOW = enum.auto()
    HIGH = enum.auto()


class FoundError(Exception):
    pass


class Machine:
    def __init__(self) -> None:
        self.modules: dict[str:Module] = {}
        self.queue: list[tuple[str, str, Pulse]] = []

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

    def press_button(
        self,
        button_press_count: int,
        found: dict[str, int],
        watched_sources: list[str],
        watched_target: str,
        watched_pulse: Pulse,
    ) -> None:
        self["broadcaster"]("button", Pulse.LOW)

        while self.queue:
            destination, source, pulse = self.queue.pop(0)

            if (
                destination == watched_target
                and source in watched_sources
                and pulse == watched_pulse
                and destination not in found
            ):
                found[source] = button_press_count

                if len(found) == len(watched_sources):
                    raise FoundError()

            self[destination](source, pulse)

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
    def __call__(self, source: str, pulse: Pulse) -> None: ...

    def send_pulse(self, pulse: Pulse) -> None:
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
            if self.identifier == "fk":
                pass
            self.send_pulse(Pulse.LOW)
        else:
            if self.identifier == "mm":
                pass
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

    total_presses = 0
    found = {}

    with tqdm() as pbar:
        while True:
            total_presses += 1
            pbar.update(1)
            try:
                machine.press_button(total_presses, found, ["lh", "fk", "ff", "mm"], "nr", Pulse.HIGH)
            except FoundError:
                break
    return math.lcm(*found.values())


if __name__ == "__main__":
    go()
