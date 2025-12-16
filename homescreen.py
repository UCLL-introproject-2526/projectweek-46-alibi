import pygame
import random
import math



def show_home_screen(screen):
    WIDTH, HEIGHT = screen.get_size()
    
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

    clock = pygame.time.Clock()

    WIDTH, HEIGHT = screen.get_size()  # ✅ HIER DE FIX

    title_font = pygame.font.SysFont("arialblack", 72)
    sub_font = pygame.font.SysFont("arial", 32)
    button_font = pygame.font.SysFont("arial", 34)

    start_button = pygame.Rect(WIDTH // 2 - 160, HEIGHT // 2 + 120, 320, 70)
    locker_button = pygame.Rect(WIDTH // 2 - 160, HEIGHT // 2 + 210, 320, 70)

    time = 0
    pygame.event.clear()

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.collidepoint(event.pos):
                    return "start"
                if locker_button.collidepoint(event.pos):
                    return "locker"


        title = title_font.render("SHARK ATTACK", True, (30, 70, 120))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))

        subtitle = sub_font.render(
            "Ontwijk de hongerige haaien en verzamel schatten!",
            True,
            (50, 100, 160)
        )
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 280))

        for rect, text in [
            (start_button, "START GAME"),
            (locker_button, "LOCKER")
        ]:
            hover = rect.collidepoint(mouse_pos)
            color = (70, 140, 200) if hover else (50, 120, 180)
            pygame.draw.rect(screen, color, rect, border_radius=14)

            label = button_font.render(text, True, (255, 255, 255))
            screen.blit(
                label,
                (rect.centerx - label.get_width() // 2,
                 rect.centery - label.get_height() // 2)
            )

        time += 1
        pygame.display.flip()
        clock.tick(60)

        # ---------------- TEKENEN ----------------
        screen.fill((8, 30, 70))

        # Lichtdeeltjes
        for i in range(180):
            px = random.randint(0, WIDTH)
            py = (random.randint(0, HEIGHT) + time) % 650
            screen.set_at((px, py), (70, 120, 170))

        # Bodem
        pygame.draw.rect(screen, (170, 150, 110),
                         (0, HEIGHT - 140, WIDTH, 140))

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
            pygame.draw.circle(screen,
                            (200, 220, 255),
                            (int(b["x"]), int(b["y"])),
                            b["size"])
