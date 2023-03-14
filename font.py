from gameengine import Resources
import os


class Font:
    FONT_1X = []
    FONT_2X = []
    FONT_3X = []
    FONT_15X = []
    FONT_25X = []

    @classmethod
    def prepare_fonts(cls):
        Resources.Surface.add_from_file(os.path.abspath("/assets/font1x.png"))
