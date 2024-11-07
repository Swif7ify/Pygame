import pygame
pygame.init()

screen = pygame.display.set_mode((500, 500))
font = pygame.font.Font("freesansbold.ttf", 24)

color = (255, 255, 255)
button = pygame.Rect(200, 200, 100, 50)

def draw_text(text, x, y):
    text = font.render(text, True, (255, 255, 255))
    screen.blit(text, (x, y))
    pygame.display.update()
    pygame.time.wait(2000)


running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                draw_text("Button Clicked", 250, 250)

    pygame.draw.rect(screen, color, button)
    pygame.display.update()