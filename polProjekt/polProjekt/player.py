import pygame
from entity import Entity
from settings import PLAYER_SPEED, WIDTH, HEIGHT

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 30)

        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (55, 55))
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = PLAYER_SPEED

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
