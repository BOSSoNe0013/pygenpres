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
from enum import Enum


class Transitions(str, Enum):
    """
    Enumeration of available slide transitions.
    Each transition has a corresponding class that implements the transition logic.
    """
    PARALLAX = "parallax"
    FADEOUT = "fadeout"
    TO_LEFT = "to_left"
    TO_RIGHT = "to_right"

    def new_instance(self):
        """
        Creates a new instance of the transition class corresponding to the enum value.

        :return: An instance of the transition class.
        """
        match self:
            case Transitions.PARALLAX:
                from app.domain.model.transitions.parallax import Parallax
                return Parallax()
            case Transitions.FADEOUT:
                from app.domain.model.transitions.fade_out import Fadeout
                return Fadeout()
            case Transitions.TO_LEFT:
                from app.domain.model.transitions.to_left import ToLeft
                return ToLeft()
            case Transitions.TO_RIGHT:
                from app.domain.model.transitions.to_right import ToRight
                return ToRight()
            case _:
                raise ValueError(f'Unknown template: {self}')

    @classmethod
    def default(cls):
        """
        Returns the default transition instance.

        :return: An instance of the default transition class (Parallax).
        """
        return cls.PARALLAX.new_instance()
