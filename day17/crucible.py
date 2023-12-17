from collections import deque
from dataclasses import dataclass, field
from heapq import heappop, heappush


class Crucible:
    def __init__(self, location, x_moved=0, y_moved=0):
        self.location = location
        self.x_moved = x_moved
        self.y_moved = y_moved
        self.moved = x_moved != 0 or y_moved != 0

    def move_to(self, location):
        x_move = location.x - self.location.x
        y_move = location.y - self.location.y
        if x_move != 0:
            return Crucible(location, x_move + self.x_moved, 0)
        else:
            return Crucible(location, 0, y_move + self.y_moved)

    def __repr__(self):
        return 'at {} moved {},{}'.format(self.location.str, self.x_moved, self.y_moved)


class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.width = len(lines[0])
        self.height = len(lines)

    def find_path(self, start, end):
        crucible = Crucible(start)
        to_end_guesses = [ToEndGuess(crucible, 0)]
        has_to_end_guess = {start.str: True}
        came_from_by_str = {}
        guesses_from_start = LocationHeatLosses(self, start)
        count = 0
        while to_end_guesses and count < 10_000_000:
            next_guess = heappop(to_end_guesses)
            crucible = next_guess.crucible
            location = crucible.location
            if location.x == end.x and location.y == end.y:
                break
            options = self.next_locations(location, crucible)
            for option in options:
                from_start_guess = guesses_from_start.guess_for(location) + self.heat_loss(option)
                if from_start_guess < guesses_from_start.guess_for(option):
                    came_from_by_str[option.str] = crucible
                    guesses_from_start.set_guess(option, from_start_guess)
                    to_end_guess = from_start_guess + option.guess_heat_loss_to(end)
                    if option.str not in has_to_end_guess:
                        heappush(to_end_guesses, ToEndGuess(crucible.move_to(option), to_end_guess))
                        has_to_end_guess[option.str] = True
            count += 1
        path = deque([crucible])
        path_count = 0
        while crucible.location.str in came_from_by_str and path_count < 1_000_000:
            crucible = came_from_by_str[crucible.location.str]
            path.appendleft(crucible)
            path_count += 1
        return list(path)

    def heat_loss(self, location):
        return self.lines[location.y][location.x]

    def guess_heat_loss_to(self, location, end):
        dist = abs(end.x - location.x) + abs(end.y - location.y)
        return dist * 5

    def next_locations(self, location, crucible):
        neighbors = []
        if location.x > 0 and crucible.x_moved < 1:
            neighbors.append(location.plus(x=-1))
        if location.x < self.width - 1 and crucible.x_moved > -1:
            neighbors.append(location.plus(x=1))
        if location.y > 0 and crucible.y_moved < 1:
            neighbors.append(location.plus(y=-1))
        if location.y < self.height - 1 and crucible.y_moved > -1:
            neighbors.append(location.plus(y=1))
        return neighbors

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

    def guess_heat_loss_to(self, end):
        dist = abs(end.x - self.x) + abs(end.y - self.y)
        return dist * 5

    def __repr__(self):
        return self.str


@dataclass(order=True)
class ToEndGuess:
    crucible: Crucible = field(compare=False)
    guess: int


class LocationHeatLosses:
    def __init__(self, grid, start):
        self.from_start_by_loc = {start.str: 0}
        self.max_loss = grid.width * grid.height * 9

    def guess_for(self, location):
        if location.str in self.from_start_by_loc:
            return self.from_start_by_loc[location.str]
        else:
            return self.max_loss

    def set_guess(self, location, from_start):
        self.from_start_by_loc[location.str] = from_start


def load_grid_from_file(input_file):
    with open(input_file, 'r') as file:
        return Grid(list(map(
            lambda line: list(map(
                lambda tile: int(tile),
                line.strip())),
            file)))
