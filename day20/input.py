import re
from dataclasses import dataclass

from day20.circuit import Circuit
from day20.modules import FlipFlopModule, ConjunctionModule, BroadcastModule, OutputModule


def read_module_circuit_from_file(input_file) -> Circuit:
    with open(input_file, 'r') as file:
        specs = list(read_module_specs(file))
    return build_circuit(specs)


@dataclass
class ModuleSpec:
    module_type: str
    name: str
    outputs: list[str]


def read_module_specs(lines):
    return map(read_module_spec, lines)


def read_module_spec(line):
    match = re.match(r'([%&]?)([a-z]+) -> (([a-z]+, )*[a-z]+)', line)
    if not match:
        return None
    module_type = match.group(1)
    name = match.group(2)
    outputs = match.group(3).split(', ')
    return ModuleSpec(module_type, name, outputs)


def build_circuit(specs) -> Circuit:
    spec_by_name = {}
    inputs_by_name = {}
    for spec in specs:
        for output in spec.outputs:
            if output in inputs_by_name:
                inputs_by_name[output].append(spec.name)
            else:
                inputs_by_name[output] = [spec.name]
        spec_by_name[spec.name] = spec
    for name in inputs_by_name:
        if name not in spec_by_name:
            spec_by_name[name] = ModuleSpec('', name, [])
    module_by_name = {}
    for name, spec in spec_by_name.items():
        if name in inputs_by_name:
            inputs = inputs_by_name[name]
        else:
            inputs = []
        if spec.module_type == '%':
            module = FlipFlopModule(name, inputs, spec.outputs)
        elif spec.module_type == '&':
            module = ConjunctionModule(name, inputs, spec.outputs)
        elif spec.name == 'broadcaster':
            module = BroadcastModule(name, inputs, spec.outputs)
        else:
            module = OutputModule(name, inputs, [])
        module_by_name[name] = module
    return Circuit(module_by_name)
