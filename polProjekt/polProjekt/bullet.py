from entity import Entity
from settings import BULLET_SPEED

class Bullet(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 5, 10)
        self.image.fill((255, 255, 0))
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
