from gameengine.display import Display
from gameengine.engine import Engine
from gameengine.window import Window
from scenes.titlescene import TitleScene


def main():
    Window.set_title("Pixel Dungeon [Python]")
    Window.set_size((1280, 720))
    Display.update_display_from_window()
    scene = TitleScene()
    scene.create()
    Engine.set_scene(scene)
    Engine.set_framerate(60)
    Engine.start_loop()


if __name__ == "__main__":
    main()
