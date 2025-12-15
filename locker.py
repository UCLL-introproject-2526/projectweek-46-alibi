import pygame
import random
import math

def show_locker(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    WIDTH, HEIGHT = screen.get_size()

    # Kleuren
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
    ]
    selected_color = colors[0]

    BOX_SIZE = 50
    START_X = 40
    Y = HEIGHT - 120

    play_button = pygame.Rect(WIDTH//2 - 80, HEIGHT - 50, 160, 40)

    # Bubbels
    bubbles = [{
        "x": random.randint(0, WIDTH),
        "y": random.randint(HEIGHT - 100, HEIGHT),
        "speed": random.uniform(0.4, 1.4),
        "size": random.randint(3, 7)
    } for _ in range(25)]

    # Zeewier
    plants = []
    for _ in range(15):
        x = random.randint(0, WIDTH)
        h = random.randint(40, 120)
        wiggle = random.uniform(0.02, 0.06)
        plants.append((x, h, wiggle))

    def draw_fish(color, x=WIDTH//2 - 60, y=60):
        pygame.draw.ellipse(screen, color, (x, y, 120, 60))
        pygame.draw.polygon(screen, color, [(x, y+30), (x-40, y), (x-40, y+60)])
        pygame.draw.circle(screen, (0, 0, 0), (x + 100, y + 30), 5)

    time = 0

    while True:
        time += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.MOUSEBUTTONUP:
                mx, my = event.pos

                # kleur selecteren
                for i, color in enumerate(colors):
                    rect = pygame.Rect(
                        START_X + i * (BOX_SIZE + 10),
                        Y,
                        BOX_SIZE,
                        BOX_SIZE
                    )
                    if rect.collidepoint(mx, my):
                        selected_color = color

                # terug naar homescreen
                if play_button.collidepoint(mx, my):
                    return selected_color

        # ---------------- TEKENEN ----------------
        screen.fill((5, 50, 120))

        # Lichtstralen
        for i in range(80):
            lx = (i * 15 + time * 0.7) % WIDTH
            pygame.draw.line(screen, (80, 130, 200), (lx, 0), (lx - 40, HEIGHT), 1)

        # Zeewier
        for x, h, wiggle in plants:
            top_x = x + math.sin(time * wiggle) * 6
            pygame.draw.line(
                screen,
                (20, 90, 70),
                (x, HEIGHT),
                (top_x, HEIGHT - h),
                5
            )

        # Bubbels
        for b in bubbles:
            b["y"] -= b["speed"]
            if b["y"] < 0:
                b["y"] = HEIGHT
                b["x"] = random.randint(0, WIDTH)
            pygame.draw.circle(
                screen,
                (200, 220, 255),
                (int(b["x"]), int(b["y"])),
                b["size"]
            )

        # Vis voorbeeld
        draw_fish(selected_color)

        # Kleurenpalet
        for i, color in enumerate(colors):
            rect = pygame.Rect(
                START_X + i * (BOX_SIZE + 10),
                Y,
                BOX_SIZE,
                BOX_SIZE
            )
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        # Speelknop
        pygame.draw.rect(screen, (0, 200, 100), play_button)
        pygame.draw.rect(screen, (0, 0, 0), play_button, 2)
        screen.blit(font.render("TERUG", True, (0, 0, 0)),
                    (play_button.x + 50, play_button.y + 10))
        screen.blit(font.render("Kies je viskleur", True, (255, 255, 255)),
                    (WIDTH//2 - 80, 20))

        pygame.display.flip()
        clock.tick(60)
