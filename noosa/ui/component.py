from noosa.group import Group


class Component(Group):
    x = None
    y = None
    width = None
    height = None

    def __init__(self) -> None:
        super().__init__()
        self.create_children()

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.layout()

        return self

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.layout()

        return self

    def set_rect(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.layout()

        return self

    def inside(self, x, y):
        return (
            x >= self.x
            and y >= self.y
            and x < self.x + self.width
            and y < self.y + self.height
        )

    def fill(self, c):
        self.set_rect(c.x, c.y, c.width, c.height)

    def left(self):
        return self.x

    def right(self):
        return self.x + self.width

    def center_x(self):
        return self.x + self.width / 2

    def top(self):
        return self.y

    def bottom(self):
        return self.y + self.height

    def center_y(self):
        return self.y + self.height / 2

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def create_children(self):
        pass

    def layout(self):
        pass
