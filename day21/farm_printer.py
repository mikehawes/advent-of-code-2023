import io


def print_reachable_counts(farm, steps_cases, wrap=False):
    out = io.StringIO()
    print('Farm is {}x{} ({} tiles), {}'.format(
        farm.width, farm.height, farm.width * farm.height,
        'repeating infinitely' if wrap else 'fenced'),
        file=out)
    print('Steps      Potential end tiles', file=out)
    for steps in steps_cases:
        print('{} {}'.format(str(steps).ljust(10), farm.count_tiles_reachable(steps, wrap)), file=out)
    return out.getvalue()
