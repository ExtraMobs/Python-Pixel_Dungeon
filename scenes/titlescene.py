from gameengine.engine import Engine
from scenes.pixelscene import PixelScene


class TitleScene(PixelScene):
    def __init__(self):
        super().__init__()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if Engine.request_quit:
            Engine.system_exit()
