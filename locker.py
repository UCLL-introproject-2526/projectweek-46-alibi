import pygame
import random
import math
import os

def show_locker(screen):
    pygame.mixer.init()

    # Muziek laden
    try:
        pygame.mixer.music.load("muziek/baby-shark-rhapsody-199067.mp3")
        pygame.mixer.music.set_volume(50)
        pygame.mixer.music.play(-1)
    except:
        print("Kon locker_music.mp3 niet laden!")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    WIDTH, HEIGHT = screen.get_size()

    # -------------------------------
    #   VISSEN & PATRONEN
    # -------------------------------
    fishes = ["vis1", "vis2", "vis3", "vis4", "vis5"]
    selected_fish = "vis1"

    patterns = ["none", "stripes", "dots", "waves"]
    selected_pattern = "none"

    BOX_SIZE = (60,40)
    START_X = 40
    COLOR_Y = HEIGHT - 150
    PATTERN_Y = HEIGHT - 90

    start_button = pygame.Rect(WIDTH//2 - 170, HEIGHT - 45, 160, 40)
    back_button  = pygame.Rect(WIDTH//2 + 10,  HEIGHT - 45, 160, 40)

    # 👉 ITEMSHOP BUTTON (rechtsboven)
    itemshop_button = pygame.Rect(WIDTH - 150, 20, 130, 40)

    # -------------------------------
    #   ACHTERGROND EFFECTEN
    # -------------------------------
    bubbles = [{
        "x": random.randint(0, WIDTH),
        "y": random.randint(HEIGHT - 200, HEIGHT),
        "speed": random.uniform(0.6, 1.8),
        "size": random.randint(3, 8)
    } for _ in range(45)]

    stones = [{
        "x": random.randint(0, WIDTH),
        "y": random.randint(HEIGHT - 120, HEIGHT - 50),
        "w": random.randint(40, 120),
        "h": random.randint(20, 60),
        "color": (
            random.randint(60, 90),
            random.randint(60, 80),
            random.randint(60, 80)
        )
    } for _ in range(18)]

    plants = []
    for _ in range(45):
        x = random.randint(0, WIDTH)
        h = random.randint(40, 140)
        wiggle = random.uniform(0.015, 0.05)
        plants.append((x, h, wiggle))

    # -------------------------------
    #   VIS VOORBEELD
    # -------------------------------
    def draw_fish(fish, pattern, x=WIDTH//2 - 60, y=HEIGHT // 2 - 30):
        # accept 'img/vis1.png', 'vis1.png' or just 'vis1'
        if fish.startswith("img/") or fish.startswith("img\\") or fish.endswith(".png"):
            path = fish
        else:
            path = os.path.join("img", fish + ".png")
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (120, 60))
        screen.blit(image, (x, y))


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
                pygame.mixer.music.stop()
                return "back", None, None

            if event.type == pygame.MOUSEBUTTONUP:
                mx, my = event.pos

                # vis selecteren
                for i, fish in enumerate(fishes):
                    rect = pygame.Rect(
                        START_X + i*(BOX_SIZE[0]+10),
                        COLOR_Y,
                        BOX_SIZE[0],
                        BOX_SIZE[1]
                    )
                    if rect.collidepoint(mx, my):
                        selected_fish = fish

                # patroon selecteren
                for i, pat in enumerate(patterns):
                    rect = pygame.Rect(
                        START_X + i*(BOX_SIZE[0]+10),
                        PATTERN_Y,
                        BOX_SIZE[0],
                        BOX_SIZE[1]
                    )
                    if rect.collidepoint(mx, my):
                        selected_pattern = pat

                # START GAME
                if start_button.collidepoint(mx, my):
                    pygame.mixer.music.stop()
                    return "start", selected_fish, selected_pattern

                # TERUG
                if back_button.collidepoint(mx, my):
                    pygame.mixer.music.stop()
                    return "back", None, None

                # 👉 ITEMSHOP OPENEN
                if itemshop_button.collidepoint(mx, my):
                    pygame.mixer.music.stop()
                    return "itemshop", selected_fish, selected_pattern

        # --- TEKENEN ---
        screen.fill((8, 30, 70))

        # Lichtdeeltjes
        for i in range(180):
            px = random.randint(0, WIDTH)
            py = (random.randint(0, HEIGHT) + time) % 650
            screen.set_at((px, py), (70, 120, 170))

        # Bodem
        pygame.draw.rect(screen, (170, 150, 110), (0, HEIGHT - 140, WIDTH, 140))

        # stenen
        for s in stones:
            pygame.draw.ellipse(screen, s["color"],
                                (s["x"], s["y"], s["w"], s["h"]))

        # planten
        for x, h, wiggle in plants:
            top_x = x + math.sin(time * wiggle) * (5 + h * 0.05)
            pygame.draw.line(
                screen,
                (40, 120, 90),
                (x, HEIGHT),
                (top_x, HEIGHT - h),
                4
            )

        # bubbels
        for b in bubbles:
            b["y"] -= b["speed"]
            if b["y"] < 0:
                b["y"] = HEIGHT
                b["x"] = random.randint(0, WIDTH)
            pygame.draw.circle(screen, (200, 220, 255),
                               (int(b["x"]), int(b["y"])),
                               b["size"])

        # vis voorbeeld
        draw_fish(selected_fish, selected_pattern)

        # vispalet
        for i, fish in enumerate(fishes):
            rect = pygame.Rect(
                START_X + i*(BOX_SIZE[0]+10),
                COLOR_Y,
                BOX_SIZE[0],
                BOX_SIZE[1]
            )
            # laad kleine image
            if fish.startswith("img/") or fish.startswith("img\\") or fish.endswith(".png"):
                small_path = fish
            else:
                small_path = os.path.join("img", fish + ".png")
            small_image = pygame.image.load(small_path).convert_alpha()
            small_image = pygame.transform.scale(small_image, (BOX_SIZE[0], BOX_SIZE[1]))
            screen.blit(small_image, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        screen.blit(font.render("KLEUR", True, (255,255,255)),
                    (START_X, COLOR_Y - 25))


        # knoppen
        pygame.draw.rect(screen, (0, 200, 100), start_button)
        pygame.draw.rect(screen, (0, 0, 0), start_button, 2)
        screen.blit(font.render("START GAME", True, (0,0,0)),
                    (start_button.x + 25, start_button.y + 10))

        pygame.draw.rect(screen, (200, 200, 200), back_button)
        pygame.draw.rect(screen, (0, 0, 0), back_button, 2)
        screen.blit(font.render("TERUG", True, (0,0,0)),
                    (back_button.x + 55, back_button.y + 10))

        # 👉 ITEMSHOP KNOP
        pygame.draw.rect(screen, (255, 200, 0), itemshop_button)
        pygame.draw.rect(screen, (0, 0, 0), itemshop_button, 2)
        screen.blit(font.render("ITEMSHOP", True, (0,0,0)),
                    (itemshop_button.x + 10, itemshop_button.y + 10))

        pygame.display.flip()
        clock.tick(60)
