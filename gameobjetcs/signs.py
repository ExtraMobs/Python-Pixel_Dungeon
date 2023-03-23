import math
from assets import Assets
from gameengine.objects import GraphicObject
from gameengine import Resources, Engine


class Signs(GraphicObject):
    def __init__(self):
        super().__init__()

        self.surface = Assets.BannerSprites.PIXEL_DUNGEON_SIGNS
        self.rect = self.surface.get_rect()
        self.time = 0

    def process(self, *args, **kwargs):
        super().process(*args, **kwargs)
        self.time += Engine.deltatime
        self.surface.set_alpha(math.sin(-self.time) * 255)
