import pygame as pg
import math
SCREEN_WIDTH = 1440
TILE_SIZE = int(SCREEN_WIDTH / 54)
GREEN = pg.Color('green3')


class Enemy(pg.sprite.Sprite):
    def __init__(self, speed, health, pos, next_tile):
        super().__init__()
        # Change the speed to a close substitute that goes into TILE_SIZE evenly
        if abs(speed) > 15:
            self.speed = 15
        elif TILE_SIZE % abs(speed) > 6:
            self.speed = math.trunc(abs(speed))
            while TILE_SIZE % self.speed > 6:
                self.speed -= 1
        else:
            self.speed = int(abs(speed))
        # Define the enemy's other properties
        self.health = health
        self.coins = health
        self.pos = (pos[0]*TILE_SIZE, pos[1]*TILE_SIZE)
        self.rect = pg.Rect(pos, (TILE_SIZE, TILE_SIZE))
        self.color = GREEN
        self.prev = pos
        self.next = next_tile
        self.direction = None

    def update(self, multiplier):
        self.direction = (self.next[0] - self.prev[0], self.next[1] - self.prev[1])
        self.pos = list(self.pos)
        self.pos[0] += round(self.direction[0]*multiplier*self.speed, 3)
        self.pos[1] += round(self.direction[1]*multiplier*self.speed, 3)
        self.pos = tuple(self.pos)

    def draw(self, surface):
        self.rect = pg.Rect(self.pos, (TILE_SIZE, TILE_SIZE))
        pg.draw.rect(surface, self.color, self.rect)

    def check_path(self, grid):
        try:
            self_next = (self.next[0] + grid.path[self.next][0], self.next[1] + grid.path[self.next][1])
        except TypeError:
            return
        distance = math.sqrt((self.pos[0] - self.prev[0]*TILE_SIZE)**2 + (self.pos[1] - self.prev[1]*TILE_SIZE)**2)
        if distance > TILE_SIZE:
            self.pos = (self.next[0]*TILE_SIZE, self.next[1]*TILE_SIZE)
            self.prev = self.next
            self.next = self_next

    def successful(self, end):
        end = (end[0]*TILE_SIZE, end[1]*TILE_SIZE)
        goal = (end[0] + self.direction[0]*TILE_SIZE, end[1] + self.direction[1]*TILE_SIZE)
        if self.pos[0] >= goal[0] and self.pos[1] >= goal[1]:
            return True
        return False
