from dataclasses import dataclass

from app import Transition


@dataclass
class Parallax(Transition):

    def __post_init__(self):
        self.name = 'parallax'
        self.duration = 0.8
        self.fill_mode = 'both'
        self.time_line = '--slide'
        self.keyframe = """
0% {
    transform: translateY(calc(-100% * var(--i)));
    opacity: 0;
}
50% {
    opacity: 0.2;
}
100% {
    transform: translateY(calc(100% * var(--i)));
    opacity: 0;
}"""
