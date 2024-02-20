from ship import Ship
import pygame
from os import path

# Player
YELLOW_SPACESHIP = pygame.image.load(path.join('assets', 'pixel_ship_yellow.png'))
YELLOW_LASER = pygame.image.load(path.join('assets', 'pixel_laser_yellow.png'))


class Player(Ship):

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_image = YELLOW_SPACESHIP
        self.laser_image = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.max_health = health

    def move_lasers(self, velocity, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(500):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def health_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_image.get_height() + 10,
                                               self.ship_image.get_width(), 10))

        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_image.get_height() + 10,
                                               self.ship_image.get_width() * (self.health / self.max_health), 10))

    def redraw(self, window):
        super().redraw(window)
        self.health_bar(window)
