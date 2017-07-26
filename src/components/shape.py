from typing import Any, Tuple

import random


class Cube:
    verts = (-1, 1, 1), (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, -1), (1, 1, -1), (1, -1, -1), (-1, -1, -1)
    faces = (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)
    colors = (255, 0, 0), (255, 128, 0), (255, 255, 0), (255, 255, 255), (0, 0, 255), (0, 255, 0)

    def __init__(self, pos=(0, 0, 0)):
        x, y, z = pos
        self.verts = [(x+X/2, y+Y/2, z+Z/2) for X, Y, Z in self.verts]

        # Each tint application lightens slightly
        tint_factor = 0.15
        self.colors = self.randomize_color(tint_factor)


    def randomize_color(self, tint_factor: float) -> Tuple[Tuple[int, int, int], ...]:
        """ Get a random color and then tint that color for each side. """
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        colors = []
        for _ in range(6):
            # Change tint for each side
            r = r + (255 - r) * tint_factor
            g = g + (255 - g) * tint_factor
            b = b + (255 - b) * tint_factor
            colors.append((r, g, b))

        return tuple(colors)



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
