from dataclasses import dataclass

from app import Transition


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
0.1% {
    position: fixed;
}
99.9% {
    position: fixed;
    opacity: 0;
    top: 0;
}
100% {
    opacity: 0;
    position: absolute;
    top: -100%;
}
"""
