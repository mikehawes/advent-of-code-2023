class SpringConditionRecord:
    def __init__(self, springs, damaged_groups):
        self.springs = springs
        self.damaged_groups = damaged_groups


def read_spring_condition_line(line):
    parts = line.rstrip().split(' ')
    return SpringConditionRecord(parts[0], parts[1].split(','))


def read_spring_conditions_from_file(input_file):
    with open(input_file, 'r') as file:
        return list(map(read_spring_condition_line, file))
