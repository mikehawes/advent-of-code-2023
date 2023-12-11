import re

from day06.race import count_winning_options


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
