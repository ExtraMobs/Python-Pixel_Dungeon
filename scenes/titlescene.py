import enum
import math

from assets import Assets
from gameengine import resources
from gameengine.nodes.basenode import BaseNode
from gameengine.nodes.basescene import BaseScene
from gameengine.nodes.graphicnode import GraphicNode


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


class PixelScene(BaseScene):
    MIN_WIDTH_P = 128
    MIN_HEIGHT_P = 224

    MIN_WIDTH_L = 224
    MIN_HEIGHT_L = 160

    default_zoom = 0

    window_density = 1  # temp

    def __init__(self):
        super().__init__()

        min_width = min_height = None
        if self.program.display.is_landscape:
            min_width = self.MIN_WIDTH_L
            min_height = self.MIN_HEIGHT_L
        else:
            min_width = self.MIN_WIDTH_P
            min_height = self.MIN_HEIGHT_P

        self.default_zoom = math.ceil(self.window_density * 2.5)
        while (
            (self.program.display.width / self.default_zoom < min_width)
            or (self.program.display.height / self.default_zoom < min_height)
        ) and self.default_zoom > 1:
            self.default_zoom -= 1

        self.min_zoom = 1
        self.max_zoom = self.default_zoom * 2

        self.program.display.set_scale(self.default_zoom)


class TitleScene(PixelScene):
    def __init__(self):
        super().__init__()

        self.add_children(ArcsChunk(ArcsChunk.BG, True), ArcsChunk(ArcsChunk.FG, True))
