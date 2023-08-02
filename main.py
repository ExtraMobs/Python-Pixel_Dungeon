from gameengine.core.program import Program
from gameengine.core.window import Window


class PixelDungeon(Program):
    def __init__(self):
        super().__init__(
            Window(
                title="Pixel Dungeon [Pygame]",
                size=(1280, 720),
            )
        )


if __name__ == "__main__":
    PixelDungeon().start_loop()
