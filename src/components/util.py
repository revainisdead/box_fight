import pygame as pg

from .. import const


class Collidable(pg.sprite.Sprite):
    """Create a collidable rect
    This sprite itself has nothing about it that prevents movement through it.
    But if the Collidable rect exists ensure that it can't be moved through.
    """
    def __init__(self, x: int, y: int, width: int=const.TILE_SIZE, height: int=const.TILE_SIZE) -> None:
        super().__init__()

        self.image = pg.Surface((width, height)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
