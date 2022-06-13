import pygame as pg
import random


class Fruit:
    def __init__(self, win_width, win_height):

        self.win_width = win_width - 200
        self.win_height = win_height - 200

        self.width = 20
        self.height = 20

        self.color = "lightgreen"

        self.pos = (random.randrange(0, self.win_width), random.randrange(0, self.win_height))
        # self.pos = (300, 300)

    def new_pos(self):
        self.pos = (random.randrange(0, self.win_width), random.randrange(0, self.win_height))

    def draw(self, screen):
        self.fruit = pg.draw.rect(screen, self.color, (*self.pos, self.width, self.height))

