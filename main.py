import pygame as pg
import neat
from Snake import Snake
from Fruit import Fruit

WIDTH = 600
HEIGHT = 600

BG = (34, 29, 29)

clock = pg.time.Clock()

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))


def draw_window(screen, snake, fruit):

    screen.fill(BG)

    fruit.draw(screen)
    snake.draw(screen)

    pg.display.update()


def check_direction(keys, x_change, y_change):
    if keys[pg.K_w]:
        x_change = 0
        y_change = -5
    elif keys[pg.K_d]:
        x_change = 5
        y_change = 0
    elif keys[pg.K_s]:
        x_change = 0
        y_change = 5
    elif keys[pg.K_a]:
        x_change = -5
        y_change = 0

    return x_change, y_change


def check_out_boarder(snake):
    if 0 > snake.head_pos[0] or snake.head_pos[0] + snake.width > WIDTH or 0 > snake.head_pos[1] \
            or snake.head_pos[1] + snake.height > HEIGHT:
        return False
    return True


def main():
    snake = Snake()
    fruit = Fruit(WIDTH, HEIGHT)
    running = True
    x_change = 0
    y_change = -5
    while running:
        draw_window(screen, snake, fruit)

        clock.tick(30)
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        x_change, y_change = check_direction(keys, x_change, y_change)

        if snake.crossing_fruit(fruit.fruit):
            fruit.new_pos()
            snake.lengthen_tail()

        snake.body_collision()

        running = check_out_boarder(snake)

        snake.move(x_change, y_change)


if __name__ == "__main__":
    main()
