from assets import Assets
from gameengine import Display, Engine, Resources
from gameengine.objects import ParticleEmitter
from gameobjetcs import FlameParticle


class Flame(ParticleEmitter):
    def __init__(self, origin) -> None:
        super().__init__(origin, 0.1, 0, FlameParticle)
