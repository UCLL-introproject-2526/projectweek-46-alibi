import pygame
import math
import random

WIDTH, HEIGHT = 1024, 768

def show_home_screen(screen):
    clock = pygame.time.Clock()
    font_title = pygame.font.SysFont("arialblack", 72)
    font_button = pygame.font.SysFont("arial", 36)

    rays = [random.randint(0, WIDTH) for _ in range(6)]
    time = 0

    start_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 80, 300, 70)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    return "start"

        # achtergrond
        screen.fill((0, 10, 30))

        # lichtstralen
        for x in rays:
            pygame.draw.line(
                screen,
                (40, 90, 140),
                (x, 0),
                (x + math.sin(time * 0.01) * 40, HEIGHT // 2),
                2
            )

        # titel
        title = font_title.render("DEEP SEA", True, (180, 220, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))

        # knop
        color = (70, 130, 180) if start_button.collidepoint(mouse_pos) else (50, 90, 140)
        pygame.draw.rect(screen, color, start_button, border_radius=12)

        text = font_button.render("START GAME", True, (255, 255, 255))
        screen.blit(
            text,
            (start_button.centerx - text.get_width()//2,
             start_button.centery - text.get_height()//2)
        )

        time += 2
        pygame.display.flip()
        clock.tick(60)
        
show_home_screen()