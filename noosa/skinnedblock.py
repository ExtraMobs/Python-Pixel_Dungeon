import math

from noosa.image import Image
from utils.resourcecache import ResourceCache


class SkinnedBlock(Image):
    offset_x = None
    offset_y = None

    auto_adjust = False

    def __init__(self, width, height, tx) -> None:
        super().__init__(tx)
        self.set_size(width, height)
        self.offset_x = 0
        self.offset_y = 0

    def update_frame(self):
        super().update_frame()
        if self.auto_adjust:
            self.offset_x %= self.origin_texture.get_width()
            self.offset_y %= self.origin_texture.get_height()

    def offset_to(self, x, y):
        self.offset_x = x
        self.offset_y = y
        self.update_frame()

    def offset(self, x, y):
        self.offset_x += x
        self.offset_y += y
        self.update_frame()

    def get_offset_x(self):
        return self.offset_x

    def get_offset_y(self):
        return self.offset_y

    def set_scale(self, x, y):
        super().set_scale(x, y)

    def get_skinned_surface(self):
        o_w = self.origin_texture.get_width()
        o_h = self.origin_texture.get_height()
        s_w = math.ceil(self.width / o_w) + 1
        s_h = math.ceil(self.height / o_h) + 1
        surface = ResourceCache.create_solid(
            (0, 0, 0, 0), (s_w * o_w, s_h * o_h)
        ).copy()
        for y in range(s_h):
            y *= o_h
            for x in range(s_w):
                x *= o_w
                surface.blit(self.texture, (x, y))
        return surface

    def set_size(self, w, h):
        if (w, h) != (self.width, self.height):
            self.width = w
            self.height = h
            self.apply_filters(**self.filters_)
            self.filters_.clear()
            self.texture = self.get_skinned_surface()
            self.update_frame()

    def draw(self):
        self.filters_["reset_surface"] = False
        super().draw(-self.offset_x, -self.offset_y)
