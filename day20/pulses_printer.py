from day20.circuit import SentPulse, Pulse


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
