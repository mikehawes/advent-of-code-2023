import io

from day12.springs import total_spring_arrangements, \
    read_spring_conditions_from_file, compute_spring_arrangements_from_records


def print_damaged_counts(record):
    return ','.join(map(str, record.damaged_counts))


def print_record(record):
    return '{} {}'.format(record.springs, print_damaged_counts(record))


def list_of_record_and_arrangement_count(records, multiple=1):
    return list(map(lambda r: [print_record(r), r.count_arrangements(multiple=multiple)], records))


def print_working_spring_arrangements_for_file(input_file, multiple=1):
    records = read_spring_conditions_from_file(input_file)
    return print_working_spring_arrangements_for_records(records, multiple)


def print_working_spring_arrangements_for_records(records, multiple=1):
    record_arrangements = compute_spring_arrangements_from_records(records, multiple=multiple)
    total_arrangements = total_spring_arrangements(record_arrangements)
    output = io.StringIO()
    print('Total arrangements:', total_arrangements, file=output)
    if multiple > 1:
        print('Multiplied by', multiple, file=output)
    print(file=output)
    for arrangements in record_arrangements:
        record = arrangements.record
        print('{} {}'.format(record.springs, print_damaged_counts(record)), file=output)
        num_fillings = arrangements.fillings_count
        arrangements_count = arrangements.arrangements_count
        print('{} filling{}'.format(num_fillings, '' if num_fillings == 1 else 's'), file=output)
        print('{} possible arrangement{}:'
              .format(arrangements_count, '' if arrangements_count == 1 else 's'), file=output)
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
