import numpy
import pygame

from gameengine.display import Display
from noosa.visual import Visual


class Image(Visual):
    origin_texture = None
    origin_texture_backup = None
    mask = None
    filters_ = None
    texture = None
    frame = None
    int_frame = None

    flip_horizontal = None
    flip_vertical = None

    old_data = [None, None, None]  # last_int_frame  # colors_m  # colors_a
    data_equals = False

    def get_current_data(self):
        return [
            self.int_frame,
            (self.rm, self.gm, self.bm, self.am),
            (self.ra, self.ga, self.ba, self.aa),
        ]

    def check_data_equality(self):
        if self.old_data != [current_data := self.get_current_data()]:
            self.old_data = current_data
            self.data_equals = False
        else:
            self.data_equals = True

    def __init__(self, tx=None) -> None:
        if tx is None:
            super().__init__(0, 0, 0, 0)
        else:
            self.filters_ = {}
            Image.__init__(self)
            self.set_texture(tx)

    def apply_filters(
        self, all_=False, scale=False, rotate=False, colors=False, reset_surface=True
    ):
        if reset_surface:
            self.texture = self.origin_texture.subsurface(self.int_frame)
        if all_:
            self.apply_colors()
            self.apply_rotation()
            self.apply_scale()
        else:
            if colors:
                self.apply_colors()
            if rotate:
                self.apply_rotation()
            if scale:
                self.apply_scale()

    def apply_scale(self):
        def scale_surface(surface, x, y):
            return pygame.transform.scale_by(surface, (x, y))

        if tuple(self.scale) != (1, 1):
            self.texture = scale_surface(
                self.texture, round(self.scale.x, 2), round(self.scale.y, 2)
            )

    def apply_rotation(self):
        def rotate_surface(surface, angle):
            return pygame.transform.rotate(surface, angle)

        if self.angle != 0:
            self.texture = rotate_surface(self.texture, round(self.angle))

    def apply_colors(self):
        self.texture.blit(self.origin_texture_backup, (0, 0), self.int_frame)
        img = pygame.surfarray.pixels3d(self.texture)
        w, h, _ = img.shape
        r = w + self.int_frame.x
        l = h + self.int_frame.y
        img_alpha = pygame.surfarray.pixels_alpha(self.texture)
        if not self.data_equals:
            numpy.multiply(img, (self.rm, self.gm, self.bm), img, casting="unsafe")
            numpy.add(img, self.am)
            numpy.multiply(img_alpha, self.am, img_alpha, casting="unsafe")
            numpy.add(img_alpha, self.aa, img_alpha)
        del img
        del img_alpha

    def update_frame(self):
        texture = self.texture if self.texture is not None else self.origin_texture
        self.width = self.frame.width * texture.get_width()
        self.height = self.frame.height * texture.get_height()

    def set_scale(self, x, y):
        self.scale.xy = x, y
        self.filters_["rotate"] = True
        self.filters_["scale"] = True
        self.update_frame()

    def set_angle(self, new_angle):
        super().set_angle(new_angle)
        self.filters_["rotate"] = True
        self.filters_["scale"] = True

    def set_texture(self, tx):
        self.origin_texture = tx
        self.origin_texture_backup = tx.copy()
        self.mask = pygame.mask.from_surface(tx, 0)
        self.mask = [
            (x, y)
            for x in range(tx.get_width())
            for y in range(tx.get_height())
            if self.mask.get_at((x, y)) == 1
        ]
        self.set_frame(pygame.FRect(0, 0, 1, 1))
        self.filters_["all_"] = True

    def set_frame(self, frame=None, left=None, top=None, width=None, height=None):
        if frame is not None:
            self.frame = frame
            w, h = self.origin_texture.get_size()
            x, y = self.frame.x * w, self.frame.y * h
            r, l = self.frame.width * w, self.frame.height * h
            w, h = max(x, r) - min(x, r), max(y, l) - min(y, l)
            self.int_frame = pygame.Rect(x, y, w, h)

            self.update_frame()
        elif None not in (left, top, width, height):
            self.set_frame(pygame.FRect(left, top, width, height))

    def get_frame(self):
        return pygame.FRect(frect=self.frame)

    def copy(self, other):
        self.origin_texture = other.texture
        self.origin_texture_backup = other.texture.copy()
        self.frame = pygame.FRect(frect=other.frame)

        self.width = other.width
        self.height = other.height

        self.update_frame()

    def update(self):
        super().update()

    def draw(self, x=None, y=None):
        super().draw()
        if len(self.filters_) > 0:
            self.apply_filters(**self.filters_)
            self.filters_.clear()
        pos_to_draw = (self.x, self.y) if (None, None) == (x, y) else (x, y)
        Display.surface.blit(self.texture, pos_to_draw)

    def set_alpha(self, value):
        super().set_alpha(value)
        self._update_filter_color()

    def invert(self):
        super().invert()
        self._update_filter_color()

    def lightness(self, value):
        super().lightness(value)
        self._update_filter_color()

    def tint_rgb(self, r, g, b, strength):
        super().tint_rgb(r, g, b, strength)
        self._update_filter_color()

    def tint_color(self, color, strength):
        super().tint_color(color, strength)
        self._update_filter_color()

    def set_color_rgb(self, r, g, b):
        super().set_color_rgb(r, g, b)
        self._update_filter_color()

    def set_color(self, color):
        super().set_color(color)
        self._update_filter_color()

    def hardlight_rgb(self, r, g, b):
        super().hardlight_rgb(r, g, b)
        self._update_filter_color()

    def hardlight_color(self, color):
        super().hardlight_color(color)
        self._update_filter_color()

    def reset_color(self):
        super().reset_color()
        self._update_filter_color()

    def _update_filter_color(self):
        self.filters_["all_"] = True
        self.check_data_equality()
        if self.data_equals and self.texture is not None:
            self.filters_["reset_surface"] = False
