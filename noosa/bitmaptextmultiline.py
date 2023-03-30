import pygame
from noosa.bitmaptext import BitmapText


class BitmapTextMultiline(BitmapText):
    max_width = 2**32 - 1

    PARAGRAPH = "\n"
    WORD = " "

    space_size = None

    n_lines = 0

    mask = []

    def __init__(self, text=None, font=None):
        super().__init__(text, font)
        self.space_size = font.get_width(font.get(" "))

    def get_word_metrics(self, word, metrics):
        w = h = 0

        for char in word:
            rect = self.font.get(char)
            w += self.font.get_width(rect) + (self.font.tracking if w > 0 else 0)
            h = max(h, self.font.get_height())

        metrics.update(w, h)

    def measure(self):
        # This object controls lines breaking
        writer = BitmapTextMultiline.SymbolWriter()

        # Word size
        metrics = pygame.Vector2()

        paragraphs = self.text.split(self.PARAGRAPH)

        # Current character (used in masking)
        pos = 0

        for paragraph in paragraphs:
            words = paragraph.split(self.WORD)
            for j, word in enumerate(words):
                if j > 0:
                    writer.add_space(self.space_size, self)
                if len(word) == 0:
                    continue

                self.get_word_metrics(word, metrics)
                writer.add_symbol(metrics.x, metrics.y, self)
            writer.new_line(0, self.font.line_height)

        self.width = writer.width
        self.height = writer.height

        self.n_lines = writer.get_n_lines()

    def base_line(self):
        return (
            self.height - self.font.line_height + self.font.base_line
        ) * self.scale.y

    class SymbolWriter:
        width = 0
        height = 0

        n_lines = 0

        line_width = 0
        line_height = 0

        x = 0
        y = 0

        def add_symbol(self, w, h, bitmap_text):
            font = bitmap_text.font
            scale = bitmap_text.scale
            if (
                self.line_width > 0
                and self.line_width + font.tracking + w > self.max_width / scale.x
            ):
                self.new_line(w, h)
            else:
                self.x = self.line_width

            self.line_width += (font.tracking if self.line_width else 0) + w
            if h > self.line_height:
                self.line_height = h

        def add_space(self, w, bitmap_text):
            font = bitmap_text.font
            max_width = bitmap_text.max_width
            scale = bitmap_text.scale
            if (
                self.line_width > 0
                and self.line_width + font.tracking + w > max_width / scale.x
            ):
                self.new_line(0, 0)
            else:
                self.x = self.line_width
                self.line_width += (font.tracking if self.line_width > 0 else 0) + w

        def new_line(self, w, h):
            self.height += self.line_height
            if self.width < self.line_width:
                self.width = self.line_width

            self.line_width = w
            self.line_height = h

            self.x = 0
            self.y = self.height

            self.n_lines += 1

        def get_n_lines(self):
            return self.n_lines if self.x == 0 else self.n_lines + 1
