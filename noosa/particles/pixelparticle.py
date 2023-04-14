from gameengine.engine import Engine
from noosa.pseudopixel import PseudoPixel


class PixelParticle(PseudoPixel):
    size = None
    lifespan = None
    left = None

    def __init__(self) -> None:
        super().__init__()
        self.origin.update(0.5, 0.5)

    def reset(self, x, y, color, size, lifespan):
        self.revive()

        self.x = x
        self.y = y

        self.set_color(color)
        self.size = size
        self.set_size(value=size)

        self.left = self.lifespan = lifespan

    def update(self):
        super().update()
        self.left -= Engine.deltatime
        if self.left <= 0:
            self.kill()


class Shrinking(PixelParticle):
    def update(self):
        super().update()
        self.set_size(value=self.size * self.left / self.lifespan)
