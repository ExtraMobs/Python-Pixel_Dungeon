from gameengine.engine import Engine


class GameMath:
    @staticmethod
    def speed(speed, acc):
        if acc != 0:
            speed += acc * Engine.deltatime
        return speed
