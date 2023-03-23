import pygame
from assets import Assets
from gameengine import Resources, Engine
from gameengine.objects import GraphicObject


class Fireball(GraphicObject):
    def __init__(self) -> None:
        super().__init__()

        self.surface = Resources.Surface.new((32, 32))
        self.rect = self.surface.get_rect()

        self.blight_rotate_degrees = 0
        self.blight_angular_speed = -90
        self.flight_rotate_degrees = 0
        self.flight_angular_speed = 360

        self.blight = Assets.FireballSprites.BLIGHT
        self.flight = Assets.FireballSprites.FLIGHT

    def process(self):
        self.surface.fill((0, 0, 0, 0))
        blight = pygame.transform.rotate(self.blight, self.blight_rotate_degrees)
        self.surface.blit(
            blight,
            (
                (self.rect.width - blight.get_width()) / 2,
                (self.rect.height - blight.get_height()) / 2,
            ),
        )
        flight = pygame.transform.rotate(self.flight, self.flight_rotate_degrees)
        self.surface.blit(
            flight,
            (
                (self.rect.width - flight.get_width()) / 2,
                (self.rect.height - flight.get_height()) / 2,
            ),
        )

        self.blight_rotate_degrees -= self.blight_angular_speed * Engine.deltatime
        self.flight_rotate_degrees -= self.flight_angular_speed * Engine.deltatime
