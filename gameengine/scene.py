class Scene:
    def __init__(self):
        super().__init__()
        self.children = []

    def add_child(self, *children):
        for child in children:
            self.children.append(child)
            child.parent = self

    def remove_child(self, *children):
        for child in children:
            self.children.remove(child)

    def update(self, *args, **kwargs):
        for child in list(self.children):
            child.update()

    def draw(self, surface, background):
        if background is not None:
            surface.blit(background, (0, 0))
        else:
            surface.fill((0, 0, 0))
        for child in self.children:
            if hasattr(child, "draw"):
                child.draw(surface)
