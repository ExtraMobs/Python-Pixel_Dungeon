from gameengine.engine import Engine
from noosa.group import Group
from utils.random import Random


class Emitter(Group):
    light_mode = False

    x = None
    y = None
    width = None
    height = None

    target = None

    interval = None
    quantity = None

    on = False

    autokill = True

    count = None
    time = None

    factory = None

    def set_pos(self, x=None, y=None, width=None, height=None, p=None):
        if p is not None:
            self.x, self.y, self.width, self.height = p
        else:
            self.x, self.y, self.width, self.height = x, y, width, height
        if self.x is None:
            self.x = 0
        if self.y is None:
            self.y = 0
        if self.width is None:
            self.width = 0
        if self.height is None:
            self.height = 0
        self.target = None

    def burst(self, factory, quantity):
        self.start(factory, 0, quantity)

    def pour(self, factory, interval):
        self.start(factory, interval, 0)

    def start(self, factory, interval, quantity):
        self.factory = factory
        self.light_mode = factory.light_mode()

        self.interval = interval
        self.quantity = quantity

        self.count = 0
        self.time = Random.from_max_float(interval)

        self.on = True

    def update(self, *args, **kwargs):
        if self.on:
            self.time += Engine.deltatime
            while self.time > self.interval:
                self.time -= self.interval
                self.emit(self.count)
                self.count += 1
                if self.quantity > 0 and self.count >= self.quantity:
                    self.on = False
                    break
        elif self.autokill and self.count_living() == 0:
            self.kill()
        super().update()

    def emit(self, index):
        if self.target == None:
            self.factory.emit(
                self,
                index,
                self.x + Random.from_max_float(self.width),
                self.y + Random.from_max_float(self.height),
            )
        else:
            self.factory.emit(
                self,
                index,
                self.x + Random.from_max_float(self.target.width),
                self.y + Random.from_max_float(self.target.height),
            )

    class Factory:
        # abstract
        def emit(self, index, x, y):
            ...

        def light_mode(self):
            return False
