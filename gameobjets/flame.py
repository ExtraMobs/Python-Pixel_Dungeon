import random
from assets import Assets
from gameengine.objects import GraphicObject
from gameengine import Resources, Display, Engine


class Flame(GraphicObject):
    INTERVAL = 0.3
    QUANTITY = 0
    on = True

    class FlameParticles(GraphicObject):
        def __init__(self, x, y):
            super().__init__()
            self.surface = (
                Assets.FireballSprites.FLAME1
                if random.randint(0, 1) == 0
                else Assets.FireballSprites.FLAME2
            )
            self.time = 0
            self.rect = self.surface.get_rect()

            self.position.x = x
            self.position.y = y

        def process(self, *args, **kwargs):
            super().process(*args, **kwargs)
            self.time += Engine.deltatime
            if self.time >= 0.6:
                self.parent.remove_child(self)
            else:
                self.position.y += -80 * Engine.deltatime
                p = 0.6
                

    def __init__(self) -> None:
        super().__init__()
        self.surface = Resources.Surface.new(Display.size)
        self.count = 0
        self.time = 0

    def process(self, *args, **kwargs):
        super().process(*args, **kwargs)
        if self.on:
            self.time += Engine.deltatime
            while self.time > self.INTERVAL:
                self.time -= self.INTERVAL
                self.parent.add_child(
                    flame:=self.FlameParticles(self.position.x, self.position.y)
                )
                flame.priority=2
                self.count += 1
                if self.QUANTITY > 0 and self.count >= self.QUANTITY:
                    self.on = False
