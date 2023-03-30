import os
import pygame

from gameengine.resources import Resources


class ResourceCache:
    @staticmethod
    def get(asset_key):
        if not Resources.Surface.contains(asset_key):
            Resources.Surface.add_from_file(asset_key, os.path.join(os.path.abspath("assets"), asset_key))
        return Resources.Surface.get(asset_key, False)

    @staticmethod
    def create_solid(color):
        key = "1x1:" + str(color)
        if not Resources.Surface.contains(color):
            color = pygame.Color(color)
            surface = Resources.Surface.new((1, 1))
            surface.fill(color)
            Resources.Surface.set(key, surface)
        return Resources.Surface.get(key, False)
