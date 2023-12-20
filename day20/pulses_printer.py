from day20.circuit import SentPulse, Pulse
from day20.modules import FlipFlopModule, ConjunctionModule


def print_sent(pulses: list[SentPulse]):
    return '\n'.join(map(
        lambda p: '{} -{}-> {}'.format(
            p.sender, print_pulse(p.pulse), p.receiver),
        pulses))


def print_button_presses(presses: list[list[SentPulse]]):
    return '\n\n'.join(map(print_sent, presses))


def print_pulse(pulse: Pulse):
    if pulse == Pulse.HIGH:
        return 'high'
    elif pulse == Pulse.LOW:
        return 'low'
    else:
        return '???'


def print_modules(modules, include_state=False):
    return '\n'.join(map(lambda m: print_module(m, include_state), modules))


def print_module(module, include_state=False):
    return '{} -> {} ->{}'.format(
        print_inputs(module, include_state),
        print_module_label(module, include_state),
        '' if not module.outputs else ' ' + ', '.join(module.outputs)
    )


def print_module_label(module, include_state=False):
    return '{}{}{}'.format(
        print_type(module),
        module.name,
        '' if not include_state else print_state(module)
    ).center(11)


def print_type(module):
    if isinstance(module, FlipFlopModule):
        return '%'
    elif isinstance(module, ConjunctionModule):
        return '&'
    else:
        return ''


def print_inputs(module, include_state=False):
    if include_state and isinstance(module, ConjunctionModule):
        inputs = map(lambda i: '{}:{}'.format(i, pulse_as_binary(module.last_pulse_by_input[i])),
                     module.inputs)
    else:
        inputs = module.inputs
    return ', '.join(inputs).rjust(42 if not include_state else 64)


def print_state(module):
    if isinstance(module, FlipFlopModule):
        return ':{}'.format(1 if module.on else 0)
    else:
        return ''


def print_last_pulse_by_input(item):
    input_name, pulse = item
    return '{}:{}'.format(input_name, 1 if pulse == Pulse.HIGH else 0)


def pulse_as_binary(pulse):
    return 1 if pulse == Pulse.HIGH else 0
