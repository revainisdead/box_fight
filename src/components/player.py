import pygame as pg

from . import helpers

from .. import setup


class Player(pg.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()


        self.x = x
        self.y = y

        self.sprite = setup.GFX["green_button01"]
        self.image = helpers.get_image(0, 0, 190, 49, self.sprite, mult=1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self, time: float, collidable_group: pg.sprite.Group) -> None:
        self.handle_state()


    def handle_state(self) -> None:
        pass


