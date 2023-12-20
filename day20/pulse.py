from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto


class Pulse(Enum):
    LOW = auto()
    HIGH = auto()


@dataclass(frozen=True)
class SendPulse:
    module: str
    pulse: Pulse


@dataclass(frozen=True)
class SentPulse:
    sender: str
    receiver: str
    pulse: Pulse


class Module(ABC):
    @abstractmethod
    def receive(self, pulse: Pulse, from_module: str) -> list[SendPulse]:
        pass

    def set_inputs(self, inputs: list[str]):
        pass
