import math
import re


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


def multiply_ways_to_beat(input_file):
    lines = open(input_file, 'r').readlines()
    times = list(map(int, re.findall('[0-9]+', lines[0])))
    record_distances = list(map(int, re.findall('[0-9]+', lines[1])))
    result = 1
    for race_index in range(0, len(times)):
        time = times[race_index]
        record_distance = record_distances[race_index]
        ways_to_beat = count_winning_options(time, record_distance)
        print("Ways to beat distance {} for time {}: {}".format(record_distance, time, ways_to_beat))
        result *= ways_to_beat
    return result
