from ship import Ship
import pygame
from os import path
from laser import Laser

# Load the images
RED_SPACESHIP = pygame.image.load(path.join('assets', 'pixel_ship_red_small.png'))
BLUE_SPACESHIP = pygame.image.load(path.join('assets', 'pixel_ship_blue_small.png'))
GREEN_SPACESHIP = pygame.image.load(path.join('assets', 'pixel_ship_green_small.png'))

# Projectiles
RED_LASER = pygame.image.load(path.join('assets', 'pixel_laser_red.png'))
BLUE_LASER = pygame.image.load(path.join('assets', 'pixel_laser_blue.png'))
GREEN_LASER = pygame.image.load(path.join('assets', 'pixel_laser_green.png'))


class Enemy(Ship):
    COLOR_DICT = {'red': (RED_SPACESHIP, RED_LASER),
                  'green': (GREEN_SPACESHIP, GREEN_LASER),
                  'blue': (BLUE_SPACESHIP, BLUE_LASER)
                  }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_image, self.laser_image = self.COLOR_DICT[color]
        self.mask = pygame.mask.from_surface(self.ship_image)

    def move(self, velocity):
        self.y += velocity

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x - 20, self.y - 20, self.laser_image)
            self.lasers.append(laser)
            self.cooldown_counter = 1
