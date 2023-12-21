import unittest

from approvaltests import verify

from day20.circuit import Pulse
from day20.input import read_module_circuit_from_file
from day20.pulses_printer import print_sent, print_button_presses, print_modules, print_circuits_by_root


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

    @unittest.skip('Not working')
    def test_should_find_presses_to_send_pulse_to_rx(self):
        circuit = read_module_circuit_from_file('input')
        self.assertEqual(0, circuit.find_presses_to_deliver(Pulse.LOW, 'rx'))

    def test_should_count_possible_states_for_example2(self):
        circuit = read_module_circuit_from_file('example2')
        self.assertEqual(32, circuit.count_possible_states())

    def test_should_count_possible_states_for_input(self):
        circuit = read_module_circuit_from_file('input')
        self.assertEqual(2_475_880_078_570_760_549_798_248_448, circuit.count_possible_states())

    def test_should_count_state_toggles_for_input(self):
        circuit = read_module_circuit_from_file('input')
        self.assertEqual(91, circuit.count_state_toggles())

    def test_should_sort_input_rx_first(self):
        circuit = read_module_circuit_from_file('input')
        verify(print_modules(circuit.sort_modules_with_root('rx')))

    def test_should_print_state_after_1_button_press(self):
        circuit = read_module_circuit_from_file('input')
        circuit.press_button()
        verify(print_modules(circuit.sort_modules_with_root('rx'), include_state=True))

    def test_should_print_state_after_1000_button_presses(self):
        circuit = read_module_circuit_from_file('input')
        circuit.press_button_times(1000)
        verify(print_modules(circuit.sort_modules_with_root('rx'), include_state=True))

    def test_should_split_to_sub_graphs(self):
        circuit = read_module_circuit_from_file('input')
        circuits = circuit.split_by_output_at_module('broadcaster')
        verify(print_circuits_by_root(circuits, 'rx'))

    def test_should_find_presses_by_sub_graphs(self):
        circuit = read_module_circuit_from_file('input')
        self.assertEqual(244_178_746_156_661, circuit.by_split_find_presses_to_deliver('broadcaster', Pulse.LOW, 'rx'))

    def test_should_count_possible_states_for_sub_graphs(self):
        circuit = read_module_circuit_from_file('input')
        circuits = circuit.split_by_output_at_module('broadcaster')
        self.assertEqual([33_554_432, 8_388_608, 2_097_152, 4_194_304],
                         list(map(lambda c: c.count_possible_states(), circuits)))

    def test_should_find_presses_by_sub_graph(self):
        circuit = read_module_circuit_from_file('input')
        circuits = circuit.split_by_output_at_module('broadcaster')
        self.assertEqual([4079, 3931, 3761, 4049], list(map(
            lambda c: c.find_presses_to_deliver(Pulse.LOW, 'rx', max_presses=1_000_000),
            circuits)))
