import pygame

from assets import Assets
from gameengine.engine import Engine
from noosa.group import Group
from noosa.image import Image
from noosa.particles.emitter import Emitter
from noosa.particles.pixelparticle import PixelParticle
from noosa.ui.component import Component
from utils.colormath import ColorMath
from utils.random import Random
from utils.resourcecache import ResourceCache


class Fireball(Component):
    BLIGHT = pygame.FRect(0.00, 0.00, 0.25, 1)
    FLIGHT = pygame.FRect(0.25, 0.00, 0.50, 1)
    FLAME1 = pygame.FRect(0.50, 0.00, 0.75, 1)
    FLAME2 = pygame.FRect(0.75, 0.00, 1.00, 1)

    COLOR = 0xFF66FF

    b_light = None
    f_light = None
    emitter = None
    sparks = None

    def create_children(self):
        super().create_children()

        self.sparks = Group()
        self.add(self.sparks)

        self.b_light = Image(ResourceCache.get(Assets.FIREBALL))
        self.b_light.set_frame(self.b_light)
        self.b_light.origin.update(self.b_light.width / 2)
        self.b_light.angular_speed = -90
        self.add(self.b_light)

        def override_emit(emitter, index, x, y):
            p = emitter.recycle(Fireball.Flame)
            p.reset()
            p.x = x - p.width / 2
            p.y = y - p.height / 2

        self.emitter = Emitter()
        factory = Emitter.Factory()
        factory.emit = override_emit
        self.emitter.pour(factory, 0.1)
        self.add(self.emitter)

        self.f_light = Image(ResourceCache.get(Assets.FIREBALL))
        self.f_light.set_frame(self.FLIGHT)
        self.f_light.origin.update(self.f_light.width / 2)
        self.f_light.angular_speed = 360
        self.add(self.f_light)

        # TODO
        # bLight.texture.filter( Texture.LINEAR, Texture.LINEAR );

    def layout(self):
        self.b_light.x = self.x - self.b_light.width / 2
        self.b_light.y = self.y - self.b_light.height / 2

        self.emitter.set_pos(
            self.x - self.b_light.width / 4,
            self.y - self.b_light.height / 4,
            self.b_light.width / 2,
            self.b_light.height / 2,
        )

        self.f_light.x = self.x - self.f_light.width / 2
        self.f_light.y = self.y - self.f_light.height / 2

    def update(self):
        super().update()

        if Random.float() < Engine.deltatime:
            spark = self.sparks.recycle(PixelParticle)
            spark.reset(
                self.x,
                self.y,
                ColorMath.random(self.COLOR, 0x66FF66),
                2,
                Random.from_range_float(0.5, 1),
            )
            spark.speed.update(0, 80)
            self.sparks.add(spark)

    class Flame(Image):
        LIFESPAN = 1

        SPEED = -40
        ACC = -20

        time_left = None

        def __init__(self):
            super().__init__(ResourceCache.get(Assets.FIREBALL))
            self.set_frame(
                Fireball.FLAME1 if Random.from_max_int(2) == 0 else Fireball.FLAME2
            )
            self.origin.update(self.width / 2, self.height / 2)
            self.acc.update(0, self.ACC)

        def reset(self):
            self.revive()
            self.time_left = self.LIFESPAN
            self.speed.update(0, self.SPEED)

        def update(self):
            super().update()
            self.time_left -= Engine.deltatime
            if self.time_left <= 0:
                self.kill()
            else:
                p = self.time_left / self.LIFESPAN
                self.set_scale(p, p)
                self.set_alpha((1 - p) * 5 if p > 0.8 else p * 1.25)
