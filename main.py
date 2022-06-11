import pygame as pg
import neat
from Snake import Snake
from Fruit import Fruit
from direction_pattern import direction_pattern
import os

WIDTH = 1200
HEIGHT = 1200

BG = (34, 29, 29)

clock = pg.time.Clock()

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))


def draw_window(screen, snakes, fruits):

    screen.fill(BG)
    for fruit, snake in zip(fruits, snakes):
        fruit.draw(screen)
        snake.draw(screen)

    pg.display.update()


def check_out_boarder(snake):
    if 0 > snake.head_pos[0] or snake.head_pos[0] + snake.width > WIDTH or 0 > snake.head_pos[1] \
            or snake.head_pos[1] + snake.height > HEIGHT:
        return False
    return True


def main(genomes, config):

    nets = []
    ge = []
    snakes = []
    fruits = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        snakes.append(Snake())
        fruits.append(Fruit(WIDTH, HEIGHT))
        g.fitness = 0
        ge.append(g)

    running = True

    while running:

        clock.tick(30)

        if len(snakes) < 1:
            running = False
        count = 0
        for i, snake in enumerate(snakes):
            output = nets[i].activate((snake.head_pos[0], snake.head_pos[1], fruits[i].pos[0], fruits[i].pos[1]))
            if output[0] > 0.5:
                snake.dir = 'w'
            elif output[0] > 0:
                snake.dir = 's'
            elif output[0] < 0:
                snake.dir = 'a'
            elif output[0] < -0.5:
                snake.dir = 'd'
            else:
                print("Error")

        for snake in snakes:
            snake.move()

        draw_window(screen, snakes, fruits)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        for i in range(len(snakes)):
            if snakes[i].crossing_fruit(fruits[i].fruit):
                ge[i].fitness += 1
                fruits[i].new_pos()
                snakes[i].lengthen_tail()

        for i, snake in enumerate(snakes):
            # snake.body_collision()
            if not(check_out_boarder(snake)):
                snakes.pop(i)
                fruits.pop(i)
                nets.pop(i)


def run(config_file):
    import pickle
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main, 10000)
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close()


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
