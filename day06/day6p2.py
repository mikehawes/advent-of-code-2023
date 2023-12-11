import re

from day06.race import count_winning_options


def ways_to_beat_multiplied_race(input_file):
    lines = open(input_file, 'r').readlines()
    record_time = ''
    record_distance = ''
    for time in re.findall('[0-9]+', lines[0]):
        record_time += time
    for distance in re.findall('[0-9]+', lines[1]):
        record_distance += distance
    record_time = int(record_time)
    record_distance = int(record_distance)

    ways_to_beat = count_winning_options(record_time, record_distance)
    print("Ways to beat distance {} for time {}: {}".format(record_distance, record_time, ways_to_beat))
    return ways_to_beat
