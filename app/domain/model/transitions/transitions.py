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
