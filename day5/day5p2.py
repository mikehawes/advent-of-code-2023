import re

from day5.entry_ranges import EntryRange, RangeMapping, RangeMappings

initial_seed_ranges = []
next_type_by_type = {}
map_ranges_by_name = {}
current_map_name = None


def get_input():
    return open('input', 'r')


def add_map_name(map_name):
    map_to_from = re.match('(.+)-to-(.+)', map_name)
    from_type = map_to_from.group(1)
    to_type = map_to_from.group(2)
    next_type_by_type[from_type] = to_type


def add_map_range(map_range):
    if current_map_name in map_ranges_by_name:
        ranges = map_ranges_by_name[current_map_name]
    else:
        ranges = []
        map_ranges_by_name[current_map_name] = ranges
    ranges.append(map_range)


def find_location_from(entry_ranges, entry_type):
    print('Found {} ranges: {}'.format(entry_type, entry_ranges))
    if entry_type not in next_type_by_type:
        return entry_ranges
    next_type = next_type_by_type[entry_type]
    map_ranges = map_ranges_by_name['{}-to-{}'.format(entry_type, next_type)]
    next_entry_ranges = RangeMappings(map_ranges).map(entry_ranges)
    return find_location_from(next_entry_ranges, next_type)


def get_seeds_in_range(seed_range):
    range_start = seed_range[0]
    range_length = seed_range[1]
    return range(range_start, range_start + range_length)


for line in get_input():
    if line.startswith('seeds: '):
        seed_ranges_raw = list(map(int, re.findall('[0-9]+', line[len('seeds: '):])))
        for i in range(0, len(seed_ranges_raw), 2):
            initial_seed_ranges.append(EntryRange(start=seed_ranges_raw[i], length=seed_ranges_raw[i + 1]))
        print('Seeds: {}'.format(initial_seed_ranges))
        continue
    map_match = re.match('(.+) map:', line)
    if map_match:
        current_map_name = map_match.group(1)
        add_map_name(current_map_name)
        continue
    numbers = list(map(int, re.findall('[0-9]+', line)))
    if len(numbers) == 3:
        add_map_range(RangeMapping(numbers[0], numbers[1], numbers[2]))

print('Types: {}'.format(next_type_by_type))
print('Ranges:')
for map_ranges_name in map_ranges_by_name:
    print('{}: {}'.format(map_ranges_name, map_ranges_by_name[map_ranges_name]))
print('Initial seed ranges: {}'.format(initial_seed_ranges))

location_ranges = []
min_location = None
for location_range in find_location_from(initial_seed_ranges, 'seed'):
    location_ranges.append(location_range)
    if min_location:
        min_location = min(location_range.start, min_location)
    else:
        min_location = location_range.start

print('Locations:', location_ranges)
print('Min location:', min_location)
