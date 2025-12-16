import pygame
import random
import math


# --------------------------------
#   OUTLINED TEKST
# --------------------------------
def draw_outlined_text(screen, text, font, color, outline_color, pos):
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            if dx != 0 or dy != 0:
                outline = font.render(text, True, outline_color)
                screen.blit(outline, (pos[0] + dx, pos[1] + dy))

    screen.blit(font.render(text, True, color), pos)


# --------------------------------
#   HOME SCREEN
# --------------------------------
def show_home_screen(screen):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # -------- AUDIO --------
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    pygame.mixer.music.load("muziek/jaws.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # -------- AFBEELDING --------
    shark_img = pygame.image.load("img/shark_mouth.png").convert_alpha()
    shark_img = pygame.transform.scale(shark_img, (420, 320))

    # -------- EFFECTEN --------
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

    # -------- UI --------
    title_font = pygame.font.SysFont("arialblack", 72)
    sub_font = pygame.font.SysFont("arial", 32)
    button_font = pygame.font.SysFont("arial", 34)

    start_button  = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 + 120, 320, 70)
    locker_button = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 + 210, 320, 70)
    close_button  = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 + 300, 320, 70)

    # -------- BIJT ANIMATIE --------
    bite_anim = False
    bite_target = None
    bite_timer = 0

    time = 0
    pygame.event.clear()

    # -------- LOOP --------
    while True:
        mouse_pos = pygame.mouse.get_pos()
        shake_x = shake_y = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit"

            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.collidepoint(event.pos):
                    bite_anim = True
                    bite_target = "start"
                    bite_timer = 0

                if locker_button.collidepoint(event.pos):
                    bite_anim = True
                    bite_target = "locker"
                    bite_timer = 0

                if close_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return "quit"

        # ===== ACHTERGROND =====
        screen.fill((8, 30, 70))

        for i in range(180):
            px = random.randint(0, WIDTH)
            py = (random.randint(0, HEIGHT) + time) % HEIGHT
            screen.set_at((px, py), (70, 120, 170))

        pygame.draw.rect(screen, (170, 150, 110),
                         (0, HEIGHT - 140, WIDTH, 140))

        for s in stones:
            pygame.draw.ellipse(screen, s["color"],
                                (s["x"], s["y"], s["w"], s["h"]))

        for x, h, wiggle in plants:
            top_x = x + math.sin(time * wiggle) * (5 + h * 0.05)
            pygame.draw.line(screen, (40, 120, 90),
                             (x, HEIGHT), (top_x, HEIGHT - h), 4)

        for b in bubbles:
            b["y"] -= b["speed"]
            if b["y"] < 0:
                b["y"] = HEIGHT
                b["x"] = random.randint(0, WIDTH)
            pygame.draw.circle(screen, (200, 220, 255),
                               (int(b["x"]), int(b["y"])), b["size"])

        # ===== HAAI + BIJT =====
        if bite_anim:
            bite_timer += 1
            shake_x = random.randint(-6, 6)
            shake_y = random.randint(-6, 6)

            scale = 1 + bite_timer * 0.05
            shark_zoom = pygame.transform.scale(
                shark_img,
                (int(420 * scale), int(320 * scale))
            )

            screen.blit(
                shark_zoom,
                (
                    WIDTH//2 - shark_zoom.get_width()//2 + shake_x,
                    120 + shake_y
                )
            )

            if bite_timer > 12:
                pygame.mixer.music.stop()
                return bite_target
        else:
            screen.blit(
                shark_img,
                (WIDTH//2 - shark_img.get_width()//2, 120)
            )

        # ===== TITEL =====
        draw_outlined_text(
            screen,
            "SHARK ATTACK",
            title_font,
            (30, 70, 120),
            (255, 255, 255),
            (WIDTH//2 - 260, 200)
        )

        subtitle = sub_font.render(
            "Ontwijk de hongerige haaien en verzamel schatten!",
            True,
            (50, 100, 160)
        )
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 280))

        # ===== KNOPPEN =====
        for rect, text in [
            (start_button, "START GAME"),
            (locker_button, "LOCKER"),
            (close_button, "SLUITEN")
        ]:
            hover = rect.collidepoint(mouse_pos)

            if rect == close_button:
                color = (200, 60, 60) if hover else (160, 40, 40)
            else:
                color = (70, 140, 200) if hover else (50, 120, 180)

            pygame.draw.rect(screen, color, rect, border_radius=14)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=14)

            label = button_font.render(text, True, (255, 255, 255))
            screen.blit(
                label,
                (rect.centerx - label.get_width()//2,
                 rect.centery - label.get_height()//2)
            )

        time += 1
        pygame.display.flip()
        clock.tick(60)
