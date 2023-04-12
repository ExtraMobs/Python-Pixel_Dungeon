import pygame
from noosa.image import Image
from noosa.ui.component import Component
from gameengine.mouse import Mouse


class Button(Component):
    long_click = 1

    hot_area = None

    pressed = False
    press_time = None

    processed = None

    def update(self):
        super().update()

        if Mouse.get_pressed(pygame.BUTTON_LEFT):
            self.pressed = self.inside(Mouse.pos.x, Mouse.pos.y)
        else:
            self.pressed = False
