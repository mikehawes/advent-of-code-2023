from dataclasses import dataclass, replace


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
            return self.plus(x=plus)
        elif i == 1:
            return self.plus(y=plus)
        elif i == 2:
            return self.plus(z=plus)

    def plus(self, x=0, y=0, z=0):
        return Location(self.x + x, self.y + y, self.z + z)


@dataclass(frozen=True)
class Size:
    x: int = 1
    y: int = 1
    z: int = 1

    def as_list(self):
        return [self.x, self.y, self.z]

    @staticmethod
    def of_brick(x, y, z):
        size = Size(x, y, z)
        num_greater_than_1 = 0
        for value in size.as_list():
            if value > 1:
                num_greater_than_1 += 1
        if num_greater_than_1 > 1:
            raise Exception('expected brick to have length in only one dimension')
        return size

    @staticmethod
    def of_snapshot(x, y, z):
        return Size(x, y, z)


@dataclass(frozen=True)
class SandBrick:
    location: Location
    size: Size
    index: int

    def max_location(self):
        size = self.size.as_list()
        location = self.location.as_list()
        max_list = []
        for i in range(0, 3):
            if size[i] > 0:
                max_list.append(location[i] + size[i] - 1)
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

    def min_z(self):
        if self.size.z < 0:
            return self.location.z + self.size.z
        else:
            return self.location.z

    def label(self):
        return label_for_index(self.index)

    def plus_location(self, x=0, y=0, z=0):
        return replace(self, location=self.location.plus(x, y, z))


def label_for_index(index):
    letter_index = index % 26
    return chr(ord('A') + letter_index)
