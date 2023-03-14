import math

import pygame

from gameengine import Display, Engine, Resources
from gameengine.objects import GraphicObject


class Archs(GraphicObject):
    SCROLL_SPEED = 20
    reversed = False

    def __init__(self) -> None:
        super().__init__()

        self.surface = Resources.Surface.new(Display.size)
        self.rect = self.surface.get_rect()

        bg_surf = Resources.Surface.get("IMAGE_ARCS1")
        self.bg_surf_rect = bg_surf.get_rect()
        bg_surf_in_display_line = math.ceil(self.rect.width / self.bg_surf_rect.width)
        bg_surf_in_display_col = math.ceil(self.rect.width / self.bg_surf_rect.width)
        self.background = Resources.Surface.new(
            (
                bg_surf_in_display_line * self.bg_surf_rect.width,
                bg_surf_in_display_col * self.bg_surf_rect.height,
            )
        )
        for y in range(bg_surf_in_display_col):
            y *= self.bg_surf_rect.height
            for x in range(bg_surf_in_display_line):
                x *= self.bg_surf_rect.width
                self.background.blit(bg_surf, (x, y))

        fg_surf = Resources.Surface.get("IMAGE_ARCS2")
        self.fg_surf_rect = fg_surf.get_rect()
        fg_surf_in_display_line = math.ceil(self.rect.width / self.fg_surf_rect.width)
        fg_surf_in_display_col = (
            math.ceil(self.rect.height / self.fg_surf_rect.height) + 1
        )
        self.foreground = Resources.Surface.new(
            (
                fg_surf_in_display_line * self.fg_surf_rect.width,
                fg_surf_in_display_col * self.fg_surf_rect.height,
            )
        )
        for y in range(fg_surf_in_display_col):
            y *= self.fg_surf_rect.height
            for x in range(fg_surf_in_display_line):
                x *= self.fg_surf_rect.width
                self.foreground.blit(fg_surf, (x, y))

        self.bg_rect, self.fg_rect = (
            self.background.get_rect(),
            self.foreground.get_rect(),
        )
        self.bg_rect.center = self.rect.center
        self.fg_rect.center = self.rect.center
        self.bg_pos = pygame.Vector2(self.bg_rect.topleft)
        self.fg_pos = pygame.Vector2(self.fg_rect.topleft)

        self.draw_bg_fg()

    def draw_bg_fg(self):
        self.bg_pos.y %= -self.bg_surf_rect.height
        self.fg_pos.y %= -self.fg_surf_rect.height

        self.surface.blit(self.background, self.bg_pos)
        self.surface.blit(self.foreground, self.fg_pos)

    def process(self, *args, **kwargs):
        super().process(*args, **kwargs)
        shift = Engine.deltatime * self.SCROLL_SPEED
        if self.reversed:
            shift = -shift
        self.bg_pos.y -= shift
        self.fg_pos.y -= shift * 2
        self.draw_bg_fg()
