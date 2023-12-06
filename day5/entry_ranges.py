class EntryRange:
    def __init__(self, start, length):
        self.start = start
        self.end = start + length
        self.length = length

    def __repr__(self):
        last = self.end - 1
        if self.start == last:
            return str(self.start)
        else:
            return '{} to {}'.format(self.start, last)

    def get_overlap(self, other):
        if self.start < other.start:
            if self.end > other.start:
                return EntryRange(other.start, self.end - other.start)
            else:
                return None
        else:
            if self.start >= other.end:
                return None
            elif self.end <= other.end:
                return self
            else:
                return EntryRange(self.start, other.end - self.start)

    def exclude_range(self, other):
        if self.start < other.start:
            if self.end > other.start:
                return EntryRange(self.start, other.start - self.start)
            else:
                return self
        else:
            if self.start >= other.end:
                return self
            elif self.end <= other.end:
                return None
            else:
                return EntryRange(other.end, self.end - other.end)

    def excluding_ranges(self, ranges):
        result = self
        for other in ranges:
            result = result.exclude_range(other)
            if not result:
                return None
        return result

    def offset(self, offset):
        return EntryRange(self.start + offset, self.length)


class EntryRanges:
    def __init__(self, ranges):
        self.ranges = ranges

    def __repr__(self):
        return '{}'.format(self.ranges)


class RangeMapping:
    def __init__(self, destination_start, source_start, length):
        self.source_range = EntryRange(source_start, length)
        self.offset = destination_start - source_start

    def __repr__(self):
        return 'Map<range {}, offset by {}>'.format(self.source_range, self.offset)


class RangeMappings:
    def __init__(self, mappings):
        self.mappings = mappings

    def __repr__(self):
        return '{}'.format(self.mappings)

    def map(self, entry_ranges):
        ranges_to_offset = []
        offsets = []
        for mapping in self.mappings:
            for entry_range in entry_ranges:
                overlap = entry_range.get_overlap(mapping.source_range)
                if overlap:
                    ranges_to_offset.append(overlap)
                    offsets.append(mapping.offset)
        result_ranges = []
        for entry_range in entry_ranges:
            result = entry_range.excluding_ranges(ranges_to_offset)
            if result:
                result_ranges.append(result)
        for i in range(0, len(ranges_to_offset)):
            result_ranges.append(ranges_to_offset[i].offset(offsets[i]))

        return result_ranges
