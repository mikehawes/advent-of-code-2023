from dataclasses import dataclass

from day19.parts import PartRange
from day19.workflows import Part, WorkflowState, Rule, WorkflowsContext


@dataclass(frozen=True)
class AcceptPart(Rule):
    def next_state(self, part: Part) -> WorkflowState:
        return WorkflowState(accepted=True)

    def filter_ranges(self, parts: PartRange, context: WorkflowsContext) -> PartRange:
        return parts


@dataclass(frozen=True)
class RejectPart(Rule):
    def next_state(self, part: Part) -> WorkflowState:
        return WorkflowState(accepted=False)

    def filter_ranges(self, parts: PartRange, context: WorkflowsContext) -> None:
        return None


@dataclass(frozen=True)
class GoToWorkflow(Rule):
    workflow: str

    def next_state(self, part: Part) -> WorkflowState:
        return WorkflowState(next_workflow=self.workflow)

    def filter_ranges(self, parts: PartRange, context: WorkflowsContext) -> PartRange | None:
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

    def filter_ranges(self, parts: PartRange, context: WorkflowsContext) -> PartRange | None:
        parts_then, parts_else = self.get_then_and_else(parts)
        return parts_then

    def get_then_and_else(self, parts: PartRange) -> (PartRange, PartRange):
        match self.test:
            case '>':
                return (parts.with_attribute_min(self.attribute, self.value + 1),
                        parts.with_attribute_max(self.attribute, self.value))
            case '<':
                return (parts.with_attribute_max(self.attribute, self.value - 1),
                        parts.with_attribute_min(self.attribute, self.value))


@dataclass(frozen=True)
class RemainingWorkflow(WorkflowsContext):
    context: WorkflowsContext
    rules: list[Rule]

    def filter_by_workflow(self, workflow: str, parts: PartRange) -> PartRange | None:
        return self.context.filter_by_workflow(workflow, parts)

    def filter_by_remaining_workflow(self, parts: PartRange) -> PartRange | None:
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

    def filter_ranges(self, parts: PartRange, context: WorkflowsContext) -> PartRange | None:
        return RemainingWorkflow(context, self.rules).filter_by_remaining_workflow(parts)
