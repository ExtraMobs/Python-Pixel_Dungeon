from assets import Assets
from gameengine import Display
from gameengine.objects import GraphicObject


class Title(GraphicObject):
    DASHBOARD_SIZE = 48

    def __init__(self) -> None:
        super().__init__()

        self.surface = Assets.BannerSprites.PIXEL_DUNGEON
        self.rect = self.surface.get_rect()

        height = self.rect.height + (
            self.DASHBOARD_SIZE if Display.is_landscape() else self.DASHBOARD_SIZE * 2
        )

        self.position.x = (Display.width - self.rect.width) / 2
        self.position.y = (Display.height - height) / 2
