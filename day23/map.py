from dataclasses import dataclass


@dataclass
class TrailsMap:
    tiles: list[list[str]]

    @staticmethod
    def from_lists(tiles: list[list[str]]):
        return TrailsMap(tiles)
