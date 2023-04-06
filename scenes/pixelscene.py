import math

from assets import Assets
from gameengine.display import Display
from gameengine.engine import Engine
from gameengine.window import Window
from noosa.bitmaptext import BitmapText
from noosa.bitmaptextmultiline import BitmapTextMultiline
from noosa.camera import Camera
from noosa.colorblock import ColorBlock
from noosa.scene import Scene
from utils.resourcecache import ResourceCache


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

        if self.font_1x is None:
            # 3x5 (6)
            self.font_1x = BitmapText.Font.color_marked(
                ResourceCache.get(Assets.FONTS1X),
                None,
                0x00000000,
                BitmapText.Font.LATIN_FULL,
            )
            self.font_1x.base_line = 6
            self.font_1x.tracking = -1

            # 5x8 (10)
            self.font_15x = BitmapText.Font.color_marked(
                ResourceCache.get(Assets.FONTS15X),
                12,
                0x00000000,
                BitmapText.Font.LATIN_FULL,
            )
            self.font_15x.base_line = 9
            self.font_15x.tracking = -1

            # 6x10 (12)
            self.font_2x = BitmapText.Font.color_marked(
                ResourceCache.get(Assets.FONTS2X),
                14,
                0x00000000,
                BitmapText.Font.LATIN_FULL,
            )
            self.font_2x.base_line = 11
            self.font_2x.tracking = -1

            # 7x12 (15)
            self.font_25x = BitmapText.Font.color_marked(
                ResourceCache.get(Assets.FONTS25X),
                17,
                0x00000000,
                BitmapText.Font.LATIN_FULL,
            )
            self.font_25x.base_line = 13
            self.font_25x.tracking = -1

            # 9x15 (18)
            self.font_3x = BitmapText.Font.color_marked(
                ResourceCache.get(Assets.FONTS3X),
                22,
                0x00000000,
                BitmapText.Font.LATIN_FULL,
            )
            self.font_3x.base_line = 17
            self.font_3x.tracking = -2

    font = None
    scale = None

    @classmethod
    def choose_font(cls, size, zoom=None):
        if zoom is None:
            cls.choose_font(size, cls.default_zoom)
        else:
            pt = size * zoom

            if pt >= 19:
                cls.scale = pt / 19
                if 1.5 <= cls.scale and cls.scale < 2:
                    cls.font = cls.font_25x
                    cls.scale = int(pt / 14)
                else:
                    cls.font = cls.font_3x
                    cls.scale = int(cls.scale)

            elif pt >= 14:
                cls.scale = pt / 14
                if 1.8 <= cls.scale and cls.scale < 2:
                    cls.font = cls.font_2x
                    cls.scale = int(pt / 2)
                else:
                    cls.font = cls.font_25x
                    cls.scale = int(cls.scale)

            elif pt >= 12:
                cls.scale = pt / 12
                if 1.7 <= cls.scale and cls.scale < 2:
                    cls.font = cls.font_15x
                    cls.scale = int(pt / 10)
                else:
                    cls.font = cls.font_2x
                    cls.scale = int(cls.scale)

            elif pt >= 10:
                cls.scale = pt / 10
                if 1.4 <= cls.scale and cls.scale < 2:
                    cls.font = cls.font_1x
                    cls.scale = int(pt / 7)
                else:
                    cls.font = cls.font_15x
                    cls.scale = int(cls.scale)

            else:
                cls.font = cls.font_1x
                cls.scale = max(1, int(pt / 7))
        cls.scale /= zoom

    @classmethod
    def create_text(cls, text, size):
        cls.choose_font(size)

        result = BitmapText(text, cls.font)
        result.scale.update(cls.scale)

        return result

    @classmethod
    def create_multiline(cls, text, size):
        cls.choose_font(size)

        result = BitmapTextMultiline(text, cls.font)
        result.scale.update(cls.scale)

        return result

    @classmethod
    def align(cls, camera, pos, v=None):
        if v is None:
            zoom = cls.default_zoom if camera is None else camera.zoom
            return int(pos * zoom) / zoom
        else:
            c = v.get_camera()
            v.x = cls.align(c, v.x)
            v.y = cls.align(c, v.y)

    no_fade = False

    def fade_in(self, color=None, light=None):
        if (color, light) == (None, None):
            if self.no_fade:
                self.no_fade = False
            else:
                self.fade_in(0xFF000000, False)
        else:
            self.add()

    def draw(self):
        Display.surface.fill((0, 0, 0))
        super().draw()

    class Fader(ColorBlock):
        FADE_TIME = 1

        light = None

        time = None

        def __init__(self, color, light, pixelscene) -> None:
            ui_camera = pixelscene.ui_camera
            super().__init__(ui_camera.width, ui_camera.height, color)

            self.light = light

            self.camera = ui_camera
            self.texture.set_alpha(255)
            self.time = self.FADE_TIME

        def update(self):
            super().update()

            self.time -= Engine.deltatime
            if self.time <= 0:
                self.texture.set_alpha(0)
                self.parent.remove(self)
            else:
                self.texture.set_alpha((self.time / self.FADE_TIME) * 255)

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
