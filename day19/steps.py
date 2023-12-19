from dataclasses import dataclass

from day19.parts import PartRange
from day19.workflows import Part, WorkflowState, Step, WorkflowsContext


@dataclass(frozen=True)
class AcceptPart(Step):
    def next_state(self, part: Part) -> WorkflowState:
        return WorkflowState(accepted=True)

    def filter_ranges(self, parts: PartRange, context: WorkflowsContext) -> PartRange:
        return parts


@dataclass(frozen=True)
class RejectPart(Step):
    def next_state(self, part: Part) -> WorkflowState:
        return WorkflowState(accepted=False)

    def filter_ranges(self, parts: PartRange, context: WorkflowsContext) -> None:
        return None


@dataclass(frozen=True)
class GoToWorkflow(Step):
    workflow: str

    def next_state(self, part: Part) -> WorkflowState:
        return WorkflowState(next_workflow=self.workflow)

    def filter_ranges(self, parts: PartRange, context: WorkflowsContext) -> PartRange | None:
        return context.filter_by_workflow(self.workflow, parts)


@dataclass(frozen=True)
class CompareAttribute(Step):
    attribute: str
    test: str
    value: int
    next_workflow: str

    def next_state(self, part: Part) -> WorkflowState | None:
        if self.meets_condition(part):
            match self.next_workflow:
                case 'A':
                    return WorkflowState(accepted=True)
                case 'R':
                    return WorkflowState(accepted=False)
                case _:
                    return WorkflowState(next_workflow=self.next_workflow)
        else:
            return None

    def meets_condition(self, part: Part) -> bool:
        score = part.score_by_attribute[self.attribute]
        match self.test:
            case '>':
                return score > self.value
            case '<':
                return score < self.value
        raise Exception('Unknown test: {}'.format(self.test))

    def filter_ranges(self, parts: PartRange, context: WorkflowsContext) -> PartRange | None:
        return parts


@dataclass(frozen=True)
class Workflow(Step):
    steps: list[Step]

    def next_state(self, part: Part) -> WorkflowState:
        for step in self.steps:
            state = step.next_state(part)
            if state:
                return state
        raise Exception('No next state found')

    def filter_ranges(self, parts: PartRange, context: WorkflowsContext) -> PartRange | None:
        return parts
