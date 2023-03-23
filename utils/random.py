import random


class Random:
    @staticmethod
    def from_max_float(a):
        return a * random.random()

    @staticmethod
    def from_max_int(a):
        return int(a * random.random())
