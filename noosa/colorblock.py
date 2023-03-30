from utils.resourcecache import ResourceCache
from noosa.image import Image


class ColorBlock(Image):
    def __init__(self, width, height, color) -> None:
        super().__init__(ResourceCache.create_solid(color))
        self.scale.update(width, height)
        self.origin.update(0, 0)

    def set_size(self, width, height):
        self.scale.update(width, height)

    def get_width(self):
        return self.scale.x

    def get_height(self):
        return self.scale.y
