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
