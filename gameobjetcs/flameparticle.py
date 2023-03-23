from functools import lru_cache
import random

import pygame

from assets import Assets
from gameengine import Engine
from gameengine.objects import Particle


class FlameParticle(Particle):
    def __init__(self, origin):
        super().__init__(1)
        self.original_surface = (
            Assets.FireballSprites.FLAME1
            if random.randint(0, 1) == 0
            else Assets.FireballSprites.FLAME2
        )
        self.surface = self.original_surface
        self.time = 0
        self.rect = self.surface.get_rect()

        self.position = pygame.Vector2(origin)

    @lru_cache
    def get_scale_by_timeleft(self, p):
        return pygame.transform.scale_by(self.original_surface, p)

    def process(self, *args, **kwargs):
        super().process(*args, **kwargs)
        self.position.y += -80 * Engine.deltatime
        p = self.timeleft / self.lifetime
        self.surface = self.get_scale_by_timeleft(p)
        self.surface.set_alpha(((1 - p) * 5 if p > 0.8 else p * 1.25) * 255)
