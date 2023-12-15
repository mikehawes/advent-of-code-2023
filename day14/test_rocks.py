import unittest

from approvaltests import verify

from day14.rocks import total_load_on_north_from_file, load_platform_state_from_file, print_platform_state


class TestRocks(unittest.TestCase):

    def test_should_tilt_to_north_for_example(self):
        state = load_platform_state_from_file('example')
        tilted = state.tilt_north()
        verify(print_platform_state(tilted))

    def test_should_find_load_on_north_for_example(self):
        self.assertEqual(136, total_load_on_north_from_file('example'))

    def test_should_find_load_on_north_for_input(self):
        self.assertEqual(109661, total_load_on_north_from_file('input'))

    def test_should_spin_cycle_for_example(self):
        state = load_platform_state_from_file('example')
        spun = state.spin_cycle()
        verify(print_platform_state(spun))
