import io

from day12.springs import read_spring_conditions_from_file


def print_working_spring_arrangements_for_file(input_file):
    records = read_spring_conditions_from_file(input_file)
    record_arrangements = list(map(lambda r: r.arrangements(), records))
    total_arrangements = sum(map(lambda a: len(a.arrangements), record_arrangements))
    output = io.StringIO()
    print('Total arrangements:', total_arrangements, file=output)
    print(file=output)
    for arrangements in record_arrangements:
        record = arrangements.record
        print('{} {}'.format(record.springs, ','.join(map(str, record.damaged_counts))), file=output)
        num_fillings = len(arrangements.fillings)
        num_arrangements = len(arrangements.arrangements)
        print('{} filling{}'.format(num_fillings, '' if num_fillings == 1 else 's'), file=output)
        print('{} arrangement{}:'.format(num_arrangements, '' if num_arrangements == 1 else 's'), file=output)
        for arrangement in arrangements.arrangements:
            print(arrangement, file=output)
        damaged_areas = len(record.damaged_areas)
        print('{} damaged area{}:'.format(damaged_areas, '' if damaged_areas == 1 else 's'), file=output)
        for area in record.damaged_areas:
            output.write('{}-{}: {} - length {}'.format(area.start, area.end, area.contents, area.length))
            if area.fully_known:
                print(', fully known', file=output)
            elif area.fully_unknown:
                print(', fully unknown', file=output)
            else:
                unknown_areas = len(area.unknown_areas)
                known_areas = len(area.known_damaged)
                if unknown_areas > 0:
                    output.write(', {} unknown area{}'.format(unknown_areas, '' if unknown_areas == 1 else 's'))
                if known_areas > 0:
                    output.write(', {} known area{}'.format(known_areas, '' if known_areas == 1 else 's'))
                print(file=output)
        print(file=output)
    return output.getvalue()
