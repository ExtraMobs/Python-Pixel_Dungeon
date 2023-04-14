import pygame

from assets import Assets
from gameengine.display import Display
from gameengine.engine import Engine
from gameengine.resources import Resources
from noosa.camera import Camera
from noosa.image import Image
from noosa.ui.button import Button
from pixeldungeon.effects.bannersprites import BannerSprites
from pixeldungeon.effects.fireball import Fireball
from pixeldungeon.ui.archs import Archs
from scenes.pixelscene import PixelScene
from utils.resourcecache import ResourceCache


class TitleScene(PixelScene):
    TXT_PLAY = "Play"
    TXT_HIGHSCORES = "Rankings"
    TXT_BADGES = "Badges"
    TXT_ABOUT = "About"

    def create(self):
        super().create()

        # TODO
        # Music.INSTANCE.play( Assets.THEME, true );
        # Music.INSTANCE.volume( 1f );

        self.ui_camera.visible = False

        w = Camera.main.width
        h = Camera.main.height

        archs = Archs()
        archs.set_size(w, h)
        self.add(archs)

        title = Image(BannerSprites.get(BannerSprites.Type.PIXEL_DUNGEON))
        self.add(title)
        height = (
            title.height + self.DashboardItem.SIZE
            if Display.is_landscape()
            else self.DashboardItem.SIZE * 2
        )

        title.x = (w - title.get_width()) / 2
        title.y = (h - height) / 2

        self.place_torch(title.x + 18, title.y + 20)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if Engine.request_quit:
            Engine.system_exit()

    def place_torch(self, x, y):
        fb = Fireball()
        fb.set_pos(x, y)
        self.add(fb)

    class DashboardItem(Button):
        SIZE = 48

        IMAGE_SIZE = 32

        image = None
        label = None

        def __init__(self, text, index) -> None:
            super().__init__()

            self.image = Image(
                Resources.Surface.slice(
                    Assets.DASHBOARD,
                    pygame.Rect(
                        index * self.IMAGE_SIZE,
                        0,
                        (index + 1) * self.IMAGE_SIZE,
                        self.IMAGE_SIZE,
                    ),
                ).copy()
            )
            self.add(self.image)

            self.add(self.label)
            self.label.text(text)
            self.label.measure()

            self.set_size(self.SIZE, self.SIZE)

        def create_children(self):
            super().create_children()

            self.image = ResourceCache.get(Assets.DASHBOARD)
            self.label = PixelScene.create_text(None, 9)

        def layout(self):
            super().layout()

            self.image.x = PixelScene.align(
                pos=self.x + (self.width - self.image.get_width()) / 2
            )
            self.image.y = PixelScene.align(self.y)

            self.label.x = PixelScene.align(
                pos=self.x + (self.width - self.label.get_width()) / 2
            )
            self.label.y = PixelScene.align(self.image.y + self.image.get_height() + 2)

        def update(self):
            super().update()

            if self.pressed:
                self.image.brightness(1.5)
            else:
                self.image.reset_color()
