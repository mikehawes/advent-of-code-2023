from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass

from day20.pulse import SentPulse, Pulse, SendPulse


@dataclass
class Module(ABC):
    name: str
    inputs: list[str]
    outputs: list[str]

    @abstractmethod
    def receive(self, pulse: Pulse, from_module: str) -> list[SendPulse]:
        pass

    def count_state_toggles(self):
        return 0


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
        for presses in range(1, 10_000):
            for sent in self.press_button():
                if sent.pulse == pulse and sent.receiver == module:
                    return presses

    def count_possible_states(self):
        return 2 ** self.count_state_toggles()

    def count_state_toggles(self):
        return sum(map(lambda m: m.count_state_toggles(), self.module_by_name.values()))

    def sort_modules_with_root(self, root):
        root_module = self.module_by_name[root]
        modules = [root_module]
        queue = deque([root_module])
        module_found = {root: True}
        while queue:
            module = queue.pop()
            for input_name in module.inputs:
                if input_name in module_found:
                    continue
                module_found[input_name] = True
                input_module = self.module_by_name[input_name]
                modules.append(input_module)
                queue.appendleft(input_module)
        return modules
