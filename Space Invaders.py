import pygame
import random

class Player:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("images/spaceInvaders/spaceship.png"), (64, 64)).convert_alpha()
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
        self.image = pygame.transform.scale(pygame.image.load("images/spaceInvaders/monster.png"), (64, 64)).convert_alpha()
        self.x = random.randint(20, 836)
        self.y = random.randint(10, 70)
        self.x_change = 3
        self.y_change = 20
        self.speed = 3
        self.hitbox = pygame.Rect(self.x, self.y, 64, 64)

    def update_position(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = self.speed
            self.y += self.y_change
        elif self.x >= 836:
            self.x_change = -self.speed
            self.y += self.y_change
        self.hitbox.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Bullet:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("images/spaceInvaders/bullet.png"), (20, 50)).convert_alpha()
        self.x, self.y = 0, 0
        self.y_change = 6
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
        self.width, self.height = 900, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.image.load("images/spaceInvaders/bg.png").convert()
        pygame.mixer.music.load("sounds/spaceInvaders/spaceBGM.mp3")
        pygame.mixer.music.play(-1)
        pygame.display.set_caption("Space Invaders")
        icon = pygame.image.load("images/spaceInvaders/ufo.png")
        pygame.display.set_icon(icon)
        self.font = pygame.font.Font("freesansbold.ttf", 24)
        self.last_score_checkpoint = 0
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
        pygame.mixer.Sound("sounds/spaceInvaders/gameOver.mp3").play()
        game_over_font = pygame.font.Font("freesansbold.ttf", 64)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        game_over_text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 100))
        gameScore = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        gameScoreRect = gameScore.get_rect(center=(self.width // 2, self.height // 2 - 30))
        self.screen.blit(game_over_text, game_over_text_rect)
        self.screen.blit(gameScore, gameScoreRect)

        restart_font = pygame.font.Font("freesansbold.ttf", 32)
        restart_text = restart_font.render("Press R to Restart", True, (255, 255, 255))
        restart_text_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 30))
        quit_text = restart_font.render("Press Q to Quit", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=(self.width // 2, self.height // 2 + 70))
        self.screen.blit(restart_text, restart_text_rect)
        self.screen.blit(quit_text, quit_text_rect)
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()

    def restart(self):
        self.score = 0
        self.player.x, self.player.y = 420, 450
        self.bullet.state = "ready"
        self.bullet.hitbox.topleft = (-100, -100)
        self.enemies = [Enemy() for _ in range(6)]
        pygame.mixer.music.play(-1)
        self.run()

    def main_screen(self):
        self.screen.blit(self.background, (0, 0))
        start_font = pygame.font.Font("freesansbold.ttf", 54)
        start_text = start_font.render("Space Invaders", True, (255, 255, 255))
        start_game = self.font.render("Press Space to Start", True, (255, 255, 255))
        start_game_rect = start_game.get_rect(center=(self.width // 2, self.height // 2 + 50))
        start_text_rect = start_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(start_text, start_text_rect)
        self.screen.blit(start_game, start_game_rect)
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False


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
        self.main_screen()
        while self.running:
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key in self.key_states:
                        self.key_states[event.key] = True
                    if event.key == pygame.K_SPACE and self.bullet.state == "ready":
                        pygame.mixer.Sound("sounds/spaceInvaders/lasersound.mp3").play()
                        self.bullet.fire(self.player.x + 10, self.player.y)
                    if event.key == pygame.K_p:
                        self.pause_menu()

                if event.type == pygame.KEYUP:
                    if event.key in self.key_states:
                        self.key_states[event.key] = False

            self.player.x_change = 0
            self.player.y_change = 0
            if self.key_states[pygame.K_a]:
                self.player.x_change = -4
            if self.key_states[pygame.K_d]:
                self.player.x_change = 4
            if self.key_states[pygame.K_w]:
                self.player.y_change = -4
            if self.key_states[pygame.K_s]:
                self.player.y_change = 4

            self.player.update_position()
            self.bullet.update_position()

            if self.score != 0 and self.score % 1000 == 0 and self.score != self.last_score_checkpoint:
                self.bullet.y_change += 0.3
                for enemy in self.enemies:
                    enemy.speed += 0.2
                self.last_score_checkpoint = self.score

            for enemy in self.enemies:
                enemy.update_position()
                if self.player.hitbox.colliderect(enemy.hitbox):
                    pygame.mixer.music.pause()
                    self.game_over_screen()
                    self.running = False
                elif self.bullet.hitbox.colliderect(enemy.hitbox):
                    pygame.mixer.Sound("sounds/spaceInvaders/explosion.mp3").play()
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
            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()