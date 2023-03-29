import math

import pygame

from gameengine.engine import Engine
from gameengine.window import Window
from noosa._utils import Array
from noosa.gizmo import Gizmo
from utils.random import Random


class Camera(Gizmo):
    all = Array()
    invW2 = None
    invH2 = None

    main = None

    zoom = None

    x = None
    y = None
    width = None
    height = None

    screen_width = None
    screen_height = None

    scroll = None
    target = None

    shake_mag_x = None
    shake_mag_y = None
    shake_time = None
    shake_duration = None

    shake_x = None
    shake_y = None

    @classmethod
    def reset(cls, new_camera=None):
        if new_camera is None:
            return cls.reset(cls.create_fullscreen(1))
        else:
            cls.invW2 = 2 / Window.width
            cls.invH2 = 2 / Window.height

            for camera in cls.all:
                camera.destroy()
            cls.all.clear()

            cls.main = cls.add(new_camera)
            return cls.main

    @classmethod
    def add(cls, camera):
        cls.all.append(camera)
        return camera

    @classmethod
    def remove(cls, camera):
        cls.all.remove(camera)
        return camera

    @classmethod
    def update_all(cls):
        for c in cls.all:
            if c.exists and c.active:
                c.update()

    @classmethod
    def create_fullscreen(cls, zoom):
        w = math.ceil(Window.width / zoom)
        h = math.ceil(Window.height / zoom)
        return cls(
            (Window.width - w * zoom) / 2, (Window.height - w * zoom) / 2, w, h, zoom
        )

    def __init__(self, x, y, width, height, zoom):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.zoom = zoom

        self.screen_width = width * zoom
        self.screen_height = height * zoom

        self.scroll = pygame.Vector2()

    def destroy(self):
        self.target = None

    def set_zoom(self, value, fx=None, fy=None):
        if None in (fx, fy):
            self.set_zoom(
                value,
                self.scroll.x + self.width / 2,
                self.scroll.y + self.height / 2,
            )
        else:
            self.zoom = value
            self.width = self.screen_width // self.zoom
            self.height = self.screen_height // self.zoom
            self.focus_on(fx, fy)

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.screen_width = int(width * self.zoom)
        self.screen_height = int(height * self.zoom)

    def update(self):
        super().update()

        if self.target is not None:
            self.focus_on(self.target)

        self.shake_time -= Engine.deltatime
        if self.shake_time > 0:
            damping = self.shake_time / self.shake_duration
            self.shake_x = (
                Random.from_range_float(-self.shake_mag_x, +self.shake_mag_x) * damping
            )
            self.shake_y = (
                Random.from_range_float(-self.shake_mag_y, +self.shake_mag_y) * damping
            )
        else:
            self.shake_x = 0
            self.shake_y = 0

    def center(self):
        return pygame.Vector2(self.width / 2, self.height / 2)

    def hit_test(self, x, y):
        return (
            x >= self.x
            and y >= self.y
            and x < self.x + self.screen_width
            and y < self.y + self.screen_height
        )

    def focus_on(self, visual=None, point=None, x=None, y=None):
        if visual is not None:
            self.focus_on(point=visual.center())
        elif point is not None:
            self.focus_on(x=point.x, y=point.y)
        elif None not in (x, y):
            self.scroll.update(x, y)

    def screen_to_camera(self, x, y):
        return pygame.Vector2(
            x - self.x / self.zoom + self.scroll.x,
            y - self.y / self.zoom + self.scroll.y,
        )

    def camera_to_screen(self, x, y):
        return pygame.Vector2(
            int((x - self.scroll.x) * self.zoom + self.x),
            int((y - self.scroll.y) * self.zoom + self.y),
        )

    def get_screen_width(self):
        return self.width * self.zoom

    def get_screen_height(self):
        return self.height * self.zoom

    def shake(self, magnitude, duration):
        self.shake_mag_x = self.shake_mag_y = magnitude
        self.shake_time = self.shake_duration = duration
