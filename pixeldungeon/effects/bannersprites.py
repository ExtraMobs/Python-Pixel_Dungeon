import enum

import pygame
from assets import Assets

from utils.resourcecache import ResourceCache


class BannerSprites:
    class Type(enum.Enum):
        PIXEL_DUNGEON = enum.auto()
        BOSS_SLAIN = enum.auto()
        GAME_OVER = enum.auto()
        SELECT_YOUR_HERO = enum.auto()
        PIXEL_DUNGEON_SIGNS = enum.auto()

    @classmethod
    def get(cls, type):
        icon = ResourceCache.get(Assets.BANNERS)
        match type:
            case cls.Type.PIXEL_DUNGEON:
                rect = pygame.Rect(0, 0, 128, 70)
            case cls.Type.BOSS_SLAIN:
                rect = pygame.Rect(0, 70, 128, 35)
            case cls.Type.GAME_OVER:
                rect = pygame.Rect(0, 105, 128, 35)
            case cls.Type.SELECT_YOUR_HERO:
                rect = pygame.Rect(0, 140, 128, 21)
            case cls.Type.PIXEL_DUNGEON_SIGNS:
                rect = pygame.Rect(0, 161, 128, 57)
        return icon.subsurface(rect)
