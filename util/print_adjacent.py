import io


def print_adjacent(printouts):
    widths = []
    printouts_lines = []
    max_length = 0
    out = io.StringIO()
    for printout in printouts:
        printout_lines = printout.splitlines()
        printouts_lines.append(printout_lines)
        width = 0
        for line in printout_lines:
            width = max(width, len(line))
        widths.append(width)
        max_length = max(max_length, len(printout_lines))
    for i in range(0, max_length):
        parts = []
        for j in range(0, len(printouts)):
            printout_lines = printouts_lines[j]
            if i < len(printout_lines):
                line = printout_lines[i]
            else:
                line = ''
            parts.append(line.ljust(widths[j]))
        print('    '.join(parts).rstrip(), file=out)
    return out.getvalue()
