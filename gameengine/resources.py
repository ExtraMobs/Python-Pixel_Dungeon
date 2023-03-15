import pygame


class Resources:
    class Scenes:
        scenes = {}

        @classmethod
        def add(cls, name, pygame_group, *args, **kwargs):
            def call():
                return pygame_group(*args, **kwargs)

            cls.scenes[name] = call

        @classmethod
        def get(cls, name):
            return cls.scenes[name]()

    class Surface:
        surfaces = {}

        @staticmethod
        def load_from_file(path, alpha=True):
            surface = pygame.image.load(path)
            try:
                if alpha:
                    surface = surface.convert_alpha()
                else:
                    surface = surface.convert()
                return surface
            except pygame.error:
                return surface

        @classmethod
        def add_from_file(cls, name, path, alpha=True):
            cls.add(name, cls.load_from_file(path, alpha))

        @classmethod
        def add(cls, name, surface, copy=False):
            if copy:
                surface = surface.copy()
            cls.surfaces[name] = surface

        @classmethod
        def slice(cls, name, *rects):
            surface = cls.get(name)
            return [surface.subsurface(rect).copy() for rect in rects]

        @classmethod
        def get(cls, name, copy=True) -> pygame.Surface:
            surface = cls.surfaces[name]
            if copy:
                return surface.copy()
            else:
                return surface

        @staticmethod
        def new(size, *flags, alpha=True):
            flag = 0
            for f in flags:
                if f != pygame.SRCALPHA:
                    flag |= f
            if alpha:
                flag |= pygame.SRCALPHA
            return pygame.Surface(size, flag)
