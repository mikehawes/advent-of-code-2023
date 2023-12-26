import io
import math
from collections import defaultdict
from itertools import groupby


def describe_farm(farm, wrap):
    return 'Farm is {}x{} ({} tiles), {}'.format(
        farm.width, farm.height, farm.width * farm.height,
        'repeating infinitely' if wrap else 'fenced')


def print_reachable_counts(farm, steps_cases, wrap=False):
    out = io.StringIO()
    print(describe_farm(farm, wrap), file=out)
    print('Steps      Potential end tiles', file=out)
    for steps in steps_cases:
        print('{} {}'.format(str(steps).ljust(10), farm.count_possible_end_tiles(steps, wrap)), file=out)
    return out.getvalue()


def print_all_end_steps(farm, steps_cases, wrap=False):
    out = io.StringIO()
    print(describe_farm(farm, wrap), file=out)
    print(file=out)
    for steps in steps_cases:
        print(steps, 'steps:', file=out)
        possible_end_tiles = farm.find_possible_end_tiles(steps, wrap)
        tiles_sorted_by_y = list(sorted(possible_end_tiles, key=lambda loc: loc.y))
        tiles_sorted_by_x = list(sorted(possible_end_tiles, key=lambda loc: loc.x))
        first_y = tiles_sorted_by_y[0].y
        last_y = tiles_sorted_by_y[-1:][0].y
        first_x = tiles_sorted_by_x[0].x
        last_x = tiles_sorted_by_x[-1:][0].x
        maps_top = math.floor(first_y / farm.height)
        maps_bottom = math.ceil(last_y / farm.height)
        maps_left = math.floor(first_x / farm.width)
        maps_right = math.ceil(last_x / farm.width)
        x_values_by_y = {}
        reachable_by_map_pos = defaultdict(lambda: 0)
        for y, locations in groupby(tiles_sorted_by_y, lambda loc: loc.y):
            x_values_by_y[y] = dict(map(lambda loc: (loc.x, True), locations))
        for y in range(maps_top * farm.height, maps_bottom * farm.height):
            farm_y = y % farm.height
            maps_y = y // farm.height
            maps_y_even = maps_y % 2
            if y in x_values_by_y:
                x_values = x_values_by_y[y]
            else:
                x_values = {}
            for x in range(maps_left * farm.width, maps_right * farm.width):
                farm_x = x % farm.width
                maps_x = x // farm.width
                maps_x_even = maps_x % 2
                empty_tile = "'" if maps_x_even != maps_y_even else '.'
                if x in x_values:
                    reachable_by_map_pos[(maps_x, maps_y)] += 1
                    out.write('O')
                else:
                    tile = farm.lines[farm_y][farm_x]
                    if tile == '.':
                        tile = empty_tile
                    out.write(tile)
            print(file=out)
        print('Found reachable by map copy:', file=out)
        reachable_by_map = []
        for maps_y in range(maps_top, maps_bottom):
            reachable_by_map_x = []
            for maps_x in range(maps_left, maps_right):
                reachable_by_map_x.append(reachable_by_map_pos[(maps_x, maps_y)])
            reachable_by_map.append(reachable_by_map_x)
        print('\n'.join(map(lambda by_map_x: '|'.join(map(lambda count: str(count).center(4),
                                                          by_map_x)).rstrip(),
                            reachable_by_map)), file=out)
        print('Total reachable:', sum(map(sum, reachable_by_map)), file=out)
        print(file=out)
    return out.getvalue()
