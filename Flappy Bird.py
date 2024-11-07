import pygame
import random

class Player:
    def __init__(self):
        self.image = pygame.image.load("images/flappyBird/bird.png").convert_alpha()
        self.X, self.Y = 70, 100
        self.Y_change = 0
        self.Gravity = 0.02
        self.HitBox = pygame.Rect(self.X, self.Y, 60, 52)

    def update_position(self):
        self.Y_change -= self.Gravity
        self.Y -= self.Y_change
        self.Y = max(0, min(self.Y, 670))

    def draw(self, screen):
        screen.blit(self.image, (self.X, self.Y))


class Pipe:
    def __init__(self, x_position):
        self.image = pygame.image.load("images/flappyBird/pipe.png").convert_alpha()
        self.image2 = pygame.image.load("images/flappyBird/pipe.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (400, 700))
        self.image2 = pygame.transform.rotate(self.image2, 180)
        self.image2 = pygame.transform.scale(self.image2, (400, 700))
        self.X = x_position
        self.Y = random.randint(-400, 0)
        self.X_change = 1
        self.HitBoxOne = pygame.Rect(self.X, self.Y, 100, 700)
        self.HitBoxTwo = pygame.Rect(self.X, self.Y, 100, 700)

    def update_position(self):
        self.X -= self.X_change
        if self.X <= -300:
            self.X = 600
            self.Y = random.randint(-400, 0)

        self.HitBoxOne.topleft = (self.X + 155, self.Y - 220)
        self.HitBoxTwo.topleft = (self.X + 155, self.Y + 720)

    def draw(self, screen):
        screen.blit(self.image, (self.X, self.Y))
        screen.blit(self.image2, (self.X + 10, self.Y + 500))


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((600, 800))
        self.background = pygame.transform.scale(pygame.image.load("images/flappyBird/bg.png"), (600, 800)).convert()
        pygame.mixer.music.load("sounds/flappyBird/bgm.mp3")
        pygame.mixer.music.play(-1)
        pygame.display.set_caption("Flappy Bird")
        icon = pygame.image.load("images/flappyBird/birdIcon.png")
        pygame.display.set_icon(icon)

        self.font = pygame.font.Font("freesansbold.ttf", 24)

        self.score = 0

        self.pipe = [Pipe(600 + i * 300) for i in range(3)]
        self.player = Player()

        self.running = True

    def pause(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    paused = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        exit()

            self.screen.fill((0, 0, 0))
            pause_font = pygame.font.Font("freesansbold.ttf", 64)
            pauseText = pause_font.render("Paused", True, (255, 255, 255))
            pause_rect = pauseText.get_rect(center=(600 // 2, 800 // 2 - 200))
            self.screen.blit(pauseText, pause_rect)

            font = pygame.font.Font("freesansbold.ttf", 32)
            resumeText = font.render("Press R to resume", True, (255, 255, 255))
            resume_rect = resumeText.get_rect(center=(600 // 2, 800 // 2))
            self.screen.blit(resumeText, resume_rect)

            quitText = font.render("Press Q to quit", True, (255, 255, 255))
            quit_rect = quitText.get_rect(center=(600 // 2, 800 // 2 + 100))
            self.screen.blit(quitText, quit_rect)
            pygame.display.update()

    def game_over_screen(self):
        pygame.mixer.Sound("sounds/flappyBird/gameOver.mp3").play()
        game_over_font = pygame.font.Font("freesansbold.ttf", 64)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        game_score = self.font.render("Score: " + str(self.score), True, (255, 100, 50))
        game_score_rect = game_score.get_rect(center=(600 // 2, 800 // 2 + 100))
        game_over_rect = game_over_text.get_rect(center=(600 // 2, 800 // 2))
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(game_score, game_score_rect)
        pygame.display.update()
        pygame.time.wait(2000)

    def show_score(self):
        score_text = self.font.render("Score: " + str(self.score), True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(600 // 2, 50))
        self.screen.blit(score_text, score_rect)

    def run(self):
        while self.running:
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.Sound("sounds/flappyBird/fly.mp3").play()
                        self.player.Y_change = 2.2
                    if event.key == pygame.K_p:
                        self.pause()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.player.Y_change = 0

            if self.player.Y == 670:
                self.running = False
            self.player.HitBox.topleft = (self.player.X, self.player.Y + 10)
            pygame.draw.rect(self.screen, (255, 0, 0), self.player.HitBox, 2)

            # limit the gravity
            if self.player.Y_change <= -1.5:
                self.player.Y_change = -1

            self.player.update_position()
            self.player.draw(self.screen)
            for p in self.pipe:
                p.update_position()
                p.draw(self.screen)
                pygame.draw.rect(self.screen, (255, 0, 0), p.HitBoxOne, 2)
                pygame.draw.rect(self.screen, (0, 255, 0), p.HitBoxTwo, 2)
                if self.player.HitBox.colliderect(p.HitBoxOne) or self.player.HitBox.colliderect(
                        p.HitBoxTwo):
                    pygame.mixer.music.pause()
                    self.game_over_screen()
                    self.running = False

                if p.X == self.player.X - 150:
                    pygame.mixer.Sound("sounds/flappyBird/scoreUp.mp3").play()
                    self.score += 1

            self.show_score()
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
