import re

initial_seeds = []
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
    ranges.append(list(map(int, map_range)))


def find_location_from(entry, entry_type):
    if entry_type not in next_type_by_type:
        return entry
    next_type = next_type_by_type[entry_type]
    map_ranges = map_ranges_by_name['{}-to-{}'.format(entry_type, next_type)]
    next_entry = entry
    for map_range in map_ranges:
        destination_start = map_range[0]
        source_start = map_range[1]
        range_length = map_range[2]
        range_index = entry - source_start
        if 0 <= range_index < range_length:
            next_entry = destination_start + range_index
    return find_location_from(next_entry, next_type)


def find_location(seed):
    return find_location_from(seed, 'seed')


def find_locations():
    return list(map(find_location, initial_seeds))


for line in get_input():
    if line.startswith('seeds: '):
        initial_seeds = list(map(int, re.findall('[0-9]+', line[len('seeds: '):])))
        print('Seeds: {}'.format(initial_seeds))
        continue
    map_match = re.match('(.+) map:', line)
    if map_match:
        current_map_name = map_match.group(1)
        add_map_name(current_map_name)
        continue
    numbers = re.findall('[0-9]+', line)
    if len(numbers) == 3:
        add_map_range(numbers)

print('Types: {}'.format(next_type_by_type))
print('Ranges: {}'.format(map_ranges_by_name))

locations = find_locations()
print('Locations: {}'.format(locations))
print('Lowest location: {}'.format(min(locations)))
