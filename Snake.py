import pygame as pg
import random
from direction_pattern import direction_pattern


class Snake:
    def __init__(self):
        self.width = 20
        self.height = 20

        self.dir = 'w'

        self.head_pos = (random.randrange(30, 300), random.randrange(30, 300))
        self.head_rect = None

        self.number_tails = 0

        self.color = "purple"

        self.tails = []
        self.tail_rects = []
        self.tails.append(self.head_pos)

        self.speed = 10

    def lengthen_tail(self):
        self.tails.append((self.tails[-1][0], self.tails[-1][1] - self.height))

    def move(self):
        self.head_pos = (self.head_pos[0] + direction_pattern[self.dir][0],
                         self.head_pos[1] + direction_pattern[self.dir][1])

        self.tails.pop()
        self.tails.insert(0, self.head_pos)

    def crossing_fruit(self, fruit_rect):
        return True if self.head_rect.colliderect(fruit_rect) else False

    def body_collision(self):
        for i in self.tail_rects:
            if self.head_rect.colliderect(i):
                return True

        return False

    def draw(self, screen):
        self.head_rect = pg.draw.rect(screen, self.color, (*self.tails[0], self.width, self.height))
        self.tail_rects = []
        for i in range(1, len(self.tails)):
            self.tail_rects.append(pg.draw.rect(screen, self.color, (*self.tails[i], self.width, self.height)))
