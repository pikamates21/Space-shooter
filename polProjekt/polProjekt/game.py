import pygame
import random
from player import Player
from enemy import Enemy
from bullet import Bullet
from settings import WIDTH, HEIGHT, FPS, BLACK

class Game:
    def __init__(self, x, y):
        self.state = "MENU"

        pygame.init()

        self.title_font = pygame.font.Font(None, 64)
        self.menu_text = self.title_font.render("START", True, (255, 255, 255))
        self.menu_rect = self.menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        self.game_over_text = self.title_font.render("GAME OVER", True, (255, 0, 0))
        self.game_over_rect = self.game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load("images/background.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.player = Player(WIDTH // 2, HEIGHT - 50)
        self.all_sprites.add(self.player)

        self.score = 0
        self.font = pygame.font.Font(None, 36)

        self.enemy_spawn_delay = 60
        self.min_spawn_delay = 5
        self.spawn_speedup = 2

        self.running = True

    def spawn_enemy(self):
        enemy = Enemy(random.randint(20, WIDTH - 20), -20)
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def run(self):
        enemy_timer = 0

        while self.running:
            self.clock.tick(FPS)

            self.handle_events()

            if self.state == "PLAYING":
                enemy_timer += 1
                if enemy_timer >= self.enemy_spawn_delay:
                    self.spawn_enemy()
                    enemy_timer = 0

            self.update()
            self.draw()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "MENU":
                    if self.menu_rect.collidepoint(event.pos):
                        self.state = "PLAYING"

                elif self.state == "GAME_OVER":
                    if self.game_over_rect.collidepoint(event.pos):
                        self.reset_game()

            if event.type == pygame.KEYDOWN:
                if self.state == "PLAYING" and event.key == pygame.K_SPACE:
                    bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)

    def reset_game(self):
        self.all_sprites.empty()
        self.enemies.empty()
        self.bullets.empty()

        self.player = Player(WIDTH // 2, HEIGHT - 50)
        self.all_sprites.add(self.player)

        self.score = 0
        self.state = "PLAYING"

        self.enemy_spawn_delay = 60

    def update(self):
        if self.state != "PLAYING":
            return

        self.all_sprites.update()

        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        if hits:
            self.score += len(hits)

            if self.enemy_spawn_delay > self.min_spawn_delay:
                self.enemy_spawn_delay -= self.spawn_speedup

        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.state = "GAME_OVER"

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        if self.state == "MENU":
            self.screen.blit(self.menu_text, self.menu_rect)

        elif self.state == "PLAYING":
            self.all_sprites.draw(self.screen)
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

        elif self.state == "GAME_OVER":
            self.all_sprites.draw(self.screen)
            self.screen.blit(self.game_over_text, self.game_over_rect)

        pygame.display.flip()




