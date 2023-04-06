import pygame

from gameengine.engine import Engine
from noosa.gizmo import Gizmo
from utils.gamemath import GameMath


class Visual(Gizmo):
    x = None
    y = None
    width = None
    height = None

    __scale = pygame.Vector2(1)
    origin = None

    speed = None
    acc = None

    rm = None
    gm = None
    bm = None
    am = None
    ra = None
    ga = None
    ba = None
    aa = None

    angle = 0
    angular_speed = 0

    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.origin = pygame.Vector2()

        self.reset_color()

        self.speed = pygame.Vector2()
        self.acc = pygame.Vector2()
        super().__init__()

    @property
    def scale(self):
        return self.__scale

    def update(self):
        self.update_motion()

    def point(self, p=None):
        if p is None:
            return pygame.Vector2(self.x, self.y)
        else:
            self.x = p.x
            self.y = p.y
            return p

    def center(self, p=None):
        if p is None:
            return pygame.Vector2(self.x + self.width / 2, self.y + self.height / 2)
        else:
            self.x = p.x - self.width / 2
            self.y = p.y - self.height / 2
            return p

    def get_width(self):
        return self.width * self.__scale.x

    def get_height(self):
        return self.height * self.__scale.y

    def update_motion(self):
        d = GameMath.speed(self.speed.x, self.acc.x) - self.speed.x / 2
        self.speed.x += d
        self.x += self.speed.x * Engine.deltatime
        self.speed.x += d

        d = GameMath.speed(self.speed.y, self.acc.y) - self.speed.y / 2
        self.speed.y += d
        self.y += self.speed.x * Engine.deltatime
        self.speed.y += d

        self.angle += self.angular_speed * Engine.deltatime

    def get_alpha(self):
        return self.am + self.aa

    def set_alpha(self, value):
        self.am = value
        self.aa = 0

    def invert(self):
        self.rm = self.gm = self.bm = -1
        self.ra = self.ga = self.ba = 1

    def lightness(self, value):
        if value < 0.5:
            self.rm = self.gm = self.bm = value * 2
            self.ra = self.ga = self.ba = 0
        else:
            self.rm = self.gm = self.bm = 2 - value * 2
            self.ra = self.ga = self.ba = value * 2 - 1

    def brightness(self, value):
        self.rm = self.gm = self.bm = value

    def tint_rgb(self, r, g, b, strength):
        self.rm = self.gm = self.bm = 1 - strength
        self.ra = r * strength
        self.ga = g * strength
        self.ba = b * strength

    def tint_color(self, color, strength):
        self.rm = self.gm = self.bm = 1 - strength
        self.ra = ((color >> 16) & 0xFF) / 255 * strength
        self.ga = ((color >> 8) & 0xFF) / 255 * strength
        self.ba = (color & 0xFF) / 255 * strength

    def set_color_rgb(self, r, g, b):
        self.rm = self.gm = self.bm = 0
        self.ra = r
        self.ga = g
        self.ba = b

    def set_color(self, color):
        self.set_color_rgb(
            ((color >> 16) & 0xFF) / 255,
            ((color >> 8) & 0xFF) / 255,
            (color & 0xFF) / 255,
        )

    def hardlight_rgb(self, r, g, b):
        self.ra, self.ga, self.ba = 0
        self.rm = r
        self.gm = g
        self.bm = b

    def hardlight_color(self, color):
        self.hardlight_rgb(
            ((color >> 16) & 0xFF) / 255,
            ((color >> 8) & 0xFF) / 255,
            (color & 0xFF) / 255,
        )

    def reset_color(self):
        self.rm = self.gm = self.bm = self.am = 1
        self.ra = self.ga = self.ba = self.aa = 0

    def overlap_point(self, x, y):
        return (
            x >= self.x
            and x < self.x + self.width * self.__scale.x
            and y >= self.y
            and y < self.y + self.height * self.__scale.y
        )

    def overlap_screen_point(self, x, y):
        c = self.get_camera()
        if c is not None:
            p = c.screen_to_camera(x, y)
            return self.overlap_point(p.x, p.y)
        else:
            return False

    def is_visible(self):
        c = self.get_camera()
        cx = c.scroll.x
        cy = c.scroll.y
        w = self.get_width()
        h = self.get_height()
        return (
            self.x + w >= cx
            and self.y + h >= cy
            and self.x < cx + c.width
            and self.y < cy + c.height
        )
