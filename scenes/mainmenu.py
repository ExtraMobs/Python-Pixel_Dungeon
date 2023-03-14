from gameengine import Engine, Scene
from gameobjets import Archs


class MainMenu(Scene):
    def __init__(self):
        super().__init__()

        self.add_child(Archs())

    def process(self, *args, **kwargs):
        super().process(*args, **kwargs)
        if Engine.request_quit:
            Engine.system_exit()
