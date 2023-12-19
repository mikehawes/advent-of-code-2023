from dataclasses import dataclass
from math import prod


@dataclass(frozen=True)
class Part:
    score_by_attribute: dict[str, int]

    def sum_scores(self) -> int:
        return sum(self.score_by_attribute.values())


@dataclass(frozen=True)
class ScoreRange:
    min_score: int
    max_score: int


@dataclass(frozen=True)
class PartRange:
    range_by_attribute: dict[str, ScoreRange]

    def with_attribute_min(self, attribute, new_min):
        return self.map_attribute(attribute, lambda r: ScoreRange(new_min, r.max_score))

    def with_attribute_max(self, attribute, new_max):
        return self.map_attribute(attribute, lambda r: ScoreRange(r.min_score, new_max))

    def map_attribute(self, attribute, map_attribute):
        new_ranges = self.range_by_attribute.copy()
        new_ranges[attribute] = map_attribute(self.range_by_attribute[attribute])
        return PartRange(new_ranges)

    def count_distinct_combinations(self):
        return prod(map(lambda r: r.max_score - r.min_score + 1,
                        self.range_by_attribute.values()))

    def contains(self, part):
        for attribute in all_attributes():
            score_range = self.range_by_attribute[attribute]
            part_score = part.score_by_attribute[attribute]
            if part_score < score_range.min_score or part_score > score_range.max_score:
                return False
        return True


def full_part_range():
    return part_range_for_all_attributes(ScoreRange(1, 4000))


def part_range_for_all_attributes(set_range):
    return PartRange(dict(map(lambda attribute: (attribute, set_range),
                              all_attributes())))


def all_attributes():
    return list('xmas')
