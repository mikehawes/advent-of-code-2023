from dataclasses import dataclass

from day20.circuit import Module
from day20.pulse import Pulse, SendPulse


@dataclass
class FlipFlopModule(Module):
    on: bool = False

    def receive(self, pulse: Pulse, from_module: str) -> list[SendPulse]:
        if pulse == Pulse.HIGH:
            return []
        if self.on:
            new_pulse = Pulse.LOW
        else:
            new_pulse = Pulse.HIGH
        self.on = not self.on
        return send_to_all_outputs(new_pulse, self.outputs)

    def count_state_toggles(self):
        return 1


@dataclass
class ConjunctionModule(Module):
    last_pulse_by_input: dict[str, Pulse] = None

    def __post_init__(self):
        self.last_pulse_by_input = {}
        for module in self.inputs:
            self.last_pulse_by_input[module] = Pulse.LOW

    def receive(self, pulse: Pulse, from_module: str) -> list[SendPulse]:
        self.last_pulse_by_input[from_module] = pulse
        if all(map(lambda p: p == Pulse.HIGH, self.last_pulse_by_input.values())):
            return send_to_all_outputs(Pulse.LOW, self.outputs)
        else:
            return send_to_all_outputs(Pulse.HIGH, self.outputs)

    def count_state_toggles(self):
        return len(self.inputs)


@dataclass
class BroadcastModule(Module):
    def receive(self, pulse: Pulse, from_module: str) -> list[SendPulse]:
        return send_to_all_outputs(pulse, self.outputs)


@dataclass
class OutputModule(Module):
    def receive(self, pulse: Pulse, from_module: str) -> list[SendPulse]:
        return []


def send_to_all_outputs(pulse: Pulse, outputs: list[str]) -> list[SendPulse]:
    return list(map(lambda module: SendPulse(module, pulse), outputs))
