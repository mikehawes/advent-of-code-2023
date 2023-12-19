from dataclasses import dataclass

from day19.parts import PartRange
from day19.workflows import Part, WorkflowState, Rule, WorkflowsContext


@dataclass(frozen=True)
class AcceptPart(Rule):
    def next_state(self, part: Part) -> WorkflowState:
        return WorkflowState(accepted=True)

    def filter_ranges(self, parts: list[PartRange], context: WorkflowsContext) -> list[PartRange]:
        return parts


@dataclass(frozen=True)
class RejectPart(Rule):
    def next_state(self, part: Part) -> WorkflowState:
        return WorkflowState(accepted=False)

    def filter_ranges(self, parts: list[PartRange], context: WorkflowsContext) -> list[PartRange]:
        return []


@dataclass(frozen=True)
class GoToWorkflow(Rule):
    workflow: str

    def next_state(self, part: Part) -> WorkflowState:
        return WorkflowState(next_workflow=self.workflow)

    def filter_ranges(self, parts: list[PartRange], context: WorkflowsContext) -> list[PartRange]:
        return context.filter_by_workflow(self.workflow, parts)


@dataclass(frozen=True)
class CompareAttribute(Rule):
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

    def filter_ranges(self, parts: list[PartRange], context: WorkflowsContext) -> list[PartRange]:
        parts_then, parts_else = self.get_then_and_else(parts)
        if self.next_workflow == 'R':
            parts_then = []
        elif self.next_workflow != 'A':
            parts_then = context.filter_by_workflow(self.next_workflow, parts_then)
        parts_else = context.filter_by_remaining_workflow(parts_else)
        return parts_then + parts_else

    def get_then_and_else(self, parts: list[PartRange]) -> (list[PartRange], list[PartRange]):
        match self.test:
            case '>':
                return (list(map(lambda p: p.with_attribute_min(self.attribute, self.value + 1), parts)),
                        list(map(lambda p: p.with_attribute_max(self.attribute, self.value), parts)))
            case '<':
                return (list(map(lambda p: p.with_attribute_max(self.attribute, self.value - 1), parts)),
                        list(map(lambda p: p.with_attribute_min(self.attribute, self.value), parts)))


@dataclass(frozen=True)
class RemainingWorkflow(WorkflowsContext):
    context: WorkflowsContext
    rules: list[Rule]

    def filter_by_workflow(self, workflow: str, parts: list[PartRange]) -> list[PartRange]:
        return self.context.filter_by_workflow(workflow, parts)

    def filter_by_remaining_workflow(self, parts: list[PartRange]) -> list[PartRange]:
        first_rule = self.rules[0]
        remaining = self.rules[1:]
        return first_rule.filter_ranges(parts, RemainingWorkflow(self.context, remaining))


@dataclass(frozen=True)
class Workflow(Rule):
    rules: list[Rule]

    def next_state(self, part: Part) -> WorkflowState:
        for rule in self.rules:
            state = rule.next_state(part)
            if state:
                return state
        raise Exception('No next state found')

    def filter_ranges(self, parts: list[PartRange], context: WorkflowsContext) -> list[PartRange]:
        return RemainingWorkflow(context, self.rules).filter_by_remaining_workflow(parts)
