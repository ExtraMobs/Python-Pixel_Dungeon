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
    
    @priority.setter
    def priority(self, value):
        old_priority = self.priority
        if old_priority > value:
            old_priority+=1
        self.parent.children.insert(value, self)
        del self.parent.children[old_priority]