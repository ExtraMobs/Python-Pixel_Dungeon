from assets import Assets
from gameengine.display import Display
from gameengine.engine import Engine
from gameengine.window import Window
from info import Info
from scenes.titlescene import TitleScene


def init():
    Info.init()
    Assets.init()


def main():
    Window.set_title("Pixel Dungeon [Python]")
    Window.set_size((1280, 720))
    Display.update_display_from_window()

    init()

    Engine.set_scene(TitleScene())
    Engine.start_loop()


if __name__ == "__main__":
    main()
