import pygame

from gameengine.engine import Engine
from noosa.gizmo import Gizmo
from utils import GameMath


class Visual(Gizmo):
    x = None
    y = None
    width = None
    height = None

    __scale = None
    origin = None

    speed = None
    acc = None

    angle = None
    angular_speed = None

    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.__scale = pygame.Vector2(1)
        self.origin = pygame.Vector2()

        self.speed = pygame.Vector2()
        self.acc = pygame.Vector2()

    @property
    def scale(self):return self.__scale
    
    def set_scale(self, x, y): self.scale.xy = x, y

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
        self.speed.xy += d

    # def alpha(self, value=None): O que diabos vou fazer com isso???

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
