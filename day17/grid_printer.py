import io

from day17.crucible import Location


def print_path(grid, path):
    char_by_loc_str = {}
    total_heat_loss = 0
    for crucible in path:
        loc_str = crucible.location.str
        heat_loss = grid.heat_loss(crucible.location)
        if crucible.moved:
            total_heat_loss += heat_loss
        if crucible.x_moved > 0:
            char_by_loc_str[loc_str] = '>'
        elif crucible.x_moved < 0:
            char_by_loc_str[loc_str] = '<'
        elif crucible.y_moved > 0:
            char_by_loc_str[loc_str] = 'v'
        elif crucible.y_moved < 0:
            char_by_loc_str[loc_str] = '^'
    out = io.StringIO()
    print('Total heat loss:', total_heat_loss, file=out)
    for y, line in enumerate(grid.lines):
        for x, tile in enumerate(line):
            loc_str = Location(x, y).str
            if loc_str in char_by_loc_str:
                out.write(char_by_loc_str[loc_str])
            else:
                out.write(str(tile))
        print(file=out)
    return out.getvalue()
