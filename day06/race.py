import math


def get_button_press_times(time, distance):
    plus_or_minus = math.sqrt(time * time - 4 * distance)
    first_option = (time - plus_or_minus) / 2
    second_option = (time + plus_or_minus) / 2
    return [first_option, second_option]


def count_winning_options(time, distance):
    winning_range = get_button_press_times(time, distance)
    print("Winning range for distance {}, time {}: {}".format(distance, time, winning_range))
    winning_a = winning_range[0]
    start = int(winning_a)
    if start == winning_a:
        start += 1
    winning_b = winning_range[1]
    end = int(winning_b)
    return end - start
