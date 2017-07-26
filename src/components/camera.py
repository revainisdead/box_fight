from typing import Optional, Tuple

import math

import pygame as pg

from .. import binds, setup


class Cam:
    def __init__(self, pos=(0,0,0), rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)


    def update_rot(self, dpos: Tuple[int, int]) -> None:
        x, y = dpos
        # Calculate how far the mouse moved compared to the size
        # of the screen.
        x/=(setup.screen_size.get_width()/2)
        y/=(setup.screen_size.get_width()/2)

        # Add y to x and x to y.
        self.rot[0] += y
        self.rot[1] += x


    def update(self, dt, dpos: Optional[Tuple[int, int]]):
        """
        dt: delta time
        dpos: delta position
        """
        if dpos is not None:
            self.update_rot(dpos)

        s = dt * 10

        if binds.INPUT.held("up"):
            #self.pos[1] += s
            self.pos[1] -= 6
        if binds.INPUT.held("down"):
            self.pos[1] += s

        #if key[pygame.K_w]: self.pos[2] += s
        #if key[pygame.K_s]: self.pos[2] -= s
        #if key[pygame.K_a]: self.pos[0] += s
        #if key[pygame.K_d]: self.pos[0] -= s

        x = s*math.sin(self.rot[1])
        y = s*math.cos(self.rot[1])

        if binds.INPUT.held("forward"):
            self.pos[0] += x
            self.pos[2] += y
        if binds.INPUT.held("back"):
            self.pos[0] -= x
            self.pos[2] -= y
        if binds.INPUT.held("left"):
            self.pos[0] -= y
            self.pos[2] += x
        if binds.INPUT.held("right"):
            self.pos[0] += y
            self.pos[2] -= x

        # TODO: Gravity hack, move later.
        if self.pos[1] < 0:
            self.pos[1] += 2


CAM = Cam((0, 0, -5))
