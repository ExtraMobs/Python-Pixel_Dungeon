from gameengine import Engine, Scene
from gameobjets import Archs, Title, Signs, Flame, Fireball


class TitleScene(Scene):
    def __init__(self):
        super().__init__()

        self.add_child(
            Archs(),
            title := Title(),
            signs := Signs(),
            left_torch := Fireball(),
            left_flame := Flame(),
            right_torch := Fireball(),
            right_flame := Flame(),
        )
        left_torch.position.x = title.position.x
        left_torch.position.y = title.position.y
        left_flame.position = left_torch.position
        right_torch.position.x = (
            title.position.x + title.rect.width - right_torch.rect.width
        )
        right_torch.position.y = title.position.y
        right_flame.position = right_torch.position
        signs.position = title.position

    def process(self, *args, **kwargs):
        super().process(*args, **kwargs)
        if Engine.request_quit:
            Engine.system_exit()
