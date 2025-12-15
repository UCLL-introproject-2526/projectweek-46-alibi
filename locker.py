import pygame
import sys

pygame.init()

# Scherm
WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vis Kleurenpalet")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

def show_locker():
    # States
    LOCKER = "locker"
    GAME = "game"
    state = LOCKER

    # Kleuren
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
    ]

    selected_color = colors[0]

    # Palet layout
    BOX_SIZE = 50
    START_X = 40
    Y = 180

    # Speel knop
    play_button = pygame.Rect(220, 240, 160, 40)

    def draw_fish(color, x=240, y=60):
        pygame.draw.ellipse(screen, color, (x, y, 120, 60))
        pygame.draw.polygon(
            screen,
            color,
            [(x, y + 30), (x - 40, y), (x - 40, y + 60)]
        )
        pygame.draw.circle(screen, (0, 0, 0), (x + 100, y + 30), 5)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if state == LOCKER:
                    # Kleur kiezen
                    for i, color in enumerate(colors):
                        rect = pygame.Rect(
                            START_X + i * (BOX_SIZE + 10),
                            Y,
                            BOX_SIZE,
                            BOX_SIZE
                        )
                        if rect.collidepoint(mx, my):
                            selected_color = color

                    # Naar spel
                    if play_button.collidepoint(mx, my):
                        state = GAME

        # LOCKER
        if state == LOCKER:
            screen.fill((0, 120, 200))
            draw_fish(selected_color)

            for i, color in enumerate(colors):
                rect = pygame.Rect(
                    START_X + i * (BOX_SIZE + 10),
                    Y,
                    BOX_SIZE,
                    BOX_SIZE
                )
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)

            pygame.draw.rect(screen, (0, 200, 100), play_button)
            pygame.draw.rect(screen, (0, 0, 0), play_button, 2)
            screen.blit(font.render("SPELEN", True, (0, 0, 0)), (270, 250))
            screen.blit(font.render("Kies je viskleur", True, (255, 255, 255)), (250, 20))

        # GAME
        elif state == GAME:
            screen.fill((0, 120, 200))
            draw_fish(selected_color, 240, 120)
            screen.blit(font.render("Spel gestart!", True, (255, 255, 255)), (250, 20))

        pygame.display.flip()
        clock.tick(60)

# Functie starten
show_locker()
