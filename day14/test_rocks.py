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

    def test_should_spin_cycle_twice_for_example(self):
        state = load_platform_state_from_file('example')
        spun = state.spin_cycles(2)
        verify(print_platform_state(spun))

    def test_should_spin_cycle_thrice_for_example(self):
        state = load_platform_state_from_file('example')
        spun = state.spin_cycles(3)
        verify(print_platform_state(spun))

    def test_should_spin_cycle_six_times_for_example(self):
        state = load_platform_state_from_file('example')
        spun = state.spin_cycles(6)
        verify(print_platform_state(spun))

    def test_should_spin_cycle_ten_times_for_example(self):
        state = load_platform_state_from_file('example')
        spun = state.spin_cycles(10)
        verify(print_platform_state(spun))

    def test_should_get_spin_cycle_repetition_for_example(self):
        state = load_platform_state_from_file('example')
        self.assertEqual((3, 10), state.get_spin_cycle_repeat())

    def test_example_spin_cycles_repeat_between_3_and_10(self):
        state = load_platform_state_from_file('example')
        self.assertEqual(
            print_platform_state(state.spin_cycles(3)),
            print_platform_state(state.spin_cycles(10)))

    def test_should_find_load_on_north_after_spins_for_example(self):
        state = load_platform_state_from_file('example')
        spun = state.spin_cycles_with_cache(1000000000)
        self.assertEqual(64, spun.total_load_on_north())

    def test_should_find_load_on_north_after_spins_for_input(self):
        state = load_platform_state_from_file('input')
        spun = state.spin_cycles_with_cache(1000000000)
        self.assertEqual(90176, spun.total_load_on_north())
