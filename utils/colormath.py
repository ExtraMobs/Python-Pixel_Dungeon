from utils.random import Random


class ColorMath:
    @staticmethod
    def interpolate_a(A, B, p):
        if p <= 0:
            return A
        elif p >= 1:
            return B

        ra = A >> 16
        ga = (A >> 8) & 0xFF
        ba = A & 0xFF

        rb = B >> 16
        gb = (B >> 8) & 0xFF
        bb = B & 0xFF

        p1 = 1 - p

        r = int(p1 * ra + p * rb)
        g = int(p1 * ga + p * gb)
        b = int(p1 * ba + p * bb)

        return (r << 16) + (g << 8) + b

    @classmethod
    def interpolate_b(cls, p, *colors):
        if p <= 0:
            return colors[0]
        elif p >= 1:
            return colors[len(colors) - 1]
        segment = int(len(colors) * p)
        return cls.interpolate(
            colors[segment], colors[segment + 1], (p * (colors.length - 1)) % 1
        )

    @classmethod
    def random(cls, a, b):
        return cls.interpolate_a(a, b, Random.float())
