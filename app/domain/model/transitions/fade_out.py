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
class Fadeout(Transition):
    """
    Represents a fade-out transition effect.
    This transition gradually reduces the opacity of an element to 0 and moves it out of view.
    """

    def __post_init__(self):
        self.name = 'Fadeout'
        self.duration = 0.8
        self.fill_mode = 'both'
        self.time_line = 'auto'
        self.target = "#slide_${position}.hidden"
        self.play_state = 'paused'
        self.keyframe = """
0% {
    opacity: 1;
}
99.9% {
    opacity: 0;
    top: 0;
}
100% {
    opacity: 0;
    top: -100%;
}
"""
