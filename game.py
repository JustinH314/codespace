from utils import *

DEFAULT_OPTIONS = {
    "screen_height": SCREEN_HEIGHT,
    "screen_width": SCREEN_WIDTH
}

class Game:
    def __init__(self, options=DEFAULT_OPTIONS):
        self.screen_height = options["screen_height"]
        self.screen_width = options["screen_width"]
