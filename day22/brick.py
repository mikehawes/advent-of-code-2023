from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    x: int
    y: int
    z: int

    def as_list(self):
        return [self.x, self.y, self.z]

    @staticmethod
    def from_list(location):
        return Location(location[0], location[1], location[2])

    def indexed_plus(self, i, plus):
        if i == 0:
            return Location(self.x + plus, self.y, self.z)
        elif i == 1:
            return Location(self.x, self.y + plus, self.z)
        elif i == 2:
            return Location(self.x, self.y, self.z + plus)


@dataclass(frozen=True)
class Size:
    x: int
    y: int
    z: int

    def as_list(self):
        return [self.x, self.y, self.z]


@dataclass(frozen=True)
class SandBrick:
    location: Location
    size: Size

    def max_location(self):
        size = self.size.as_list()
        location = self.location.as_list()
        max_list = []
        for i in range(0, 3):
            if size[i] > 0:
                max_list.append(location[i] + size[i])
            else:
                max_list.append(location[i])
        return Location.from_list(max_list)

    def locations_covered(self):
        locations = [self.location]
        size = self.size.as_list()
        for i in range(0, 3):
            for j in range(0, size[i]):
                locations.append(self.location.indexed_plus(i, j))
        return locations
