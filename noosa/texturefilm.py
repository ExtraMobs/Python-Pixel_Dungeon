import pygame


class TextureFilm:
    FULL = pygame.FRect(0, 0, 1, 1)

    tex_width = None
    tex_height = None

    frames = {}

    def __init__(self, texture, width=None, height=None, patch=None):
        self.tex_width = texture.get_width()
        self.tex_width = texture.get_height()
        if (width, height) == (None, None):
            self.add(None, self.FULL)
        else:
            uw = int(width / self.tex_width)
            vh = int(height / self.tex_height)
            if patch is None:
                cols = self.tex_width / width
                rows = self.tex_height / height
            else:
                cols = int(self.get_width(patch) / width)
                rows = int(self.get_height(patch) / height)

            for i in range(rows):
                for j in range(cols):
                    rect = pygame.FRect(j * uw, i * vh, (j + 1) * uw, (i + 1) * vh)
                    if patch is not None:
                        rect.move_ip(patch.left, patch.top)
                    self.add(i * cols + j, rect)

    def add(self, id, rect):
        self.frames[id] = rect

    def get(self, id):
        return self.frames[id]

    def get_width(self, frame):
        return frame.width * self.tex_width

    def get_height(self, frame):
        return frame.height * self.tex_height

    @classmethod
    def from_texture(cls, texture, width, height=None):
        if height is None:
            return cls(texture, width, texture.get_height())
        else:
            return cls(texture, width, height)

    @classmethod
    def from_atlas(cls, atlas, key, width, height):
        return cls(atlas, width, height, atlas.get(key))
