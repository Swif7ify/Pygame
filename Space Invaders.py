import pygame
import random

class Player:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("images/spaceInvaders/spaceship.png"), (64, 64))
        self.x, self.y = 420, 450
        self.x_change, self.y_change = 0, 0
        self.hitbox = pygame.Rect(self.x, self.y, 64, 64)

    def update_position(self):
        self.x += self.x_change
        self.y += self.y_change
        self.x = max(0, min(self.x, 836))
        self.y = max(0, min(self.y, 536))
        self.hitbox.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Enemy:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("images/spaceInvaders/monster.png"), (64, 64))
        self.x = random.randint(0, 900)
        self.y = random.randint(10, 70)
        self.x_change = 0.20
        self.y_change = 40
        self.hitbox = pygame.Rect(self.x, self.y, 64, 64)

    def update_position(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = 0.2
            self.y += self.y_change
        elif self.x >= 836:
            self.x_change = -0.2
            self.y += self.y_change
        self.hitbox.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Bullet:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("images/spaceInvaders/bullet.png"), (20, 50))
        self.x, self.y = 0, 0
        self.y_change = 0.60
        self.state = "ready"
        self.hitbox = self.image.get_rect()

    def fire(self, x, y):
        self.state = "fire"
        self.x, self.y = x, y

    def update_position(self):
        if self.state == "fire":
            self.y -= self.y_change
            self.hitbox.topleft = (self.x, self.y)
            if self.y <= 0:
                self.state = "ready"
                self.hitbox.topleft = (-100, -100)

    def draw(self, screen):
        if self.state == "fire":
            screen.blit(self.image, (self.x, self.y))

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((900, 600))
        self.background = pygame.image.load("images/spaceInvaders/bg.png").convert()
        pygame.mixer.music.load("sounds/spaceBGM.mp3")
        pygame.mixer.music.play(-1)
        pygame.display.set_caption("Space Invaders")
        icon = pygame.image.load("images/spaceInvaders/ufo.png")
        pygame.display.set_icon(icon)
        self.font = pygame.font.Font("freesansbold.ttf", 24)
        self.score = 0
        self.player = Player()
        self.bullet = Bullet()
        self.enemies = [Enemy() for _ in range(6)]
        self.key_states = {
            pygame.K_a: False,
            pygame.K_d: False,
            pygame.K_w: False,
            pygame.K_s: False,
        }
        self.running = True

    def show_score(self):
        score_text = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def game_over_screen(self):
        game_over_font = pygame.font.Font("freesansbold.ttf", 64)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(game_over_text, (250, 250))
        pygame.display.update()
        pygame.time.wait(2000)

    def pause_menu(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        exit()

            self.screen.fill((0, 0, 0))
            pause_font = pygame.font.Font("freesansbold.ttf", 64)
            pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
            self.screen.blit(pause_text, (300, 200))

            resume_font = pygame.font.Font("freesansbold.ttf", 32)
            resume_text = resume_font.render("Press R to Resume", True, (255, 255, 255))
            self.screen.blit(resume_text, (300, 300))

            quit_font = pygame.font.Font("freesansbold.ttf", 32)
            quit_text = quit_font.render("Press Q to Quit", True, (255, 255, 255))
            self.screen.blit(quit_text, (300, 350))

            pygame.display.update()

    def run(self):
        while self.running:
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key in self.key_states:
                        self.key_states[event.key] = True
                    if event.key == pygame.K_SPACE and self.bullet.state == "ready":
                        pygame.mixer.Sound("sounds/lasersound.mp3").play()
                        self.bullet.fire(self.player.x + 10, self.player.y)
                    if event.key == pygame.K_p:
                        self.pause_menu()

                if event.type == pygame.KEYUP:
                    if event.key in self.key_states:
                        self.key_states[event.key] = False

            self.player.x_change = 0
            self.player.y_change = 0
            if self.key_states[pygame.K_a]:
                self.player.x_change = -0.3
            if self.key_states[pygame.K_d]:
                self.player.x_change = 0.3
            if self.key_states[pygame.K_w]:
                self.player.y_change = -0.3
            if self.key_states[pygame.K_s]:
                self.player.y_change = 0.3

            self.player.update_position()
            self.bullet.update_position()

            for enemy in self.enemies:
                enemy.update_position()
                if self.player.hitbox.colliderect(enemy.hitbox):
                    self.game_over_screen()
                    self.running = False
                elif self.bullet.hitbox.colliderect(enemy.hitbox):
                    pygame.mixer.Sound("sounds/explosion.mp3").play()
                    self.bullet.state = "ready"
                    self.bullet.hitbox.topleft = (-100, -100)
                    enemy.x, enemy.y = random.randint(0, 836), random.randint(10, 70)
                    self.score += 100

            self.player.draw(self.screen)
            self.bullet.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            self.show_score()
            pygame.display.update()
            pygame.time.Clock().tick(99999)

if __name__ == "__main__":
    game = Game()
    game.run()