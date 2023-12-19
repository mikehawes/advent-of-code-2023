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
    ranges_by_attribute: dict[str, list[ScoreRange]]

    def with_attribute_min(self, attribute, new_min):
        return self.map_attribute(attribute, lambda r: ScoreRange(new_min, r.max_score))

    def with_attribute_max(self, attribute, new_max):
        return self.map_attribute(attribute, lambda r: ScoreRange(r.min_score, new_max))

    def map_attribute(self, attribute, map_attribute):
        new_ranges = self.ranges_by_attribute.copy()
        new_ranges[attribute] = list(map(map_attribute, self.ranges_by_attribute[attribute]))
        return PartRange(new_ranges)

    def __str__(self):
        return '      '.join(map(
            print_attribute_range,
            self.ranges_by_attribute.items()))


def print_attribute_range(item: (str, list[ScoreRange])) -> str:
    attribute, scores = item
    score_range = ', '.join(map(
        lambda score: '{}-{}'.format(str(score.min_score).rjust(4), str(score.max_score).ljust(4)),
        scores))
    return '{}: {}'.format(attribute, score_range)


def full_part_range():
    return range_with_all_attributes_same(ScoreRange(1, 4000))


def all_attributes():
    return list('xmas')


def range_with_all_attributes_same(set_range):
    return PartRange(dict(map(lambda attribute: (attribute, [set_range]),
                              all_attributes())))


def combine_part_ranges(parts1: PartRange | None, parts2: PartRange | None):
    if parts1 is None:
        return parts2
    if parts2 is None:
        return parts1
    ranges_by_attribute = {}
    for attribute in all_attributes():
        ranges1 = parts1.ranges_by_attribute[attribute]
        ranges2 = parts2.ranges_by_attribute[attribute]
        ranges_by_attribute[attribute] = remove_overlaps(ranges1 + ranges2)
    return PartRange(ranges_by_attribute)


def remove_overlaps(ranges: list[ScoreRange]):
    sorted_ranges = sorted(sorted(ranges, key=lambda r: r.max_score),
                           key=lambda r: r.min_score)
    last_min = None
    last_max = None
    new_ranges = []
    for found in sorted_ranges:
        if found.min_score > found.max_score:
            continue
        if last_min is None:
            last_min = found.min_score
            last_max = found.max_score
            continue
        if last_max >= found.min_score - 1:
            last_max = max(last_max, found.max_score)
        else:
            new_ranges.append(ScoreRange(last_min, last_max))
            last_min = found.min_score
            last_max = found.max_score
    if last_min is not None:
        new_ranges.append(ScoreRange(last_min, last_max))
    return new_ranges
