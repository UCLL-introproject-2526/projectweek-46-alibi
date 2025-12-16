import pygame
import math
from window import draw_background   # zelfde achtergrond



def show_home_screen(screen):
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
