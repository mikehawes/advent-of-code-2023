import io

from day12.springs import read_spring_conditions_from_file


def print_working_spring_arrangements_for_file(input_file):
    records = read_spring_conditions_from_file(input_file)
    output = io.StringIO()
    for record in records:
        print('{} {}'.format(record.springs, ','.join(map(str, record.damaged_counts))), file=output)
        damaged_areas = len(record.damaged_areas)
        print('{} arrangements'.format('?'), file=output)
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
