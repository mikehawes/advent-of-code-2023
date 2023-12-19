from dataclasses import dataclass


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

    def __str__(self):
        return '      '.join(map(
            print_attribute_range,
            self.range_by_attribute.items()))


def print_attribute_range(item: (str, ScoreRange)) -> str:
    attribute, score = item
    score_range = '{}-{}'.format(
        str(score.min_score).rjust(4),
        str(score.max_score).ljust(4))
    return '{}: {}'.format(attribute, score_range)


def full_part_range():
    return range_with_all_attributes_same(ScoreRange(1, 4000))


def all_attributes():
    return list('xmas')


def range_with_all_attributes_same(set_range):
    return PartRange(dict(map(lambda attribute: (attribute, set_range),
                              all_attributes())))
