import pygame
import random
import math

def show_locker(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    WIDTH, HEIGHT = screen.get_size()

    # -------------------------------
    #   KLEUREN & PATRONEN
    # -------------------------------
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
    ]
    selected_color = colors[0]

    patterns = ["none", "stripes", "dots", "waves"]
    selected_pattern = "none"

    BOX_SIZE = 50
    START_X = 40
    COLOR_Y = HEIGHT - 150
    PATTERN_Y = HEIGHT - 90

    # 👉 NIEUWE KNOPPEN
    start_button = pygame.Rect(WIDTH//2 - 170, HEIGHT - 45, 160, 40)
    back_button  = pygame.Rect(WIDTH//2 + 10,  HEIGHT - 45, 160, 40)

    # -------------------------------
    #   ACHTERGROND EFFECTEN
    # -------------------------------
    bubbles = [{
        "x": random.randint(0, WIDTH),
        "y": random.randint(HEIGHT - 100, HEIGHT),
        "speed": random.uniform(0.4, 1.4),
        "size": random.randint(3, 7)
    } for _ in range(25)]

    plants = []
    for _ in range(15):
        x = random.randint(0, WIDTH)
        h = random.randint(40, 120)
        wiggle = random.uniform(0.02, 0.06)
        plants.append((x, h, wiggle))

    # -------------------------------
    #   VIS VOORBEELD
    # -------------------------------
    def draw_fish(color, pattern, x=WIDTH//2 - 60, y=60):
        pygame.draw.ellipse(screen, color, (x, y, 120, 60))
        pygame.draw.polygon(screen, color, [(x, y+30), (x-40, y), (x-40, y+60)])
        pygame.draw.circle(screen, (0, 0, 0), (x + 100, y + 30), 5)

        if pattern == "stripes":
            for i in range(4):
                pygame.draw.rect(screen, (255, 255, 255),
                                 (x + 20 + i*20, y + 5, 10, 50), 2)

        elif pattern == "dots":
            for i in range(5):
                pygame.draw.circle(screen, (255, 255, 255),
                                   (x + 20 + i*18, y + 20 + (i % 2)*10), 6)

        elif pattern == "waves":
            for i in range(6):
                wx = x + 15 + i * 17
                wy = y + 10 + math.sin(i * 0.8) * 6
                pygame.draw.circle(screen, (255, 255, 255), (wx, wy), 4)

    time = 0

    # -------------------------------
    #   MAIN LOOP
    # -------------------------------
    while True:
        time += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "back", None, None

            if event.type == pygame.MOUSEBUTTONUP:
                mx, my = event.pos

                # kleur selecteren
                for i, color in enumerate(colors):
                    rect = pygame.Rect(START_X + i*(BOX_SIZE+10), COLOR_Y, BOX_SIZE, BOX_SIZE)
                    if rect.collidepoint(mx, my):
                        selected_color = color

                # patroon selecteren
                for i, pattern in enumerate(patterns):
                    rect = pygame.Rect(START_X + i*(BOX_SIZE+10), PATTERN_Y, BOX_SIZE, BOX_SIZE)
                    if rect.collidepoint(mx, my):
                        selected_pattern = pattern

                # 👉 START GAME
                if start_button.collidepoint(mx, my):
                    return "start", selected_color, selected_pattern

                # 👉 TERUG
                if back_button.collidepoint(mx, my):
                    return "back", None, None

        # ---------------- TEKENEN ----------------
        screen.fill((5, 50, 120))

        # lichtstralen
        for i in range(80):
            lx = (i * 15 + time * 0.7) % WIDTH
            pygame.draw.line(screen, (80, 130, 200), (lx, 0), (lx - 40, HEIGHT), 1)

        # planten
        for x, h, wiggle in plants:
            top_x = x + math.sin(time * wiggle) * 6
            pygame.draw.line(screen, (20, 90, 70), (x, HEIGHT), (top_x, HEIGHT - h), 5)

        # bubbels
        for b in bubbles:
            b["y"] -= b["speed"]
            if b["y"] < 0:
                b["y"] = HEIGHT
                b["x"] = random.randint(0, WIDTH)
            pygame.draw.circle(screen, (200, 220, 255),
                               (int(b["x"]), int(b["y"])), b["size"])

        # vis voorbeeld
        draw_fish(selected_color, selected_pattern)

        # kleurpalet
        for i, color in enumerate(colors):
            rect = pygame.Rect(START_X + i*(BOX_SIZE+10), COLOR_Y, BOX_SIZE, BOX_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        screen.blit(font.render("KLEUR", True, (255,255,255)),
                    (START_X, COLOR_Y - 25))

        # patroonpalet
        for i, pattern in enumerate(patterns):
            rect = pygame.Rect(START_X + i*(BOX_SIZE+10), PATTERN_Y, BOX_SIZE, BOX_SIZE)
            pygame.draw.rect(screen, (180, 180, 180), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            screen.blit(font.render(pattern, True, (0,0,0)),
                        (rect.x + 5, rect.y + 15))

        screen.blit(font.render("PATRONEN", True, (255,255,255)),
                    (START_X, PATTERN_Y - 25))

        # 👉 KNOPPEN
        pygame.draw.rect(screen, (0, 200, 100), start_button)
        pygame.draw.rect(screen, (0, 0, 0), start_button, 2)
        screen.blit(font.render("START GAME", True, (0,0,0)),
                    (start_button.x + 25, start_button.y + 10))

        pygame.draw.rect(screen, (200, 200, 200), back_button)
        pygame.draw.rect(screen, (0, 0, 0), back_button, 2)
        screen.blit(font.render("TERUG", True, (0,0,0)),
                    (back_button.x + 55, back_button.y + 10))

        pygame.display.flip()
        clock.tick(60)
