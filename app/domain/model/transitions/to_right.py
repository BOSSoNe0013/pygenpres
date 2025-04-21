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


from dataclasses import dataclass

from app.domain.model.transitions import Transition


@dataclass
class ToRight(Transition):
    """
    Represents a transition that moves an element to the right.
    The element starts visible and moves off-screen to the right, becoming hidden.
    """

    def __post_init__(self):
        self.name = 'To right'
        self.duration = 0.8
        self.fill_mode = 'both'
        self.time_line = 'auto'
        self.play_state = 'paused'
        self.target = "#slide_${position}.hidden"
        self.keyframe = """
0% {
    opacity: 1;
}
0.1% {
    top: 0;
    left: 0;
    right: 0;
    opacity: 1;
}
75% {
    opacity: 1;
}
100% {
    top: 0;
    left: 100%;
    right: -100%;
    opacity: 0;
}"""
