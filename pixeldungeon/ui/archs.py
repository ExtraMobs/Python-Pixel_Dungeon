from assets import Assets
from gameengine.engine import Engine
from noosa.skinnedblock import SkinnedBlock
from noosa.ui.component import Component
from utils.resourcecache import ResourceCache


class Archs(Component):
    SCROLL_SPEED = 20
    arcs_bg = None
    arcs_fg = None

    offs_b = 0
    offs_f = 0

    reversed_ = False

    def create_children(self):
        self.arcs_bg = SkinnedBlock(1, 1, ResourceCache.get(Assets.ARCS_BG))
        self.arcs_bg.auto_adjust = True
        self.add(self.arcs_bg)

        self.arcs_fg = SkinnedBlock(1, 1, ResourceCache.get(Assets.ARCS_FG))
        self.arcs_fg.auto_adjust = True
        self.add(self.arcs_fg)

    def layout(self):
        self.arcs_bg.set_size(self.width, self.height)
        width = self.arcs_bg.origin_texture.get_width()
        self.arcs_bg.offset(width / 4 - (self.width % width) / 2, 0)

        self.arcs_fg.set_size(self.width, self.height)
        width = self.arcs_fg.origin_texture.get_width()
        self.arcs_fg.offset(width / 4 - (self.width % width) / 2, 0)

    def update(self):
        super().update()

        shift = Engine.deltatime * self.SCROLL_SPEED
        if self.reversed_:
            shift = -shift

        self.arcs_bg.offset(0, shift)
        self.arcs_fg.offset(0, shift * 2)
