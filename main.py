import assets
from gameengine.core.program import Program
from gameengine.core.window import Window
from scenes.titlescene import TitleScene


class PixelDungeon(Program):
    def __init__(self):
        super().__init__(
            Window(
                title="Pixel Dungeon [Pygame]",
                size=(1280, 720),
            ),
            framerate=60,
        )

        assets.load_files()
        self.set_scene(TitleScene())


if __name__ == "__main__":
    PixelDungeon().start_loop()
