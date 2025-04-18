from dataclasses import dataclass

from app import Transition


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
        self.target = "#slide_${position}.hidden, #slide_${position}.hidden .content"
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
50% {
    opacity: 0.2;
}
100% {
    top: -100%;
    left: 0;
    right: 0;
    opacity: 0;
}"""
