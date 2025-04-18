from dataclasses import dataclass

from app import Transition


@dataclass
class ToLeft(Transition):
    """
    Represents a transition that moves an element to the left.
    The element will slide out of view to the left.
    """

    def __post_init__(self):
        self.name = 'To left'
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
    left: -100%;
    right: 100%;
    opacity: 0;
}"""
