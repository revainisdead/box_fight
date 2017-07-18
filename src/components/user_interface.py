from typing import Any, Dict, List, Tuple

from collections import OrderedDict
from datetime import datetime
import time

import pygame as pg

from . import helpers

from .. import binds
from .. import const
from .. import setup
from .. import tools


menu_labels = {
    "play": "play",
    "load_game": "load game",
    "quit": "quit",
}


class MenuSelection(pg.sprite.Sprite):
    def __init__(self, x, y, name) -> None:
        super().__init__()

        self.sprite = setup.GFX["green_button01"]
        self.sprite_selected = setup.GFX["green_button00"]
        self.font = setup.FONTS["menu_kenvector_future_thin"]

        self.frames = self.load_sprites_from_sheet()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.state = const.Switch.OFF
        self.name = name
        self.selected = False


    def load_sprites_from_sheet(self) -> List[pg.Surface]:
        frames = []
        frames.append(helpers.get_image(0, 0, 190, 49, self.sprite, mult=const.MENU_MULT))
        frames.append(helpers.get_image(0, 0, 190, 49, self.sprite_selected, mult=const.MENU_MULT))
        return frames


    def update(self, selection) -> None:
        self.handle_state(selection)


    def handle_state(self, selection) -> None:
        if selection == self.name:
            self.selected = True
            frame_index = 1
            self.image = self.frames[frame_index]
        else:
            self.selected = False
            frame_index = 0
            self.image = self.frames[frame_index]


    def render_name(self, surface) -> None:
        if self.selected:
            text = self.font.render(menu_labels[self.name], True, const.SELECTED_GRAY)
        else:
            text = self.font.render(menu_labels[self.name], True, const.RESTING_GRAY)

        text_rect = text.get_rect(center=(setup.screen_size.get_width()/2, self.rect.y + self.rect.height/2))
        surface.blit(text, text_rect)


class Hud:
    def __init__(self) -> None:
        self.font = setup.FONTS["game_kenvector_future_thin"]

        self.x = setup.screen_size.get_width() - const.IMMUTABLE_HUD_X_OFFSET
        self.y = const.IMMUTABLE_HUD_Y
        self.clock = ""
        self.coords = ""


    def update_sizes(self) -> None:
        if setup.screen_size.changed():
            self.x = setup.screen_size.get_width() - const.IMMUTABLE_HUD_X_OFFSET
            self.y = const.IMMUTABLE_HUD_Y


    def update(self, screen: pg.Surface, game_info: Dict[str, Any], player: pg.sprite.Sprite, map_height: int) -> None:
        self.update_sizes()

        # Don't need game_info for clock but will still need it later.
        self.update_clock()
        self.update_coords(player.rect.x, player.rect.y, map_height)

        self.render_clock(screen)
        self.render_coords(screen)


    def update_clock(self) -> None:
        """Get the real time and save it as a string.
        Ex. 8:15 AM
        """
        time = datetime.now()
        time = time.strftime("%I:%M %p")

        # Remove the starting zero from the hour if it exists.
        if time.startswith("0"):
            time = time[1:]
        self.clock = time


    def update_coords(self, x: int, y: int, map_height: int) -> None:
        self.coords = "({}, {})".format(x, map_height - y)


    def render_clock(self, surface: pg.Surface) -> None:
        text = self.font.render(self.clock, True, const.WHITE)
        text_rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, text_rect)


    def render_coords(self, surface: pg.Surface) -> None:
        text = self.font.render(self.coords, True, const.SELECTED_GRAY)
        text_rect = text.get_rect(center=(self.x - const.IMMUTABLE_HUD_X_OFFSET*2, self.y))
        surface.blit(text, text_rect)


    def notification(self) -> None: pass
    def detect_item_change(self) -> None:
        # Compare stored game info inventory to new game info
        # and display a notification for a period of time that
        # displays the items gained? But also if the items gained
        # are within the period of time that the notification would
        # be displayed, then add it to the notifcation instead of
        # overwriting. Show Lumber + 1! and if another lumber is
        # gained within the time of the notification being displayed,
        # show Lumber + 2! and reset the display timer.
        pass
