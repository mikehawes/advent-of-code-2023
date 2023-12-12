import io

from day12.springs import read_spring_conditions_from_file


def print_working_spring_arrangements_for_file(input_file):
    records = read_spring_conditions_from_file(input_file)
    output = io.StringIO()
    for record in records:
        print('{} {}'.format(record.springs, ','.join(record.damaged_groups)), file=output)
    return output.getvalue()
