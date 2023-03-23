class Gizmo:
    exists = None
    alive = None
    active = None
    visible = None

    parent = None

    camera = None

    def __init__(self) -> None:
        super().__init__()
        self.exists = True
        self.alive = True
        self.active = True
        self.visible = True

    def destroy(self):
        self.parent.remove_child(self)

    def update(self):
        ...

    def draw(self):
        ...

    def kill(self):
        self.alive = False
        self.exists = False

    # Not exactly opposite to "kill" method
    def revive(self):
        self.alive = True
        self.exists = True

    def get_camera(self):
        if self.camera != None:
            return self.camera
        elif self.parent is not None:
            return self.parent.camera
        else:
            return None

    def is_visible(self):
        if self.parent is None:
            return self.visible
        else:
            return self.visible and self.parent.is_visible()

    def is_active(self):
        if self.parent is None:
            return self.active
        else:
            return self.active and self.parent.active

    def kill_and_erase(self):
        self.kill()
        if self.parent is not None:
            self.parent.erase(self)

    def remove(self):
        if self.parent is not None:
            self.parent.remove(self)
