from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Part:
    score_by_attribute: dict[str, int]


@dataclass
class WorkflowState:
    next_workflow: str | None = None
    accepted: bool = False


class Step(ABC):
    @abstractmethod
    def next_state(self, part: Part) -> WorkflowState | None:
        pass


@dataclass
class Workflow:
    steps: list[Step]

    def next_state(self, part: Part) -> WorkflowState:
        for step in self.steps:
            state = step.next_state(part)
            if state:
                return state
        raise Exception('No next state found')


@dataclass
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


class AcceptPart(Step):
    def next_state(self, part: Part) -> WorkflowState:
        return WorkflowState(accepted=True)


class RejectPart(Step):
    def next_state(self, part: Part) -> WorkflowState:
        return WorkflowState(accepted=False)


@dataclass
class GoToWorkflow(Step):
    workflow: str

    def next_state(self, part: Part) -> WorkflowState:
        return WorkflowState(next_workflow=self.workflow)


@dataclass
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
