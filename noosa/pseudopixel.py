from noosa.image import Image
from utils.resourcecache import ResourceCache


class PseudoPixel(Image):
    def __init__(self, x=None, y=None, color=None) -> None:
        if None not in (x, y, color):
            self.__init__()

            self.x = x
            self.y = y
            self.set_color(color)
        else:
            super().__init__(ResourceCache.create_solid(0xFFFFFFFF))

    def set_size(self, w=None, h=None, value=None):
        if None not in (w, h):
            self.set_scale(w, h)
        else:
            if type(value) is int:
                self.set_scale(value, value)
            else:
                self.set_scale(value.x, value.y)
