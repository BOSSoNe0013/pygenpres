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
class Parallax(Transition):
    """
    Represents a Parallax transition effect.
    This transition moves the target elements upwards while fading them out.
    """

    def __post_init__(self):
        self.name = 'Parallax'
        self.duration = 1.5
        self.fill_mode = 'both'
        self.time_line = 'auto'
        self.play_state = 'paused'
        self.timing_function = 'ease-in-out'
        self.target = "#slide_${position}.hidden, #slide_${position}.hidden .content, #slide_${position}.hidden .content > *, #slide_${position}.hidden .content div > div"
        self.keyframe = """
0% {
    transform: translateY(0);
    opacity: 1;
}
50% {
    opacity: 0.4;
}
100% {
    transform: translateY(-400%);
    opacity: 0;
}"""
        self.extra_css = f"""
#slide_${{position}}.hidden {{
    animation-delay: {self.duration - 1.0}s;
}}
#slide_${{position}}.hidden .content {{
    animation-delay: 350ms;
}}
@for $i from 1 through 3 {{
    #slide_${{position}} .content > :nth-child(#{{$i}}) {{
        animation-delay: 100ms * $i;
    }}
    #slide_${{position}} .content div > div:nth-child(#{{$i}}) {{
        animation-delay: 50ms * $i;
    }}
}}
"""
