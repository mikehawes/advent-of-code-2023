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


def print_modules(modules):
    return '\n'.join(map(print_module, modules))


def print_module(module):
    return '{} -> {} ->{}'.format(
        ', '.join(module.inputs).rjust(42),
        '{}{}'.format(print_type(module), module.name).center(11),
        '' if not module.outputs else ' ' + ', '.join(module.outputs)
    )


def print_type(module):
    if isinstance(module, FlipFlopModule):
        return '%'
    elif isinstance(module, ConjunctionModule):
        return '&'
    else:
        return ''
