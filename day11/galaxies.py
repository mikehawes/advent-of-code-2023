import re


class Galaxies:
    def __init__(self, lines):
        self.lines = lines
        self.expansion_by_y = {}
        for y, line in enumerate(lines):
            if re.match(r'^\.+$', line):
                self.expansion_by_y[y] = True
        self.expansion_by_x = {}
        for x in range(0, len(lines[0])):
            col_empty = True
            for y in range(0, len(lines)):
                if lines[y][x] != '.':
                    col_empty = False
                    break
            if col_empty:
                self.expansion_by_x[x] = True
        self.galaxies = []
        for y, line in enumerate(lines):
            for x, contents in enumerate(line):
                if contents == '#':
                    self.galaxies.append((x, y))

    def expand_lines(self):
        expanded_lines = []
        for y, line in enumerate(self.lines):
            expanded_line = []
            for x, contents in enumerate(line):
                expanded_line.append(contents)
                if x in self.expansion_by_x:
                    expanded_line.append(contents)
            expanded_line = ''.join(expanded_line)
            expanded_lines.append(expanded_line)
            if y in self.expansion_by_y:
                expanded_lines.append(expanded_line)
        return expanded_lines

    def sum_distances(self, expansion):
        galaxies = self.galaxies
        total_distance = 0
        for i, a in enumerate(galaxies[:len(galaxies) - 1]):
            for b in galaxies[i + 1:]:
                ax, bx, ay, by = (a[0], b[0], a[1], b[1])
                x1 = min(ax, bx)
                x2 = max(ax, bx)
                y1 = min(ay, by)
                y2 = max(ay, by)
                dist_x = x2 - x1
                dist_y = y2 - y1
                for x in range(x1 + 1, x2):
                    if x in self.expansion_by_x:
                        dist_x += expansion
                for y in range(y1 + 1, y2):
                    if y in self.expansion_by_y:
                        dist_y += expansion
                total_distance += dist_x + dist_y
        return total_distance


def read_galaxies_from_file(input_file):
    with open(input_file, 'r') as file:
        raw_lines = file.readlines()
    lines = list(map(lambda ln: ln.strip(), raw_lines))
    return Galaxies(lines)


def read_and_expand_space_from_file(input_file):
    return read_galaxies_from_file(input_file).expand_lines()


def sum_galaxy_distances_from_file(input_file):
    galaxies = read_galaxies_from_file(input_file)
    return galaxies.sum_distances(1)
