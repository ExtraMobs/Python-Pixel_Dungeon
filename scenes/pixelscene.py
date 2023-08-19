import math

from gameengine.nodes.scene import Scene


class PixelScene(Scene):
    MIN_WIDTH_P = 128
    MIN_HEIGHT_P = 224

    MIN_WIDTH_L = 224
    MIN_HEIGHT_L = 160

    default_zoom = 0

    window_density = 1  # temp

    def __init__(self):
        super().__init__()

        min_width = min_height = None
        if self.program.display.is_landscape:
            min_width = self.MIN_WIDTH_L
            min_height = self.MIN_HEIGHT_L
        else:
            min_width = self.MIN_WIDTH_P
            min_height = self.MIN_HEIGHT_P

        self.default_zoom = math.ceil(self.window_density * 2.5)
        while (
            (self.program.display.width / self.default_zoom < min_width)
            or (self.program.display.height / self.default_zoom < min_height)
        ) and self.default_zoom > 1:
            self.default_zoom -= 1

        self.min_zoom = 1
        self.max_zoom = self.default_zoom * 2

        self.program.display.set_scale(self.default_zoom)
