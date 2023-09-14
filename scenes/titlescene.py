from abc import abstractclassmethod
import enum
import math
import random

import pygame

from assets import Assets, BannerSprites, Flames
from gameengine import resources
from gameengine.misc.timer import Timer
from gameengine.nodes.graphicnode import GraphicNode
from gameengine.nodes.node import Node
from pd_backend.noosa.pdcomponent import PDComponent
from pd_backend.noosa.pdimage import PDImage
from scenes.pixelscene import PixelScene


class SkinnedBlock(PDImage):
    __auto_adjust = False
    offset = pygame.Vector2(0,0)

    # o SkinnedBlock do projeto original, usa o width e height pra propor o tamanho máximo
    # da textura que vai ser repetida, da seguinte maneira:
    # A textura por exemplo tem 32x32
    # Se for 1, então o tamanho de cada textura repetida na tela vai ser a escala original (32x32)
    # Se for 512, então o tamanho de cada textura vai estar no tamanho de 1/16(0.0625x0.0625), DIVIDO pela escala (no caso o zoom da câmera),
    # então se a escala (zoom da câmera) for 2, o tamanho final de cada textura repetida fica 1/8 (0.125x0.125)
    # Então, quanto maior o 'width' e 'height', maior a quantidade de imagens repetidas na imagem.

    # Em resumo, a densidade de imagens no objeto

    def __init__(self, width, height, asset):
        self.texture = resources.surface.get(asset)
        self.width = width
        self.height = height

        self.auto_adjust = False
        super().__init__(self.texture)

    def update(self):
        tex_w, tex_h = self.texture.get_size()
        if self.auto_adjust:
            while self.rect.x > tex_w:
                self.rect.x -= tex_w
            while self.rect.x < -tex_w:
                self.rect.x += tex_w
            while self.rect.y > tex_h:
                self.rect.y -= tex_h
            while self.rect.y < -tex_h:
                self.rect.y += tex_h
        super().update()

    def set_offset_to(self, x, y):
        self.offset.xy = x, y

    def set_offset(self, x, y):
        self.offset += x, y
        
    @property
    def auto_adjust(self):
        return self.__auto_adjust

    @auto_adjust.setter
    def auto_adjust(self, value):
        tex_w, tex_h = self.texture.get_size()

        u0 = 1 / (self.width / tex_w)
        v0 = 1 / (self.height / tex_h)

        chunk_w = math.ceil(self.program.display.width / u0) + 1
        chunk_h = math.ceil(self.program.display.height / v0) + 1

        self.surface = resources.surface.new(
            (
                chunk_w * tex_w,
                chunk_h * tex_h,
            )
        )

        for y in range(chunk_h):
            y *= tex_h
            for x in range(chunk_w):
                x *= tex_w
                self.surface.blit(self.texture, (x, y))

        self.__auto_adjust = value


class Archs(PDComponent):
    SCROLL_SPEED = 20.0

    BG = enum.auto()
    FG = enum.auto()

    arcs_bg = None
    arcs_fg = None

    off_b = 0
    off_f = 0

    reversed = False

    def create_children(self):
        self.arcs_bg = SkinnedBlock(1, 1, Assets.ARCS_BG)
        self.arcs_bg.auto_adjust = True
        self.arcs_bg.offset.xy = 0, self.off_b
        self.add_children(self.arcs_bg)

        self.arcs_fg = SkinnedBlock(1, 1, Assets.ARCS_FG)
        self.arcs_fg.auto_adjust = True
        print(self.arcs_bg.surface.get_size(), self.arcs_fg.surface.get_size())
        self.arcs_fg.offset.xy = 0, self.off_f
        self.add_children(self.arcs_fg)

        self.arcs_fg = SkinnedBlock(1, 1, Assets.ARCS_FG)

    def update(self):
        shift = self.program.time.delta * self.SCROLL_SPEED

        if self.reversed:
            shift = -shift

        self.rect.y += shift


class DashBoardItem:
    SIZE = 48


class Title(GraphicNode):
    def __init__(self):
        super().__init__(resources.surface.get(BannerSprites.PIXEL_DUNGEON))
        height = (
            self.rect.h + DashBoardItem.SIZE
            if self.program.display.is_landscape
            else DashBoardItem.SIZE * 2
        )

        self.rect.x = (self.program.display.width - self.rect.width) / 2
        self.rect.y = (self.program.display.height - height) / 2


class Flame(GraphicNode):
    def __init__(self):
        image_asset = Flames.FLAME1 if random.randint(0, 2) == 0 else Flames.FLAME2
        super().__init__(resources.surface.get(image_asset))


class Factory:
    @abstractclassmethod
    def emit(self, emitter, index, x, y):
        pass


class FireFactory:
    def emit(self, emitter, index, x, y):
        flame = Flame()
        emitter.add(flame)
        flame.rect.center = (x, y)
        # flame.rect.x = x - flame.rect.width / 2
        # flame.rect.y = y - flame.rect.height / 2


class Emitter(Node):
    def __init__(self):
        super().__init__()
        self.on = False
        self.x, self.y, self.width, self.height = 0, 0, 0, 0
        self.target = None

    def pour(self, factory, interval):
        self.start(factory, interval, 0)

    def start(self, factory, interval, quantity):
        self.factory = factory
        interval *= random.random()
        self.timer = Timer(interval, False)
        self.quantity = quantity

        self.count = 0

        self.on = True

    def update(self):
        if self.on:
            for _ in range(self.timer.reached):
                self.emit(self.count)
                self.count += 1

    def emit(self, index):
        if self.target is None:
            # random_x = random.random() * self.
            self.factory.emit(
                self,
                index,
            )


class Fire(PDImage):
    def __init__(self, asset):
        super().__init__(asset)
        self.angular_speed = 0
        self.speed = pygame.Vector2(0)
        self.acc = pygame.Vector2(0)

    def update(self):
        d = ((self.speed * self.program.time.delta) - self.speed) / 2
        self.speed += d
        self.rect.x += self.speed.x * self.program.time.delta
        self.rect.y += self.speed.y * self.program.time.delta

        self.rotation.angle += self.angular_speed * self.program.time.delta


class FireBall(Node):
    def __init__(self):
        super().__init__()

        self.x = 0
        self.y = 0

        self.blight = Fire(Flames.BLIGHT)
        self.blight.rect.topleft = (
            self.blight.rect.width / 2,
            self.blight.rect.height / 2,
        )
        self.blight.angular_speed = -90
        self.add_children(self.blight)

        self.emitter = Emitter()
        self.emitter.pour(FireFactory(), 0.1)
        self.add_children(self.emitter)

        self.flight = Fire(Flames.FLIGHT)
        self.flight.rect.topleft = (
            self.flight.rect.width / 2,
            self.flight.rect.height / 2,
        )
        self.flight.angular_speed = 360
        self.add_children(self.flight)


class TitleScene(PixelScene):
    def __init__(self):
        super().__init__()

        pygame.mixer.Channel(0).play(resources.sound.get(Assets.THEME), -1)
        pygame.mixer.Channel(0).set_volume(1)

        self.add_children(
            Archs(),
            title := Title(),
        )

        self.place_torch(title.rect.x + 18, title.rect.y + 20)
        self.place_torch(title.rect.x - 18, title.rect.y + 20)

    def place_torch(self, x, y):
        fb = FireBall()
        fb.x = x
        fb.y = y
        self.add_children(fb)
