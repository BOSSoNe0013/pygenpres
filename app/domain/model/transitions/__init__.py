import os
from dataclasses import dataclass, field
from pathlib import Path
from string import Template
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel

"""
    PyGenPres - A Python Presentation Generator

    Copyright (C) 2025  Cyril BOSSELUT

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from app.domain.model import ModelObject


class TransitionId(str):
    """
    Represents a unique identifier for a transition.

    This class is a subclass of `str` and is used to ensure that transition IDs
    are always strings.
    """
    pass


class TransitionResponse(BaseModel):
    id: str
    name: str
    duration: float = 0.0
    timing_function: str = "linear"
    delay: float = 0.0
    direction: str = "normal"
    fill_mode: str = "unset"
    time_line: str = ""
    iteration_count: int = 1
    play_state: str = "running"
    keyframe: str = ""
    target: str = "#slide_$position"
    extra_css: str = ""


@dataclass
class Transition(ModelObject):
    """
    Represents a transition effect that can be applied to a slide.

    Attributes:
        id (Optional[TransitionId]): The unique identifier of the transition.
        name (str): The name of the transition.
        duration (float): The duration of the transition in seconds.
        timing_function (str): The timing function of the transition (e.g., "linear", "ease-in-out").
        delay (float): The delay before the transition starts in seconds.
        direction (str): The direction of the transition (e.g., "normal", "reverse").
    """
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
    play_state: str = "running"
    keyframe: str = ""
    target: str = "#slide_$position"
    extra_css: str = ""

    def get(self, slide_position: int) -> str:
        """
        Generates the CSS code for the transition.

        Args:
            slide_position (int): The position of the slide to which the transition is applied.

        Returns:
            str: The CSS code for the transition.

        """
        css_values = {
            'id': self.id,
            'name': self.name.lower().replace(' ', '_'),
            'duration': self.duration,
            'timing_function': self.timing_function,
            'delay': self.delay,
            'direction': self.direction,
            'fill_mode': self.fill_mode,
            'time_line': self.time_line,
            'iteration_count': self.iteration_count,
            'play_state': self.play_state,
            'keyframe': self.keyframe,
            'target': Template(self.target).safe_substitute({'position': slide_position}),
            'position': slide_position,
            'extra_css': self.extra_css
        }
        with open(os.path.join(self.templates_path, 'base_transition.css'), 'r') as css_file:
            css_template = css_file.read()
        return Template(css_template).safe_substitute(css_values)

    @property
    def templates_path(self) -> str:
        """
        Returns the path to the directory containing the transition templates.

        Returns:
            str: The path to the transition templates directory.
        """
        return os.path.join(Path.cwd(), 'res', 'transitions')

    def to_response(self) -> TransitionResponse:
        return TransitionResponse(
            id=self.id,
            name=self.name,
            duration=self.duration,
            timing_function=self.timing_function,
            delay=self.delay,
            direction=self.direction,
            fill_mode=self.fill_mode,
            time_line=self.time_line,
            iteration_count=self.iteration_count,
            play_state=self.play_state,
            keyframe=self.keyframe,
            target=self.target,
            extra_css=self.extra_css
        )

