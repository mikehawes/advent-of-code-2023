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
    range_by_attribute: dict[str, list[ScoreRange]]

    def __str__(self):
        return '\n'.join(map(
            print_attribute_range,
            self.range_by_attribute.items()))

    def with_attribute_min(self, attribute, new_min):
        return self.map_attribute(attribute, lambda r: ScoreRange(new_min, r.max_score))

    def with_attribute_max(self, attribute, new_max):
        return self.map_attribute(attribute, lambda r: ScoreRange(r.min_score, new_max))

    def map_attribute(self, attribute, map_attribute):
        new_ranges = self.range_by_attribute.copy()
        new_ranges[attribute] = list(map(map_attribute, self.range_by_attribute[attribute]))
        return PartRange(new_ranges)


def print_attribute_range(item: (str, list[ScoreRange])) -> str:
    attribute, scores = item
    return '{}: {}'.format(attribute, ', '.join(map(
        lambda score: '{}-{}'.format(score.min_score, score.max_score),
        scores)))


def full_part_range():
    return range_with_all_attributes_same(ScoreRange(1, 4000))


def range_with_all_attributes_same(set_range):
    return PartRange(dict(map(lambda attribute: (attribute, [set_range]),
                              ['x', 'm', 'a', 's'])))
