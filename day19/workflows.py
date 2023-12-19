from abc import ABC, abstractmethod
from dataclasses import dataclass

from day19.parts import Part, PartRange, full_part_range


@dataclass
class WorkflowState:
    next_workflow: str | None = None
    accepted: bool = False


class WorkflowsContext(ABC):
    @abstractmethod
    def filter_by_workflow(self, workflow: str, parts: PartRange) -> PartRange | None:
        pass


class Step(ABC):
    @abstractmethod
    def next_state(self, part: Part) -> WorkflowState | None:
        pass

    @abstractmethod
    def filter_ranges(self, parts: PartRange, context: WorkflowsContext) -> PartRange | None:
        pass


@dataclass(frozen=True)
class Workflows(WorkflowsContext):
    workflows: dict[str, Step]

    def is_accepted(self, part: Part) -> bool:
        workflow = self.workflows['in']
        state = workflow.next_state(part)
        while state.next_workflow:
            workflow = self.workflows[state.next_workflow]
            state = workflow.next_state(part)
        return state.accepted

    def list_accepted(self, parts: list[Part]) -> list[Part]:
        return list(filter(self.is_accepted, parts))

    def sum_accepted_scores(self, parts: list[Part]) -> int:
        return sum(map(lambda part: part.sum_scores(),
                       filter(self.is_accepted, parts)))

    def find_accepted_ranges(self) -> PartRange:
        return self.filter_by_workflow('in', full_part_range())

    def filter_by_workflow(self, workflow: str, parts: PartRange) -> PartRange | None:
        return self.workflows[workflow].filter_ranges(parts, self)
