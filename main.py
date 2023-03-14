import scenes
from assets import Assets
from gameengine import Display, Engine, Window
from info import Info


def init():
    Info.init()
    Assets.init()


def main():
    Window.set_title("Pixel Dungeon [Python]")
    Window.set_size((1280, 720))
    Display.update_display_from_window()

    init()

    Engine.set_scene(scenes.MainMenu())
    Engine.start_loop()


if __name__ == "__main__":
    main()
