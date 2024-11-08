import pygame
import random

class Player:
    def __init__(self):
        self.image = pygame.image.load("images/flappyBird/bird.png").convert_alpha()
        self.X, self.Y = 70, 100
        self.Y_change = 0
        self.Gravity = 1.5  # Lower gravity for smoother descent
        self.flapSpeed = -15  # Strength of the upward flap
        self.Max_fall_speed = 10  # Limit to the downward speed
        self.HitBox = pygame.Rect(self.X, self.Y, 55, 47)

    def update_position(self):
        # Apply gravity and cap the fall speed
        self.Y_change += self.Gravity
        if self.Y_change > self.Max_fall_speed:
            self.Y_change = self.Max_fall_speed

        # Update the Y position based on Y_change
        self.Y += self.Y_change
        self.Y = max(0, min(self.Y, 670))  # Constrain to screen bounds

    def flap(self):
        # Upward movement when space bar is pressed
        self.Y_change = self.flapSpeed

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
        self.X_change = 7
        self.HitBoxOne = pygame.Rect(self.X, self.Y, 85, 700)
        self.HitBoxTwo = pygame.Rect(self.X, self.Y, 85, 700)
        self.scored = False

    def update_position(self):
        self.X -= self.X_change
        if self.X <= -300:
            self.X = 600
            self.Y = random.randint(-400, 0)
            self.scored = False

        self.HitBoxOne.topleft = (self.X + 163, self.Y - 220)
        self.HitBoxTwo.topleft = (self.X + 163, self.Y + 720)

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

        self.clock = pygame.time.Clock()
        self.running = True

    def main_screen(self):
        title_font = pygame.font.Font("freesansbold.ttf", 64)
        prompt_font = pygame.font.Font("freesansbold.ttf", 32)
        title_text = title_font.render("Flappy Bird", True, (255, 255, 255))
        prompt_text = prompt_font.render("Press SPACE to play", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(600 // 2, 800 // 2 - 100))
        prompt_rect = prompt_text.get_rect(center=(600 // 2, 800 // 2 + 100))

        while True:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(title_text, title_rect)
            self.screen.blit(prompt_text, prompt_rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

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
        game_score_rect = game_score.get_rect(center=(600 // 2, 800 // 2 - 100))
        game_over_rect = game_over_text.get_rect(center=(600 // 2, 800 // 2 - 200))
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(game_score, game_score_rect)

        restart_font = pygame.font.Font("freesansbold.ttf", 32)
        restart_text = restart_font.render("Press R to Restart", True, (255, 255, 255))
        quit_text = restart_font.render("Press Q to Quit", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(600 // 2, 800 // 2 + 200))
        quit_rect = quit_text.get_rect(center=(600 // 2, 800 // 2 + 250))
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(quit_text, quit_rect)
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        exit()

    def reset_game(self):
        self.score = 0
        self.player = Player()
        self.pipe = [Pipe(600 + i * 300) for i in range(3)]
        pygame.mixer.music.play(-1)
        self.run()

    def show_score(self):
        score_text = self.font.render("Score: " + str(self.score), True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(600 // 2, 50))
        self.screen.blit(score_text, score_rect)

    def run(self):
        self.main_screen()
        while self.running:
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.Sound("sounds/flappyBird/fly.mp3").play()
                        self.player.flap()
                    if event.key == pygame.K_p:
                        self.pause()

            if self.player.Y >= 670:
                pygame.mixer.music.pause()
                self.game_over_screen()
                self.running = False

            self.player.HitBox.topleft = (self.player.X + 5, self.player.Y + 5)

            self.player.update_position()
            self.player.draw(self.screen)
            for p in self.pipe:
                if p.X + p.X_change + 90 < self.player.X and not p.scored:
                    pygame.mixer.Sound("sounds/flappyBird/scoreUp.mp3").play()
                    self.score += 1
                    p.scored = True

                p.update_position()
                p.draw(self.screen)
                if self.player.HitBox.colliderect(p.HitBoxOne) or self.player.HitBox.colliderect(p.HitBoxTwo):
                    pygame.mixer.music.pause()
                    self.game_over_screen()
                    self.running = False

            self.show_score()
            self.clock.tick(60)
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
