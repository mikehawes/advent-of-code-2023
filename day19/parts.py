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
    full_range = ScoreRange(1, 4000)
    return PartRange(dict(map(lambda attribute: (attribute, [full_range]),
                              ['x', 'm', 'a', 's'])))
