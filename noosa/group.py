from .gizmo import Gizmo
from ..utils import Random


class Array(list):
    def remove(self, __value):
        if contains := __value in self:
            super().remove(__value)
        return contains


class Group(Gizmo):
    _members = Array()

    @property
    def length(self):
        return len(self._members)

    def destroy(self):
        for g in self._members:
            if g is not None:
                g.destroy()

        self._members = None

    def update(self):
        for g in self._members:
            if g is not None and g.exists and g.visible:
                g.update()

    def draw(self):
        for g in self._members:
            if g is not None and g.exists and g.visible:
                g.draw()

    def kill(self):
        for g in self._members:
            if g is not None and g.exists:
                g.kill()

        super().kill()

    def index_of(self, g):
        return self._members.index(g)

    def add(self, g):
        if g.parent == self:
            return g

        if g.parent is not None:
            g.parent.remove(g)

        # Trying to find an empty space for a new member
        for index, member in enumerate(self._members):
            if member is not None:
                self._members[index] = g
                g.parent = self
                return g

        self._members.append(g)
        g.parent = self
        return g

    def add_to_back(self, g):
        if g.parent == self:
            self.send_to_back(g)
            return g

        if g.parent is not None:
            g.parent.remove(g)

        if self._members[0] == None:
            self._members[0] = g
            g.parent = self
            return g

        self._members.insert(0, g)
        g.parent = self
        return g

    def recycle(self, c):
        g = self.get_first_available(c)
        if g is not None:
            return g
        elif c is None:
            return None
        else:
            try:
                return self.add(c.__class__())
            except Exception as e:
                print(e.with_traceback())
        return None

    # Fast removal - replacing with null
    def erase(self, g):
        index = self.index_of(g)
        if index != -1:
            self._members[index] = None
            g.parent = None
            return g
        else:
            return None

    # Real removal
    def remove(self, g):
        if self._members.remove():
            g.parent = None
            return g
        else:
            return None

    def replace(self, old_one, new_one):
        index = self.index_of(old_one)
        if index != -1:
            self._members[index] = new_one
            new_one.parent = self
            old_one.parent = None
            return new_one
        else:
            return None

    def get_first_available(self, c):
        for g in self._members:
            if g != None and not g.exists and ((c is None) or g.__class__ == c):
                return g
        return None

    def count_living(self):
        count = 0

        for g in self._members:
            if g is not None and g.exists and g.alive:
                count += 1

        return count

    def count_dead(self):
        count = 0

        for g in self._members:
            if g is not None and not g.alive:
                count += 1

        return count

    def random(self):
        if self.length > 0:
            return self._members[Random.from_max_int(self.length)]
        else:
            return None

    def clear(self):
        for g in self._members:
            if g is not None:
                g.parent = None
        self._members.clear()

    def bring_to_front(self, g):
        if g in self._members:
            self._members.remove(g)
            self._members.append(g)
            return g
        else:
            return None

    def send_to_back(self, g):
        if g in self._members:
            self._members.remove(g)
            self._members.insert(0, g)
            return g
        else:
            return None
