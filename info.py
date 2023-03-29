import math

import screeninfo

from gameengine.display import Display


class Info:
    default_zoom = 0

    @classmethod
    def init(cls):
        monitor = screeninfo.get_monitors()[0]
        game_density = (monitor.width * monitor.height) / (
            (monitor.width_mm * monitor.height_mm) / 25.4
        )

        MIN_WIDTH_P = 128
        MIN_HEIGHT_P = 224

        MIN_WIDTH_L = 224
        MIN_HEIGHT_L = 160

        if Display.width > Display.height:
            min_width, min_height = (MIN_WIDTH_L, MIN_HEIGHT_L)
        else:
            min_width, min_height = (MIN_WIDTH_P, MIN_HEIGHT_P)

        cls.default_zoom = math.ceil(game_density * 2.5)
        while (
            Display.width / cls.default_zoom < min_width
            or Display.height / cls.default_zoom < min_height
        ) and cls.default_zoom > 1:
            cls.default_zoom -= 1

        Display.set_scale(cls.default_zoom)
