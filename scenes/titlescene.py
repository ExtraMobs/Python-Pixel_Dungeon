import enum
import math

from assets import Assets, BannerSprites
from gameengine import resources
from gameengine.nodes.graphicnode import GraphicNode
from scenes.pixelscene import PixelScene


class ArcsChunk(GraphicNode):
    SCROLL_SPEED = 20

    BG = enum.auto()
    FG = enum.auto()

    def __init__(self, arch_type, reversed):
        self.reversed = reversed
        if arch_type == self.BG:
            arch_id = Assets.ARCS_BG
        elif arch_type == self.FG:
            arch_id = Assets.ARCS_FG
        else:
            raise Exception("Invalid 'arch_type' parameter.")

        if arch_type == self.FG:
            self.SCROLL_SPEED *= 2

        arc_surface = resources.surface.get(arch_id)
        self.arc_w, self.arc_h = arc_surface.get_size()

        chunk_w = math.ceil(self.program.display.width / self.arc_w) + 1
        chunk_h = math.ceil(self.program.display.height / self.arc_h) + 1

        super().__init__(
            resources.surface.new(
                size=(
                    chunk_w * self.arc_w,
                    chunk_h * self.arc_h,
                )
            )
        )

        for y in range(chunk_h):
            y *= self.arc_h
            for x in range(chunk_w):
                x *= self.arc_w
                self.surface.blit(arc_surface, (x, y))

        self.rect.center = self.program.display.rect.center

    def update(self):
        shift = self.program.time.delta * self.SCROLL_SPEED

        if self.reversed:
            shift = -shift

        self.rect.y += shift

        if self.rect.y < -self.arc_h:
            self.rect.y += self.arc_h
        elif self.rect.y > 0:
            self.rect.y -= self.arc_h


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


class TitleScene(PixelScene):
    def __init__(self):
        super().__init__()

        self.add_children(
            ArcsChunk(ArcsChunk.BG, True), ArcsChunk(ArcsChunk.FG, True), Title()
        )
