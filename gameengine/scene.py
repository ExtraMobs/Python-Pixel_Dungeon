from .objects import GraphicObject


class Scene:
    def __init__(self):
        super().__init__()
        self.children = []

    def add_child(self, *children):
        for child in children:
            self.children.append(child)
            child.parent = self

    def process(self, *args, **kwargs):
        for child in self.children:
            child.process()

    def render(self, surface, background):
        if background is not None:
            surface.blit(background, (0, 0))
        else:
            surface.fill((0, 0, 0))
        for child in self.children:
            if isinstance(child, GraphicObject):
                child.render(surface)
