from functools import lru_cache

import pygame

from gameengine.display import Display
from noosa.visual import Visual
import pygame


class Image(Visual):
    origin_texture = None
    mask = None
    filters_ = None
    texture = None
    frame = None

    flip_horizontal = None
    flip_vertical = None

    def __init__(self, tx=None) -> None:
        if tx is None:
            super().__init__(0, 0, 0, 0)
        else:
            self.filters_ = {}
            Image.__init__(self)
            self.set_texture(tx)

    def apply_filters(self, all_=False, scale=False, colors=False, reset_surface=True):
        if reset_surface:
            self.texture = self.origin_texture.copy()
        if all_:
            self.apply_colors()
            self.apply_scale()
        else:
            if colors:
                self.apply_colors()
            if scale:
                self.apply_scale()

    def apply_scale(self):
        @lru_cache
        def scale_surface(surface_buffer, surface_size, x, y):
            return pygame.transform.scale_by(
                pygame.image.frombytes(surface_buffer, surface_size, "RGBA"), (x, y)
            )

        self.texture = scale_surface(
            pygame.image.tobytes(self.texture, "RGBA"),
            self.texture.get_size(),
            self.scale.x,
            self.scale.y,
        )

    def apply_colors(self):
        @lru_cache(None)
        def get_color(rgba, rmgmbmam, ragabaaa):
            r, g, b, a = rgba
            rm, gm, bm, am = rmgmbmam
            ra, ga, ba, aa = ragabaaa
            return (
                r * rm + (ra * 255),
                g * gm + (ga * 255),
                b * bm + (ba * 255),
                a * am + (aa * 255),
            )

        img = pygame.surfarray.pixels3d(self.texture)
        img_alpha = pygame.surfarray.pixels_alpha(self.texture)

        for position in self.mask:
            x, y = position
            color = img[x][y]
            alpha = img_alpha[x][y]

            r, g, b, a = get_color(
                (*color, alpha),
                (self.rm, self.gm, self.bm, self.am),
                (self.ra, self.ga, self.ba, self.aa),
            )
            color[0] = r
            color[1] = g
            color[2] = b
            img_alpha[x][y] = a
        del img
        del img_alpha

    def update_frame(self):
        texture = self.texture if self.texture is not None else self.origin_texture
        self.width = self.frame.width * texture.get_width()
        self.height = self.frame.height * texture.get_height()

    def set_scale(self, x, y):
        self.scale.xy = x, y
        self.filters_["scale"] = True
        self.update_frame()

    def set_texture(self, tx):
        self.origin_texture = tx
        self.mask = pygame.mask.from_surface(tx, 0)
        self.mask = [
            (x, y)
            for x in range(tx.get_width())
            for y in range(tx.get_height())
            if self.mask.get_at((x, y))
        ]
        self.set_frame(pygame.FRect(0, 0, 1, 1))
        self.filters_["all_"] = True

    def set_frame(self, frame=None, left=None, top=None, width=None, height=None):
        if frame is not None:
            self.frame = frame

            self.update_frame()
        elif None not in (left, top, width, height):
            self.set_frame(pygame.FRect(left, top, width, height))

    def get_frame(self):
        return pygame.FRect(frect=self.frame)

    def copy(self, other):
        self.origin_texture = other.texture
        self.frame = pygame.FRect(frect=other.frame)

        self.width = other.width
        self.height = other.height

        self.update_frame()

    def draw(self, x=None, y=None):
        super().draw()
        if len(self.filters_) > 0:
            self.apply_filters(**self.filters_)
            self.filters_.clear()
        pos_to_draw = (self.x, self.y) if (None, None) == (x, y) else (x, y)
        Display.surface.blit(self.texture, pos_to_draw)

    def set_alpha(self, value):
        super().set_alpha(value)
        self.filters_["all_"] = True

    def invert(self):
        super().invert()
        self.filters_["all_"] = True

    def lightness(self, value):
        super().lightness(value)
        self.filters_["all_"] = True

    def tint_rgb(self, r, g, b, strength):
        super().tint_rgb(r, g, b, strength)
        self.filters_["all_"] = True

    def tint_color(self, color, strength):
        super().tint_color(color, strength)
        self.filters_["all_"] = True

    def set_color_rgb(self, r, g, b):
        super().set_color_rgb(r, g, b)
        self.filters_["all_"] = True

    def set_color(self, color):
        super().set_color(color)
        self.filters_["all_"] = True

    def hardlight_rgb(self, r, g, b):
        super().hardlight_rgb(r, g, b)
        self.filters_["all_"] = True

    def hardlight_color(self, color):
        super().hardlight_color(color)
        self.filters_["all_"] = True

    def reset_color(self):
        super().reset_color()
        self.filters_["all_"] = True
