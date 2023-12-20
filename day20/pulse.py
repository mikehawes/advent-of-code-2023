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
