class StandardObject:
    def __init__(self) -> None:
        self.parent = None

    def process(self, *args, **kwargs):
        pass

    @property
    def priority(self):
        try:
            return self.parent.children.index(self)
        except IndexError:
            return -1
