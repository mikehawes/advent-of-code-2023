from abc import ABC, abstractmethod
from dataclasses import dataclass

from day19.parts import Part, PartRange, full_part_range


class WorkflowsContext(ABC):
    @abstractmethod
    def filter_by_workflow(self, workflow: str, parts: list[PartRange]) -> list[PartRange]:
        pass

    @abstractmethod
    def filter_by_remaining_workflow(self, parts: list[PartRange]) -> list[PartRange]:
        pass


class Rule(ABC):
    @abstractmethod
    def filter_ranges(self, parts: list[PartRange], context: WorkflowsContext) -> list[PartRange]:
        pass


@dataclass(frozen=True)
class Workflows(WorkflowsContext):
    workflows: dict[str, Rule]

    def list_accepted(self, parts: list[Part]) -> list[Part]:
        accepted_ranges = self.find_accepted_ranges()
        return list(filter(lambda p: is_part_in_ranges(p, accepted_ranges), parts))

    def sum_accepted_scores(self, parts: list[Part]) -> int:
        return sum(map(lambda part: part.sum_scores(),
                       self.list_accepted(parts)))

    def find_accepted_ranges(self) -> list[PartRange]:
        return self.filter_by_workflow('in', [full_part_range()])

    def count_accepted_values(self) -> int:
        return sum(map(lambda r: r.count_distinct_combinations(),
                       self.find_accepted_ranges()))

    def filter_by_workflow(self, workflow: str, parts: list[PartRange]) -> list[PartRange]:
        return self.workflows[workflow].filter_ranges(parts, self)

    def filter_by_remaining_workflow(self, parts: PartRange) -> list[PartRange]:
        return []


def is_part_in_ranges(part, ranges):
    for part_range in ranges:
        if part_range.contains(part):
            return True
    return False
