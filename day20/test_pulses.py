import unittest

from approvaltests import verify

from day20.circuit import Pulse
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

    def test_should_find_pulse_product_for_example_1(self):
        circuit = read_module_circuit_from_file('example1')
        self.assertEqual(32_000_000, circuit.find_pulse_product_for_presses(1000))

    def test_should_find_pulse_product_for_example_2(self):
        circuit = read_module_circuit_from_file('example2')
        self.assertEqual(11_687_500, circuit.find_pulse_product_for_presses(1000))

    def test_should_find_pulse_product_for_input(self):
        circuit = read_module_circuit_from_file('input')
        self.assertEqual(731_517_480, circuit.find_pulse_product_for_presses(1000))

    def test_should_find_presses_to_send_pulse_to_output_for_example_2(self):
        circuit = read_module_circuit_from_file('example2')
        circuit.press_button()
        self.assertEqual(2, circuit.find_presses_to_deliver(Pulse.LOW, 'output'))

    def test_should_find_presses_to_send_pulse_to_rx(self):
        circuit = read_module_circuit_from_file('input')
        self.assertEqual(0, circuit.find_presses_to_deliver(Pulse.LOW, 'rx'))

    def test_should_count_possible_states_for_input(self):
        circuit = read_module_circuit_from_file('input')
        self.assertEqual(2_128_896, circuit.count_possible_states())
