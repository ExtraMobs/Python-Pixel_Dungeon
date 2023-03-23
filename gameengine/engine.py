import pygame

from .display import Display
from .mouse import Mouse
from .window import Window

pygame.init()


class Engine:
    scene = None
    request_quit = False
    framerate = 30
    deltatime = 1 / framerate
    clock = pygame.time.Clock()

    @classmethod
    def set_framerate(cls, framerate):
        cls.framerate = framerate

    @classmethod
    def update_events(cls):
        cls.request_quit = len(pygame.event.get(pygame.QUIT)) > 0

        Mouse.update(
            *pygame.event.get(pygame.MOUSEBUTTONDOWN),
            *pygame.event.get(pygame.MOUSEBUTTONUP),
            *pygame.event.get(pygame.MOUSEMOTION),
            *pygame.event.get(pygame.MOUSEWHEEL),
        )

    @classmethod
    def clock_tick(cls):
        cls.deltatime = cls.clock.tick(cls.framerate) / 1000

    @classmethod
    def set_scene(cls, scene):
        cls.scene = scene
        Window.surface.fill((0, 0, 0))

    @classmethod
    def system_exit(cls):
        raise exit(0)

    @classmethod
    def draw_scene(cls):
        if Window.get_size() != Display.get_size():
            cls.scene.render(Display.surface, Display.background)
            pygame.transform.scale(
                Display.surface,
                Window.size,
                Window.surface,
            )
        else:
            cls.scene.render(Window.surface, Display.background)

    @classmethod
    def start_loop(cls):
        while True:
            cls.update_events()

            if cls.scene is not None:
                cls.scene.process()
                cls.draw_scene()

            pygame.display.update()
            cls.clock_tick()
