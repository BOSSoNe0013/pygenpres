from enum import Enum


class Transitions(str, Enum):
    PARALLAX = "parallax"

    def new_instance(self):
        match self:
            case Transitions.PARALLAX:
                from app.domain.model.transitions.parallax import Parallax
                return Parallax()
            case _:
                raise ValueError(f'Unknown template: {self}')

    @classmethod
    def default(cls):
        return cls.PARALLAX.new_instance()
