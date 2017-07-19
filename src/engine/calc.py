from typing import Tuple

import math


def rotate2d(pos: Tuple[int, int], rad: int) -> Tuple[float, float]:
    x, y = pos
    s = math.sin(rad)
    c = math.cos(rad)

    # Math step written out
    #x = x*math.cos(rad) - y*math.sin(rad)
    #y = y*math.cos(rad) + x*math.sin(rad)
    return x*c - y*s, y*c + x*s
