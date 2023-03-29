import math
from gameengine.window import Window
from noosa.camera import Camera
from noosa.scene import Scene


class PixelScene(Scene):
    MIN_WIDTH_P = 128
    MIN_HEIGHT_P = 224

    MIN_WIDTH_L = 224
    MIN_HEIGHT_L = 160

    default_zoom = 0

    min_zoom = None
    max_zoom = None

    ui_camera = None

    font_1x = None
    font_15x = None
    font_2x = None
    font_25x = None
    font_3x = None

    window_density = 1  # temp

    def create(self):
        super().create()

        min_width = min_height = None
        if Window.is_landscape():
            min_width = self.MIN_WIDTH_L
            min_height = self.MIN_HEIGHT_L
        else:
            min_width = self.MIN_WIDTH_P
            min_height = self.MIN_HEIGHT_P

        self.default_zoom = math.ceil(self.window_density * 2.5)
        while (
            (Window.width / self.default_zoom < min_width)
            or (Window.height / self.default_zoom < min_height)
        ) and self.default_zoom > 1:
            self.default_zoom -= 1

        # TODO
        # if (PixelDungeon.scaleUp()) {
        # 		while (
        # 			Game.width / (defaultZoom + 1) >= minWidth &&
        # 			Game.height / (defaultZoom + 1) >= minHeight) {

        # 			defaultZoom++;
        # 		}
        # 	}

        self.min_zoom = 1
        self.max_zoom = self.default_zoom * 2

        Camera.reset(self.PixelCamera(self.default_zoom))

        ui_zoom = self.default_zoom
        self.ui_camera = Camera.create_fullscreen(ui_zoom)
        Camera.add(self.ui_camera)

    class PixelCamera(Camera):
        def __init__(self, zoom):
            super().__init__(
                int(Window.width - math.ceil(Window.width / zoom) * zoom) / 2,
                int(Window.height - math.ceil(Window.height / zoom) * zoom) / 2,
                math.ceil(Window.width / zoom),
                math.ceil(Window.height / zoom),
                zoom,
            )

        def update(self):
            super().update()
            # aling
