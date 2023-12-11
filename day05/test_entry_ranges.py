import unittest

from day05.entry_ranges import RangeMapping, EntryRange, RangeMappings


def single_range(start, length):
    return [EntryRange(start, length)]


def single_mapping(source_start, destination_start, length):
    return RangeMappings([RangeMapping(source_start=source_start, destination_start=destination_start, length=length)])


def assert_that_range_maps_to(test, ranges, mapper, result):
    test.assertEqual(result, repr(mapper.map(ranges)), 'Apply {} for {}'.format(mapper, ranges))


class TestMapSingleRange(unittest.TestCase):

    def test_should_map_range_inside_mapping_source(self):
        ranges = single_range(start=15, length=2)
        mapper = single_mapping(source_start=10, destination_start=20, length=10)
        assert_that_range_maps_to(self, ranges, mapper, "[25 to 26]")

    def test_should_map_range_matching_mapping_source(self):
        ranges = single_range(start=10, length=10)
        mapper = single_mapping(source_start=10, destination_start=20, length=10)
        assert_that_range_maps_to(self, ranges, mapper, "[20 to 29]")

    def test_should_map_range_meeting_start_of_mapping_source(self):
        ranges = single_range(start=10, length=5)
        mapper = single_mapping(source_start=10, destination_start=20, length=10)
        assert_that_range_maps_to(self, ranges, mapper, "[20 to 24]")

    def test_should_map_range_meeting_end_of_mapping_source(self):
        ranges = single_range(start=15, length=5)
        mapper = single_mapping(source_start=10, destination_start=20, length=10)
        assert_that_range_maps_to(self, ranges, mapper, "[25 to 29]")

    def test_should_map_single_range_before_offset(self):
        ranges = single_range(8, 2)
        mapper = single_mapping(source_start=10, destination_start=20, length=10)
        assert_that_range_maps_to(self, ranges, mapper, "[8 to 9]")

    def test_should_map_single_range_after_offset(self):
        ranges = single_range(20, 2)
        mapper = single_mapping(source_start=10, destination_start=20, length=10)
        assert_that_range_maps_to(self, ranges, mapper, "[20 to 21]")

    def test_should_map_single_range_overlapping_start_of_offset(self):
        ranges = single_range(9, 2)
        mapper = single_mapping(source_start=10, destination_start=20, length=10)
        assert_that_range_maps_to(self, ranges, mapper, "[9, 20]")

    def test_should_map_single_range_overlapping_end_of_offset(self):
        ranges = single_range(19, 2)
        mapper = single_mapping(source_start=10, destination_start=20, length=10)
        assert_that_range_maps_to(self, ranges, mapper, "[20, 29]")

    def test_should_map_single_range_overlapping_start_of_offset_meeting_end(self):
        ranges = single_range(5, 15)
        mapper = single_mapping(source_start=10, destination_start=20, length=10)
        assert_that_range_maps_to(self, ranges, mapper, "[5 to 9, 20 to 29]")

    def test_should_map_single_range_overlapping_end_of_offset_meeting_start(self):
        ranges = single_range(10, 15)
        mapper = single_mapping(source_start=10, destination_start=20, length=10)
        assert_that_range_maps_to(self, ranges, mapper, "[20 to 24, 20 to 29]")


class TestMapMultipleRanges(unittest.TestCase):

    def test_should_map_with_two_offset_ranges(self):
        ranges = single_range(10, 15)
        mapper = RangeMappings([
            RangeMapping(source_start=10, destination_start=15, length=10),
            RangeMapping(source_start=20, destination_start=30, length=10)
        ])
        assert_that_range_maps_to(self, ranges, mapper, "[15 to 24, 30 to 34]")
