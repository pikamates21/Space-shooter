import pygame
from entity import Entity
from player import Player
from settings import HEIGHT, ENEMY_SPEED

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, -20, 30, 30)

        self.image = pygame.image.load("images/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 52))
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()
