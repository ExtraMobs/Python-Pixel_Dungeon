from noosa.camera import Camera
from noosa.group import Group


class Scene(Group):
    def create(self):
        pass

    def camera(self):
        return Camera.main
