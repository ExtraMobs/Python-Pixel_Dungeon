import pygame

from .standardobject import StandardObject


class GraphicObject(StandardObject):
    def __init__(self) -> None:
        super().__init__()
        self.surface = None
        self.position = pygame.Vector2()

    def render(self, surface):
        surface.blit(self.surface, self.position)
