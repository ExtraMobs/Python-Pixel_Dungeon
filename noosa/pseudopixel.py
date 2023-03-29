import pygame

from noosa.image import Image


class PseudoPixel(Image):
    def __init__(self, x=None, y=None, color=None) -> None:
        if None not in (x, y, color):
            self.__init__()

            self.x = x
            self.y = y
            self.get_texture().fill(color)
        else:
            super().__init__(pygame.Surface(1, 1))
            self.get_texture().fill((255, 255, 255))

    def set_size(self, w=None, h=None, value=None):
        if None not in (w, h):
            self.set_scale(w, h)
        else:
            self.set_scale(value.x, value.y)
