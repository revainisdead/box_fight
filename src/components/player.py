import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()

        self.x = x
        self.y = y

    def update(self, time: float, collidable_group: pg.sprite.Group) -> None:
        self.handle_state()


    def handle_state(self) -> None:
        pass


