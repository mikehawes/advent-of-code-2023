import unittest

from approvaltests import verify

from day20.input import read_module_circuit_from_file
from day20.pulses_printer import print_sent, print_button_presses


class TestPulses(unittest.TestCase):

    def test_should_find_pulses_for_example_1(self):
        circuit = read_module_circuit_from_file('example1')
        verify(print_sent(circuit.press_button()))

    def test_should_find_pulses_for_example_2(self):
        circuit = read_module_circuit_from_file('example2')
        verify(print_button_presses([
            circuit.press_button(),
            circuit.press_button(),
            circuit.press_button(),
            circuit.press_button()]))
