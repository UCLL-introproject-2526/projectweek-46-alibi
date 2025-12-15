import pygame
import sys

pygame.init()

# Scherm
WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vis Kleurenpalet")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Alle kleuren direct beschikbaar
colors = [
    (255, 0, 0),    # rood
    (0, 255, 0),    # groen
    (0, 0, 255),    # blauw
    (255, 255, 0),  # geel
    (255, 0, 255),  # paars
]

selected_color = colors[0]

# Palet layout
BOX_SIZE = 50
START_X = 40
Y = 200

def draw_fish(color):
    pygame.draw.ellipse(screen, color, (260, 110, 120, 60))
    pygame.draw.polygon(
        screen,
        color,
        [(260, 140), (220, 110), (220, 170)]
    )
    pygame.draw.circle(screen, (0, 0, 0), (360, 140), 5)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for i, color in enumerate(colors):
                rect = pygame.Rect(
                    START_X + i * (BOX_SIZE + 10),
                    Y,
                    BOX_SIZE,
                    BOX_SIZE
                )
                if rect.collidepoint(mx, my):
                    selected_color = color

    screen.fill((0, 120, 200))  # zee

    draw_fish(selected_color)

    # Palet tekenen
    for i, color in enumerate(colors):
        rect = pygame.Rect(
            START_X + i * (BOX_SIZE + 10),
            Y,
            BOX_SIZE,
            BOX_SIZE
        )
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

    info = font.render("Klik een kleur om je vis te veranderen", True, (255, 255, 255))
    screen.blit(info, (150, 20))

    pygame.display.flip()
    clock.tick(60)