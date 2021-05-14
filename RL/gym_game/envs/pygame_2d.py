import pygame
import random
from pygame.sprite import Group
from pygame.sprite import Sprite
import math
import sys

class PyGame2D:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 800))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 30)
        self.ship = Ship((800, 500))
        self.obstacles = Group()
        self.game_speed = 60
        self.mode = 0
        self.score = 0

    def action(self, action):
        if action == 0:
            self.ship.rect.x -= 1
        if action == 1:
            self.ship.rect.x = self.ship.rect.x
        if action == 2:
            self.ship.rect.x += 1

    def evaluate(self):
        reward = 0
        for obstacle_one in self.obstacles.sprites():
            if obstacle_one.rect.top == 1000:
                self.score += 1
                self.obstacles.remove(obstacle_one)
        print(len(self.obstacles))
        if not self.ship.is_alive:
            reward = -10000 + self.ship.score

        return reward

    def is_done(self):
        if not self.ship.is_alive:
            self.ship.score = 0
        return True

    def observe(self):
        radars = self.ship.radars
        ret = [0, 0, 0, 0, 0]
        for i in radars:
            ret.append(radars[1])
        return ret

    def view(self):
        nie = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                sys.exit()
        self.screen.fill((0, 0, 0))
        self.ship.draw(self.screen)
        if len(self.obstacles) <= 5:
            if len(self.obstacles) == 0:
                new_obstacle = Obstacle(self.screen)
                self.obstacles.add(new_obstacle)
            for obs in self.obstacles:
                if obs.rect.top <= 0:
                    nie = 1
                    break
            if nie == 0:
                new_obstacle = Obstacle(self.screen)
                self.obstacles.add(new_obstacle)
        for obs in self.obstacles:
            obs.draw_obstacle()
            obs.update()
        pygame.display.flip()
        self.clock.tick(self.game_speed)


class Ship:
    def __init__(self, pos):
        self.surface = pygame.image.load('ship.bmp')
        self.surface = pygame.transform.scale(self.surface, (100, 100))
        self.rect = self.surface.get_rect()
        self.rect.bottom = pos[0]
        self.rect.centerx = pos[1]
        self.pos = pos
        self.center = [self.pos[0]+50, self.pos[1]+50]
        self.radars = []
        self.is_alive = True
        self.current_check = 0
        self.prev_score = 0
        self.cur_score = 0
        self.score = 0
        self.time_spent = 0

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def check_radar(self, obstacles):
        for obstacle_one in obstacles.sprites():
            [x, y] = obstacle_one.rect.x, obstacle_one.rect.y
            dist = int(math.sqrt(math.pow(x-self.center[0], 2) + math.pow(y - self.center[1], 2)))
            self.radars.append([(x, y), dist])

    def check_collision(self, obstacles):
        self.is_alive = True
        for obstacle in obstacles.copy():
            if obstacle.rect.colliderect(self):
                self.is_alive = False
                break


class Obstacle(Sprite):
    def __init__(self, screen):
        super(Obstacle, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(100, 100, 50, 50)
        self.rect.centerx = random.randint(0, 1000)
        self.rect.bottom = 0
        self.y = float(self.rect.y)
        self.color = (210, 105, 30)
        self.speed_factor = 1

    def update(self):
        self.y += 5
        self.rect.y = self.y



    def draw_obstacle(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
