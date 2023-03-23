from functools import lru_cache

import pygame
from gameengine import FRect
from gameengine import Display

from .visual import Visual


class Image(Visual):
    __origin_texture = None
    __texture = None
    frame = None

    flip_horizontal = None
    flip_vertical = None

    dirty = None

    def __init__(self, tx=None) -> None:
        if tx is None:
            super().__init__(0, 0, 0, 0)
        else:
            self.set_texture(tx)

    def set_scale(self, x, y):
        super().set_scale(x, y)
        self.__texture = self.scale_surface(x, y)
        
    @lru_cache
    def scale_surface(self, x, y):
        return pygame.transform.scale_by(self.__origin_texture, (x, y))

    def set_texture(self, tx):
        self.__origin_texture = tx
        self.set_frame(FRect(0, 0, 1, 1))
        self.set_scale(*self.scale.xy)

    def get_texture(self):
        return self.__texture

    def set_frame(self, frame=None, left=None, top=None, width=None, height=None):
        if frame is not None:
            self.frame = frame

            self.width = frame.width
            self.height = frame.height
        elif None not in (left, top, width, height):
            self.set_frame(FRect(left, top, left + width, top + height))

    def get_frame(self):
        return FRect(frect=self.frame)

    def copy(self, other):
        self.__origin_texture = other.texture
        self.frame = FRect(frect=other.frame)
        
        self.width = other.width
        self.height = other.height
    
        self.dirty = True

    def draw(self):
        super().draw()
        
        if self.dirty:
            Display.surface.blit(self.__origin_texture, (self.x, self.y))
            self.dirty = False
