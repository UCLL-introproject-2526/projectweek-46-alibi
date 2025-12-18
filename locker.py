from cmath import rect
import pygame
import random
import math
import os
from coins import CoinManager
from powerups import FISH_POWERUPS
from window import draw_background


def show_locker(screen, coin_manager, unlocked_fishes, coins):
    SPACING_X = 60

    coin_img = pygame.image.load("img/muntje.png").convert_alpha()
    coin_img = pygame.transform.scale(coin_img, (24, 24))
    # Muziek laden
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("muziek/baby_shark.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    power_font = pygame.font.SysFont(None, 18)


    WIDTH, HEIGHT = screen.get_size()
    SAND_HEIGHT = 140

    coin_img = pygame.image.load("img/muntje.png").convert_alpha()
    coin_img = pygame.transform.scale(coin_img, (24, 24))

   


    # -------------------------------
    #   VISSEN & PATRONEN
    # -------------------------------
    fishes = ["vis1", "vis2", "vis3", "vis4", "vis5", "vis6", "vis7", "vis8", "vis9", "vis10"]
    selected_fish = "vis1"

    patterns = ["none", "stripes", "dots", "waves"]
    selected_pattern = "none"

    BOX_SIZE = (60,40)
    START_X = 40
    COLOR_Y = HEIGHT - SAND_HEIGHT - 60
    PATTERN_Y = HEIGHT - SAND_HEIGHT + 10


    start_button = pygame.Rect(WIDTH//2 - 170, HEIGHT - 45, 160, 40)
    back_button  = pygame.Rect(WIDTH//2 + 10,  HEIGHT - 45, 160, 40)

    # 👉 ITEMSHOP BUTTON (rechtsboven)
    itemshop_button = pygame.Rect(WIDTH - 150, 20, 130, 40)
    

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
                    START_X + i * (BOX_SIZE[0] + SPACING_X),
                    COLOR_Y,
                    BOX_SIZE[0],
                    BOX_SIZE[1]
                )


                    if rect.collidepoint(mx, my):
                        if fish in unlocked_fishes:
                            selected_fish = fish

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
                    return "itemshop", selected_fish, selected_pattern
               
        # --- TEKENEN ---
        draw_background(screen, time, scroll=False)
        x = 20
        y = 20

        screen.blit(coin_img, (x, y))
        screen.blit(
            font.render(str(coin_manager.get_count()), True, (255, 215, 0)),
            (x + 30, y + 2)
        )


        # vis voorbeeld
        draw_fish(selected_fish,selected_pattern)

        # vispalet
        for i, fish in enumerate(fishes):
            rect = pygame.Rect(
                START_X + i * (BOX_SIZE[0] + SPACING_X),
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

            # 🔒 LOCK overlay
            if fish not in unlocked_fishes:
                lock_overlay = pygame.Surface((BOX_SIZE[0], BOX_SIZE[1]), pygame.SRCALPHA)
                lock_overlay.fill((0, 0, 0, 160))  # donker transparant
                screen.blit(lock_overlay, rect)

                lock_text = font.render("LOCK", True, (255, 0, 0))
                screen.blit(lock_text, (rect.x + 10, rect.y + 10))

   
            # ⭐ POWER-UP TEKST (HIER IS fish GELDIG)
            power = FISH_POWERUPS.get(fish)

           
            if fish != "vis1" and power:
                power_text = power.replace("_", " ").upper()
                label = power_font.render(power_text, True, (255, 255, 255))

                screen.blit(
                    label,
                    (
                        rect.centerx - label.get_width() // 2,
                        rect.y - label.get_height() - 6
                    )
                )






       
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
