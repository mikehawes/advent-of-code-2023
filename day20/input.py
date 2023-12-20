import re

from day20.circuit import Circuit
from day20.modules import FlipFlopModule, ConjunctionModule, BroadcastModule, OutputModule


def read_module_circuit_from_file(input_file) -> Circuit:
    module_by_name = {}
    inputs_by_name = {}
    with open(input_file, 'r') as file:
        for line in file:
            match = re.match(r'([%&]?)([a-z]+) -> (([a-z]+, )*[a-z]+)', line)
            if match:
                module_type = match.group(1)
                name = match.group(2)
                outputs = match.group(3).split(', ')
                if module_type == '%':
                    module = FlipFlopModule(outputs)
                elif module_type == '&':
                    module = ConjunctionModule(outputs)
                elif name == 'broadcaster':
                    module = BroadcastModule(outputs)
                else:
                    raise Exception('Unrecognised module: {}'.format(name))
                for output in outputs:
                    if output in inputs_by_name:
                        inputs_by_name[output].append(name)
                    else:
                        inputs_by_name[output] = [name]
                module_by_name[name] = module
    for name, module in module_by_name.items():
        if name in inputs_by_name:
            module.set_inputs(inputs_by_name[name])
        else:
            module.set_inputs([])
    for name in inputs_by_name:
        if name not in module_by_name:
            module_by_name[name] = OutputModule()
    return Circuit(module_by_name)
