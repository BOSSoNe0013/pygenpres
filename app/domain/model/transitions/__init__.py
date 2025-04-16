from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import uuid4

from app.domain.model import ModelObject


class TransitionId(str):
    pass

@dataclass
class Transition(ModelObject):
    id: Optional[TransitionId] = field(
        default_factory=lambda: TransitionId(str(uuid4())))
    name: str = ""
    duration: float = 0.0
    timing_function: str = "linear"
    delay: float = 0.0
    direction: str = "normal"
    fill_mode: str = "unset"
    time_line: str = ""
    iteration_count: int = 1
    keyframe: str = ""

    def get(self) -> str:
        return f"""animation-duration: {self.duration}s;
animation-timing-function: {self.timing_function};
animation-delay: {self.delay}s;
animation-iteration-count: {self.iteration_count};
animation-direction: {self.direction};
animation-fill-mode: {self.fill_mode};
animation-name: {self.name}-{self.id};
animation-timeline: {self.time_line};"""

    def get_keyframe(self) -> str:
        return f"""@keyframes {self.name}-{self.id} {{
        {self.keyframe}
}}"""
