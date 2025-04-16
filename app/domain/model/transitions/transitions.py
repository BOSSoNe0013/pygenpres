from enum import Enum


class Transitions(str, Enum):
    PARALLAX = "parallax"
    FADEOUT = "fadeout"
    TO_LEFT = "to_left"
    TO_RIGHT = "to_right"

    def new_instance(self):
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
        return cls.PARALLAX.new_instance()
