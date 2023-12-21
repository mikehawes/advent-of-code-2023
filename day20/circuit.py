from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, replace
from math import lcm

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

    def split_by_outputs(self):
        return list(map(lambda output: replace(self, outputs=[output]),
                        self.outputs))

    def filter_inputs(self, modules_by_name):
        return replace(self, inputs=list(filter(lambda name: name in modules_by_name,
                                                self.inputs)))


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

    def press_button_times(self, presses):
        for i in range(0, presses):
            self.press_button()

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

    def find_presses_to_deliver(self, pulse: Pulse, module: str, max_presses=10_000):
        for presses in range(1, max_presses):
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

    def split_by_output_at_module(self, module_name):
        circuits = []
        for module in self.module_by_name[module_name].split_by_outputs():
            reachable_by_name = {}
            self.add_reachable(module, reachable_by_name)
            module_by_name = {}
            for reachable in reachable_by_name.values():
                module_by_name[reachable.name] = reachable.filter_inputs(reachable_by_name)
            circuits.append(Circuit(module_by_name))
        return circuits

    def add_reachable(self, module, module_by_name):
        if module.name in module_by_name:
            return
        module_by_name[module.name] = module
        for output_name in module.outputs:
            output = self.module_by_name[output_name]
            self.add_reachable(output, module_by_name)

    def by_split_find_presses_to_deliver(self, split_at: str, pulse: Pulse, target: str, max_subgraph_presses=10_000):
        circuits = self.split_by_output_at_module(split_at)
        presses = list(map(lambda c: c.find_presses_to_deliver(pulse, target, max_presses=max_subgraph_presses),
                           circuits))
        a = presses[0]
        b = presses[1]
        multiple = lcm(a, b)
        for other in presses[2:]:
            multiple = lcm(multiple, other)
        return multiple
