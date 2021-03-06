from typing import Any, Dict, Tuple

import os

import pygame as pg

from . import const
from . import tools


GFX =   {} # type: Dict[str, pg.Surface]
FONTS = {} # type: Dict[str, pg.font.Font]
SFX =   {} # type: Dict[str, pg.mixer.Sound]

screen_size = None # type: ScreenSize
map_size = None # type: MapSize


class ScreenSize:
    def __init__(self):
        self.__width, self.__height = const.DEFAULT_SCREEN_SIZE
        self.__changed = False


    def __resize(self, width: int, height: int) -> None:
        if width != self.__width and height != self.__height:
            self.__width = width
            self.__height = height
            self.__changed = True
        else:
            self.__changed = False


    def get_size(self) -> Tuple[int, int]:
        return self.__width, self.__height


    def get_width(self) -> int:
        return self.__width


    def get_height(self) -> int:
        return self.__height


    def changed(self) -> bool:
        """This will spit out true for only one frame when the size changes."""
        return self.__changed


    def update(self, width: float, height: float) -> None:
        self.__resize(int(round(width)), int(round(height)))

        if self.__changed:
            pg.display.set_mode((self.__width, self.__height), pg.RESIZABLE)


class MapSize:
    """ Map size acts basically like screen size. Because:
       - It is always based off of the default screen size.
       - It changes depending on the biome.
       - It needs to be accessible everywhere.
    """
    def __init__(self) -> None:
        self.__biome = None
        #self.__width = 0
        #self.__height = 0
        self.__changed = False

        self.__resize_map(const.Biome.FARMLAND)

        # Grid size is based off of Map size. Store that too.
        #self.__grid_width = 0
        #self.__grid_height = 0
        self.__resize_grid()


    def __resize_map(self, biome: const.Biome) -> None:
        """Size the map based on biome. Round to the nearest tile size."""
        if self.__biome != biome:
            self.__biome = biome
            self.__width = round(const.DEFAULT_SCREEN_WIDTH * const.map_mult[self.__biome] / const.TILE_SIZE) * const.TILE_SIZE
            self.__height = round(const.DEFAULT_SCREEN_HEIGHT * const.map_mult[self.__biome] / const.TILE_SIZE) * const.TILE_SIZE
            self.__changed = True
        else:
            self.__changed = False


    def __resize_grid(self) -> None:
        if self.__changed:
            # Since the map size gets updated first, if the map size changes,
            # this needs changing as well.
            self.__grid_width = int(round(self.__width / const.TILE_SIZE))
            self.__grid_height = int(round(self.__height / const.TILE_SIZE))


    def get_width(self) -> int:
        return self.__width


    def get_height(self) -> int:
        return self.__height


    def get_grid_width(self) -> int:
        return self.__grid_width


    def get_grid_height(self) -> int:
        return self.__grid_height


    def changed(self) -> bool:
        """Determine whether the map size and grid size has changed.

        If map size changed, we can assume grid size changed as well.
        And changed only lasts for one frame for both.
        """
        return self.__changed


    def get_biome(self) -> const.Biome:
        return self.__biome


    def update(self, biome: const.Biome) -> None:
        """ Don't let callers resize. Resize based on biome only."""
        self.__resize_map(biome)
        self.__resize_grid()


def start():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pg.init()
    pg.font.init()

    # Mouse
    pg.mouse.set_visible(0)
    pg.event.set_grab(1)

    # Initialize screen
    _ = pg.display.set_mode(const.DEFAULT_SCREEN_SIZE, pg.RESIZABLE)

    global GFX
    GFX = tools.load_gfx(os.path.join("data", "graphics"))
    global FONTS
    FONTS = tools.load_fonts(os.path.join("data", "fonts"))
    global SFX
    #SFX = tools.load_sfx(os.path.join("data", "sounds"))

    global screen_size
    screen_size = ScreenSize()
    global map_size
    map_size = MapSize()
