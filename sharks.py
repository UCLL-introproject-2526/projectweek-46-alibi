import pygame
import random
from window import create_main_surface

def run_game(screen):
    clock = pygame.time.Clock()
    WIDTH, HEIGHT = screen.get_size()

    time = 0  # 👈 nodig voor animatie

    # === rest van je game-setup ===
    fish_image = pygame.image.load("fish.png").convert_alpha()
    fish_image = pygame.transform.scale(fish_image, (60, 40))
    fish_rect = fish_image.get_rect(x=100, y=HEIGHT // 2)
    fish_speed = 5

    shark_image = pygame.image.load("shark.png").convert_alpha()
    shark_image = pygame.transform.scale(shark_image, (80, 50))
    sharks = []

    score = 0
    spawn_timer = 0
    spawn_delay = 120
    shark_speed = 4
    game_over = False

    while True:
        # 🌊 ZELFDE ACHTERGROND ALS window.py
        draw_background(screen, time)
        time += 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "home"

        # === game logic hier ===
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            fish_rect.y -= fish_speed
        if keys[pygame.K_DOWN]:
            fish_rect.y += fish_speed
        fish_rect.y = max(0, min(HEIGHT - fish_rect.height, fish_rect.y))

        spawn_timer += 1
        if spawn_timer > spawn_delay:
            spawn_timer = 0
            rect = shark_image.get_rect(x=WIDTH, y=random.randint(0, HEIGHT - 50))
            sharks.append(rect)

        for shark in sharks[:]:
            shark.x -= shark_speed
            if shark.right < 0:
                sharks.remove(shark)
            if shark.colliderect(fish_rect):
                game_over = True

        # === tekenen bovenop achtergrond ===
        screen.blit(fish_image, fish_rect)
        for shark in sharks:
            screen.blit(shark_image, shark)

        pygame.display.flip()
        clock.tick(60)
