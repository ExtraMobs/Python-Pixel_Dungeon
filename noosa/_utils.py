class Array(list):
    def remove(self, __value):
        if contains := __value in self:
            super().remove(__value)
        return contains
