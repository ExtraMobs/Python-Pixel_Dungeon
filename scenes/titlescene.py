import pygame
from gameengine import Engine, Scene
from gameobjetcs import Archs, Title, Signs, Flame, Fireball


class TitleScene(Scene):
    def __init__(self):
        super().__init__()
        title = Title()
        signs = Signs()
        left_torch = Fireball()
        left_torch.position = pygame.Vector2(title.position)
        right_torch = Fireball()
        right_torch.position.x = (
            title.position.x + title.rect.width - right_torch.rect.width
        )
        right_torch.position.y = title.position.y
        signs.position = title.position
        self.add_child(
            Archs(),
            title,
            signs,
            left_torch,
            Flame(left_torch.position),
            right_torch,
            Flame(right_torch.position),
        )

    def process(self, *args, **kwargs):
        super().process(*args, **kwargs)
        if Engine.request_quit:
            Engine.system_exit()
