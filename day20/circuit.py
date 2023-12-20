from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto


class Pulse(Enum):
    LOW = auto()
    HIGH = auto()


@dataclass(frozen=True)
class SendPulse:
    module: str
    pulse: Pulse


@dataclass(frozen=True)
class SentPulse:
    sender: str
    receiver: str
    pulse: Pulse


class Module(ABC):
    @abstractmethod
    def receive(self, pulse: Pulse, from_module: str) -> list[SendPulse]:
        pass

    def set_inputs(self, inputs: list[str]):
        pass


@dataclass(frozen=True)
class Circuit:
    module_by_name: dict[str, Module]

    def press_button(self):
        pulses = [SentPulse('button', 'broadcaster', Pulse.LOW)]
        sent = []
        while pulses:
            sent += pulses
            next_pulses = []
            for pulse in pulses:
                next_pulses += self.next_sent_pulses(pulse)
            pulses = next_pulses
        return sent

    def find_pulse_product_for_presses(self, presses):
        total_low = 0
        total_high = 0
        for i in range(0, presses):
            for sent in self.press_button():
                if sent.pulse == Pulse.LOW:
                    total_low += 1
                else:
                    total_high += 1
        return total_low * total_high

    def next_sent_pulses(self, pulse: SentPulse):
        receiver = self.module_by_name[pulse.receiver]
        send_pulses = receiver.receive(pulse.pulse, pulse.sender)
        return list(map(lambda send: SentPulse(pulse.receiver, send.module, send.pulse), send_pulses))

    def find_presses_to_deliver(self, pulse: Pulse, module: str):
        for presses in range(1, 3_000_000):
            for sent in self.press_button():
                if sent.pulse == pulse and sent.receiver == module:
                    return presses
