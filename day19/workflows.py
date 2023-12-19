from abc import ABC, abstractmethod
from dataclasses import dataclass

from day19.parts import Part, PartRange, full_part_range


@dataclass
class WorkflowState:
    next_workflow: str | None = None
    accepted: bool = False


class Step(ABC):
    @abstractmethod
    def next_state(self, part: Part) -> WorkflowState | None:
        pass


@dataclass(frozen=True)
class Workflow:
    steps: list[Step]

    def next_state(self, part: Part) -> WorkflowState:
        for step in self.steps:
            state = step.next_state(part)
            if state:
                return state
        raise Exception('No next state found')


@dataclass(frozen=True)
class Workflows:
    workflows: dict[str, Workflow]

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
        return full_part_range()
