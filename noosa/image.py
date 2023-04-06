from functools import lru_cache

import pygame

from gameengine.display import Display
from noosa.visual import Visual
import pygame


class Image(Visual):
    origin_texture = None
    texture = None
    frame = None

    flip_horizontal = None
    flip_vertical = None

    dirty = None

    def __init__(self, tx=None) -> None:
        if tx is None:
            super().__init__(0, 0, 0, 0)
        else:
            Image.__init__(self)
            self.set_texture(tx)

    def set_scale(self, x, y):
        self.scale.xy = x, y
        self.texture = self.scale_surface(x, y)
        self.update_frame()

    @lru_cache
    def scale_surface(self, x, y):
        return pygame.transform.scale_by(self.origin_texture, (x, y))

    def update_frame(self):
        self.dirty = True

    def set_texture(self, tx):
        self.origin_texture = tx
        self.set_frame(pygame.FRect(0, 0, 1, 1))
        self.set_scale(self.scale.x, self.scale.y)

    def set_frame(self, frame=None, left=None, top=None, width=None, height=None):
        if frame is not None:
            self.frame = frame

            self.width = frame.width
            self.height = frame.height
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
        pos_to_draw = (self.x, self.y) if (None, None) == (x, y) else (x, y)
        if self.dirty:
            Display.surface.blit(self.texture, pos_to_draw)
            self.dirty = False
