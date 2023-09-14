import pygame
from gameengine import resources
from gameengine.nodes.node import Node


class PDComponent(Node):
    def __init__(self):
        super().__init__()
        self.rect = pygame.FRect(0, 0, 0, 0)
        self.create_children()

    def set_pos(self, x, y):
        self.rect.topleft = x, y
        self.layout()

    def set_size(self, width, height):
        self.rect.size = width, height
        self.layout()

    def set_rect(self, x, y, width, height):
        self.rect.topleft = x, y
        self.rect.size = width, height

        self.layout()

    def inside(self, x, y):
        self.rect.collidepoint(x, y)

    def fill(self, component):
        self.set_rect(*component.rect.topleft, *component.rect.size)

    def create_children(self):
        pass

    def layout(self):
        pass
