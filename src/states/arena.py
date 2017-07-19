from typing import Any, Dict, Tuple

import time
import random

import pygame as pg

from .. import binds
from .. import const
from .. import control
from .. import setup
from .. import tools

from .. components import camera, player, mapdef, user_interface, util


class Arena(control.State):
    def __init__(self) -> None:
        super().__init__()
        self.collidable_group = pg.sprite.Group()
        self.setup_map()


    def startup(self, game_info: Dict[str, Any]) -> None:
        self.game_info = game_info
        self.state = const.MainState.arena

        self.setup_player()
        self.setup_hud()


    def setup_map(self) -> None:
        self.mapdef = mapdef.MapDef()
        self.map_surf = self.mapdef.update(0)

        self.entire_area = pg.Surface((800, 800)).convert()
        #self.entire_area_rect = self.entire_area.get_rect()


    def setup_hud(self) -> None:
        self.hud = user_interface.Hud()


    def setup_player(self) -> None:
        self.player = player.Player(0, 0) # TODO: Start player somewhere else
        self.player_group = pg.sprite.Group(self.player)


    def update(self, surface: pg.Surface, current_time: int, dt: float) -> None:
        self.game_info["current_time"] = current_time

        self.update_sizes()
        self.update_map(dt)
        self.update_sprites()
        self.handle_states(dt)
        self.blit_images(surface)

        # Draw the hud to the screen over everything else.
        # Similar to Game UI but the hud needs access to game_info.
        self.hud.update(surface, self.game_info, self.player)


    def handle_states(self, dt: float) -> None:
        if binds.INPUT.pressed("escape"):
            self.quit = True
        else:
            self.move_camera(dt)


    def move_camera(self, dt: float) -> None:
        camera.CAM.update(dt, binds.INPUT.mouse_pos())


    def update_sizes(self) -> None:
        if setup.screen_size.changed():
            # Start new camera at the same position as before.
            #self.camera = pg.Rect((self.camera.x, self.camera.y), (setup.screen_size.get_width(), setup.screen_size.get_height()))
            pass


    def update_map(self, dt: float) -> None:
        # Draw black background for now.
        self.map_surf.fill(const.BLACK)

        self.map_surf = self.mapdef.update(dt)

        if setup.map_size.changed():
            self.setup_player()


    def update_sprites(self) -> None:
        self.player_group.update(self.game_info["current_time"], self.collidable_group)



    def blit_images(self, surface: pg.Surface) -> None:
        # This is responsible for showing only a certain area
        # of the tilemap surface, the area shown is the area of the camera.
        #self.entire_area.blit(self.map_surf, self.camera, self.camera)
        self.entire_area.blit(self.map_surf, (0, 0))

        self.player_group.draw(self.entire_area)

        # Finally, draw everything to the screen surface.
        #surface.blit(self.entire_area, (0, 0), self.camera)
        surface.blit(self.entire_area, (0, 0))
