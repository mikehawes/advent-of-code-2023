import io


def hash_string(string):
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        value %= 256
    return value


def sum_hashes_for_file(input_file):
    with open(input_file, 'r') as file:
        steps = file.readline().strip().split(',')
    return sum(map(hash_string, steps))


class Lens:
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length


def print_boxes(boxes, out):
    for i, box in enumerate(boxes):
        if box:
            printed_lenses = list(map(lambda lens: '{} {}'.format(lens.label, lens.focal_length), box))
            print('Box {}: {}'.format(i, printed_lenses), file=out)


def find_position_with_label(box, label):
    return next(map(lambda p: p[0],
                    filter(lambda p: p[1].label == label,
                           enumerate(box))),
                None)


def print_steps_for_file(input_file):
    out = io.StringIO()
    follow_steps_for_file(input_file, out)
    return out.getvalue()


def follow_steps_for_file(input_file, out=None):
    with open(input_file, 'r') as file:
        steps = file.readline().strip().split(',')

    boxes = list(map(lambda n: [], range(0, 256)))
    for step in steps:
        if step.endswith('-'):
            label = step[:-1]
            box = boxes[hash_string(label)]
            position = find_position_with_label(box, label)
            if position is not None:
                del box[position]
        else:
            parts = step.split('=')
            label = parts[0]
            focal_length = int(parts[1])
            box = boxes[hash_string(label)]
            position = find_position_with_label(box, label)
            lens = Lens(label, focal_length)
            if position is not None:
                box[position] = lens
            else:
                box.append(lens)
        if out:
            print('After "{}":'.format(step), file=out)
            print_boxes(boxes, out)
    return boxes


def get_total_focusing_power_for_file(input_file):
    boxes = follow_steps_for_file(input_file)
    total_focusing_power = 0
    for i, box in enumerate(boxes):
        box_power = i + 1
        for slot, lens in enumerate(box):
            slot_power = slot + 1
            lens_power = box_power * slot_power * lens.focal_length
            total_focusing_power += lens_power
    return total_focusing_power
