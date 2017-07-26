from typing import Any, Tuple

import random


class Cube:
    verts = (-1, 1, 1), (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, -1), (1, 1, -1), (1, -1, -1), (-1, -1, -1)
    faces = (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)
    colors = (255, 0, 0), (255, 128, 0), (255, 255, 0), (255, 255, 255), (0, 0, 255), (0, 255, 0)

    def __init__(self, pos=(0, 0, 0)):
        x, y, z = pos
        self.verts = [(x+X/2, y+Y/2, z+Z/2) for X, Y, Z in self.verts]
        self.colors = self.randomize_color()


    def randomize_color(self) -> Tuple[Tuple[int, int, int], ...]:
        for _ in range(3):
            c = ((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),)
        return c * 6




class Floor(Cube):
    """
    verts = (-v_size, v_size, 1), (v_size, v_size, 1), \
            (v_size, -v_size, 1), (-v_size, -v_size, 1), \
            (-v_size, v_size, -1), (v_size, v_size, -1), \
            (v_size, -v_size, -1), (-v_size, -v_size, -1)
    """
    v_size = 20

    # Positive z and then Negative z
    verts = (-v_size, 1, v_size), (v_size, 1, v_size), \
            (v_size, -1, v_size), (-v_size, -1, v_size), \
            (-v_size, 1, -v_size), (v_size, 1, -v_size), \
            (v_size, -1, -v_size), (-v_size, -1, -v_size)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class Wall: pass
