import math
from assets import Assets
from gameengine import resources
from gameengine.nodes.basenode import BaseNode
from gameengine.nodes.basescene import BaseScene
from gameengine.nodes.graphicnode import GraphicNode


class Arc(GraphicNode):
    BG = "1"
    FG = "2"

    def __init__(self, arch_type, _scroll_speed=None, _reversed=False):
        if arch_type == self.BG:
            arch_id = Assets.ARCS_BG
        elif arch_type == self.FG:
            arch_id = Assets.ARCS_FG
        else:
            raise Exception("Invalid 'arch_type' parameter.")

        super().__init__(resources.surface.get(arch_id))

        self.scroll_speed = _scroll_speed
        self.reversed = _reversed

        self.__shift_count = 0

    def update(self):
        if not self.scroll_speed is None:
            shift = self.program.time.delta * self.scroll_speed

            if self.reversed:
                shift = -shift

            self.rect.y += shift

            self.__shift_count += shift
            if self.__shift_count < -self.rect.h:
                self.rect.y += self.rect.h
                self.__shift_count += self.rect.h


class ArcsChunk(BaseNode):
    SCROLL_SPEED = 20

    def __init__(self, arch_type, reversed):
        if arch_type == Arc.FG:
            self.SCROLL_SPEED *= 2
        self.base_arc_rect = Arc(arch_type, self.SCROLL_SPEED, reversed).rect
        super().__init__()

        x_diff = self.program.display.width % self.base_arc_rect.w
        y_diff = self.program.display.height % self.base_arc_rect.h

        for y in range(
            math.ceil(self.program.display.height / self.base_arc_rect.h) + 1
        ):
            y *= self.base_arc_rect.h
            y += y_diff
            for x in range(
                math.ceil(self.program.display.width / self.base_arc_rect.w) + 1
            ):
                x *= self.base_arc_rect.w
                x += x_diff
                new_arch = Arc(arch_type, self.SCROLL_SPEED, reversed)
                new_arch.rect.topleft = (x, y)
                self.add_children(new_arch)


class TitleScene(BaseScene):
    def __init__(self):
        super().__init__(ArcsChunk(Arc.BG, True), ArcsChunk(Arc.FG, True))
