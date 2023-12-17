from collections import deque
from dataclasses import dataclass, field
from heapq import heappop, heappush


class Crucible:
    def __init__(self, location, x_moved=0, y_moved=0, min_move=1, max_move=3):
        self.location = location
        self.x_moved = x_moved
        self.y_moved = y_moved
        self.min_move = min_move
        self.max_move = max_move
        self.moved = x_moved != 0 or y_moved != 0
        if x_moved > 0:
            direction = '>'
            distance = abs(x_moved)
        elif x_moved < 0:
            direction = '<'
            distance = abs(x_moved)
        elif y_moved > 0:
            direction = 'v'
            distance = abs(y_moved)
        elif y_moved < 0:
            direction = '^'
            distance = abs(y_moved)
        else:
            direction = '.'
            distance = ''
        self.str = '{}{}{}'.format(location, direction, distance)

    def move_to(self, location):
        x_move = location.x - self.location.x
        y_move = location.y - self.location.y
        if x_move != 0:
            return Crucible(location, x_move + self.x_moved, 0, self.min_move, self.max_move)
        else:
            return Crucible(location, 0, y_move + self.y_moved, self.min_move, self.max_move)

    def next_locations_unbounded(self):
        abs_x_moved = abs(self.x_moved)
        if 0 < abs_x_moved < self.min_move:
            return [self.location.plus(x=int(self.x_moved / abs_x_moved))]
        abs_y_moved = abs(self.y_moved)
        if 0 < abs_y_moved < self.min_move:
            return [self.location.plus(y=int(self.y_moved / abs_y_moved))]
        locations = []
        if -self.max_move < self.x_moved <= 0:
            locations.append(self.location.plus(x=-1))
        if 0 <= self.x_moved < self.max_move:
            locations.append(self.location.plus(x=1))
        if -self.max_move < self.y_moved <= 0:
            locations.append(self.location.plus(y=-1))
        if 0 <= self.y_moved < self.max_move:
            locations.append(self.location.plus(y=1))
        return locations

    def __repr__(self):
        return self.str


class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.width = len(lines[0])
        self.height = len(lines)

    def find_path(self, start, end):
        if type(start) is Crucible:
            crucible = start
        else:
            crucible = Crucible(start)
        to_end_guesses = [PathGuess(crucible, 0)]
        has_to_end_guess = {crucible.str: True}
        came_from_by_str = {}
        guesses_from_start = GuessesFromStart(self, crucible)
        count = 0
        while to_end_guesses and count < 10_000_000:
            to_end_guess = heappop(to_end_guesses)
            crucible = to_end_guess.crucible
            del has_to_end_guess[crucible.str]
            location = crucible.location
            if location.x == end.x and location.y == end.y:
                break
            from_start_guess = guesses_from_start.guess_for(crucible)
            next_locations = self.next_locations(crucible)
            for next_location in next_locations:
                after_option = PathGuess(crucible.move_to(next_location),
                                         from_start_guess.heat_loss + self.heat_loss(next_location))
                if after_option.heat_loss < guesses_from_start.guess_for(after_option.crucible).heat_loss:
                    came_from_by_str[after_option.crucible.str] = crucible
                    guesses_from_start.set_guess(after_option)
                    new_to_end_guess = after_option.heat_loss + self.guess_heat_loss_from_to(next_location, end)
                    if after_option.crucible.str not in has_to_end_guess:
                        heappush(to_end_guesses, PathGuess(after_option.crucible, new_to_end_guess))
                        has_to_end_guess[after_option.crucible.str] = True
            count += 1
        path = deque([crucible])
        path_count = 0
        while crucible.str in came_from_by_str and path_count < 1_000_000:
            crucible = came_from_by_str[crucible.str]
            path.appendleft(crucible)
            path_count += 1
        return list(path)

    def heat_loss(self, location):
        return self.lines[location.y][location.x]

    def guess_heat_loss_from_to(self, location, end):
        dist = abs(end.x - location.x) - 1 + abs(end.y - location.y) - 1
        return dist + self.heat_loss(end)

    def next_locations(self, crucible):
        return list(filter(lambda loc: 0 <= loc.x < self.width and 0 <= loc.y < self.height,
                           crucible.next_locations_unbounded()))

    def top_left(self):
        return Location(0, 0)

    def bottom_right(self):
        return Location(self.width - 1, self.height - 1)


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.str = '{},{}'.format(x, y)

    def plus(self, x=0, y=0):
        return Location(self.x + x, self.y + y)

    def __repr__(self):
        return self.str


@dataclass(order=True)
class PathGuess:
    crucible: Crucible = field(compare=False)
    heat_loss: int


class GuessesFromStart:
    def __init__(self, grid, start_crucible):
        self.from_start_by_crucible = {start_crucible.str: PathGuess(start_crucible, 0)}
        self.max_loss = grid.width * grid.height * 9

    def guess_for(self, crucible):
        if crucible.str in self.from_start_by_crucible:
            return self.from_start_by_crucible[crucible.str]
        else:
            return PathGuess(crucible, self.max_loss)

    def set_guess(self, guess):
        self.from_start_by_crucible[guess.crucible.str] = guess


def load_grid_from_file(input_file):
    with open(input_file, 'r') as file:
        return Grid(list(map(
            lambda line: list(map(
                lambda tile: int(tile),
                line.strip())),
            file)))
