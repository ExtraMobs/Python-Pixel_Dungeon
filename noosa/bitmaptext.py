import pygame
from gameengine.display import Display
from noosa.texturefilm import TextureFilm
from noosa.visual import Visual


class BitmapText(Visual):
    text = None
    font = None

    real_length = None

    def __init__(self, text=None, font=None) -> None:
        if (text, font) == (None, None):
            self.__init__("", None)
        elif text is None:
            self.__init__("", font)
        else:
            super().__init__(0, 0, 0, 0)
            self.text = text
            self.font = font

    def destroy(self):
        self.text = None
        self.font = None
        super().destroy()

    def draw(self):
        if self.dirty:
            Display.surface.blit(self.__origin_texture, (self.x, self.y))

    class Font(TextureFilm):
        LATIN_UPPER = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        LATIN_FULL = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\u007F"

        texture = None

        tracking = 0
        base_line = None

        auto_uppercase = False

        line_height = None

        def __init__(self, texture):
            super().__init__(texture)
            self.texture = texture

        def split_by(self, bitmap, height, color, chars):
            color = pygame.Color(color)
            self.auto_uppercase = chars == self.LATIN_UPPER

            width = bitmap.get_width()
            v_height = height / bitmap.get_height()

            for pos in range(width):
                for j in range(height):
                    break_space_measuring = bitmap.get_at((pos, j)) != color
                if break_space_measuring:
                    break

            self.add(" ", pygame.FRect(0, 0, pos / width, v_height))
            for ch in chars:
                if ch == " ":
                    continue
                else:
                    separator = pos
                    found = False
                    break_while = False

                    def do_while(separator, found, break_while):
                        if separator >= width:
                            break_while = True
                        found = True
                        if not break_while:
                            for j in range(height):
                                if bitmap.get_at((separator, j)) != color:
                                    found = False
                                    break
                        return found, break_while

                    separator += 1
                    do_while(separator, found, break_while)
                    while not found and not break_while:
                        separator += 1
                        found, break_while = do_while(separator, found, break_while)
                    self.add(ch, rect := pygame.FRect(pos / width, 0, 0, v_height))
                    rect.right = separator / width
                    pos = separator + 1

        @classmethod
        def color_marked(cls, bmp, height, color, chars):
            if height is None:
                height = bmp.get_height()
            font = cls(bmp)
            font.split_by(bmp, height, color, chars)
            return font
