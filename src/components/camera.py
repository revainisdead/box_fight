from typing import Optional, Tuple

import math

import pygame as pg

from .. import binds


class Cam:
    def __init__(self, pos=(0,0,0), rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)


    def update(self, dt, point: Optional[Tuple[int, int]]):
        if point is not None:
            x, y = event.rel
            x/=(w/2); y/=(w/2)
            self.rot[0] += y
            self.rot[1] += x

        s = dt * 10

        if binds.INPUT.held("up"):
            self.pos[1] += s
        if binds.INPUT.held("down"):
            self.pos[1] -= s

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


CAM = Cam((0, 0, -5))