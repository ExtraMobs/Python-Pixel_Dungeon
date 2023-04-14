import random


class Random:
    @staticmethod
    def float():
        return random.random()

    @staticmethod
    def from_max_float(a):
        return a * random.random()

    @staticmethod
    def from_range_float(_min, _max):
        return _min + random.random() * (_max - _min)

    @staticmethod
    def from_max_int(a):
        return int(a * random.random())
