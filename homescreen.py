import pygame
import math
import random

WIDTH, HEIGHT = 1024, 768

def draw_lightblue_background(screen, time):
    # 🌤️ Basis lichtblauw
    screen.fill((135, 200, 240))

    # ☀️ Zachte lichtstralen (van boven naar beneden)
    for x in range(0, WIDTH, 160):
        pygame.draw.line(
            screen,
            (200, 235, 255),
            (x, 0),
            (x + math.sin(time * 0.01) * 40, HEIGHT),
            3
        )

    # ✨ Zwevende deeltjes (stof / plankton)
    for i in range(120):
        px = (i * 37 + time * 1.2) % WIDTH
        py = (i * 19 + time * 0.6) % HEIGHT
        screen.set_at((int(px), int(py)), (215, 245, 255))


def show_home_screen(screen):
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("arialblack", 72)
    sub_font = pygame.font.SysFont("arial", 32)
    button_font = pygame.font.SysFont("arial", 34)

    start_button = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 + 120, 320, 70)
    locker_button = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 + 210, 320, 70)

    time = 0

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    return "start"
                if locker_button.collidepoint(mouse_pos):
                    return "locker"

        # 🌊 LICHTBLAUWE ACHTERGROND (losstaand)
        draw_lightblue_background(screen, time)

        # 🐠 Titel
        title = title_font.render("SHARK ATTACK", True, (30, 70, 120))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))

        subtitle = sub_font.render(
            "Ontwijk de hongerige haaien en verzamel schatten!",
            True,
            (50, 100, 160)
        )
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 280))

        # ▶️ Knoppen
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
                (rect.centerx - label.get_width()//2,
                 rect.centery - label.get_height()//2)
            )

        time += 2
        pygame.display.flip()
        clock.tick(60)
