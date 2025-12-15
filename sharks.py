import pygame
import random
from window import draw_background  # 👈 zelfde achtergrond!

def run_game(screen):
    clock = pygame.time.Clock()
    WIDTH, HEIGHT = screen.get_size()
    time = 0

    # VIS
    fish_image = pygame.image.load("fish.png").convert_alpha()
    fish_image = pygame.transform.scale(fish_image, (60, 40))
    fish_rect = fish_image.get_rect(x=100, y=HEIGHT // 2)
    fish_speed = 5

    # HAAI
    shark_image = pygame.image.load("shark.png").convert_alpha()
    shark_image = pygame.transform.scale(shark_image, (80, 50))
    sharks = []

    spawn_timer = 0
    spawn_delay = 90   # spawn vaker haaien
    shark_speed = 4
    vertical_speed = 0.8  # minder snel naar boven/beneden

    # SCORE
    score = 0
    highscore = 0
    score_timer = 0

    game_over = False

    font = pygame.font.SysFont(None, 32)
    big_font = pygame.font.SysFont(None, 56)

    while True:
        draw_background(screen, time)
        time += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "home"
                if game_over and event.key == pygame.K_RETURN:
                    # reset game
                    fish_rect.y = HEIGHT // 2
                    sharks = []
                    spawn_timer = 0
                    score = 0
                    score_timer = 0
                    game_over = False

        if not game_over:
            # SCORE OPHOOG
            score_timer += 1
            if score_timer >= 30:  # 30 frames ≈ 0.5 seconde
                score += 1
                score_timer = 0

            # VIS BEWEGEN
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                fish_rect.y -= fish_speed
            if keys[pygame.K_DOWN]:
                fish_rect.y += fish_speed
            fish_rect.y = max(0, min(HEIGHT - fish_rect.height, fish_rect.y))

            # HAAIEN SPAWNEN
            spawn_timer += 1
            if spawn_timer > spawn_delay:
                spawn_timer = 0
                for _ in range(random.randint(1, 2)):
                    rect = shark_image.get_rect(
                        x=WIDTH,
                        y=random.randint(0, HEIGHT - shark_image.get_height())
                    )
                    sharks.append(rect)

            # HAAIEN BEWEGEN
            for shark in sharks[:]:
                shark.x -= shark_speed

                if shark.y + shark.height/2 < fish_rect.y + fish_rect.height/2:
                    shark.y += vertical_speed
                elif shark.y + shark.height/2 > fish_rect.y + fish_rect.height/2:
                    shark.y -= vertical_speed

                if shark.right < 0:
                    sharks.remove(shark)

                if shark.colliderect(fish_rect):
                    game_over = True
                    highscore = max(highscore, score)

            # TEKENEN
            screen.blit(fish_image, fish_rect)
            for shark in sharks:
                screen.blit(shark_image, shark)

            # SCORE DISPLAY
            screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10, 10))
            screen.blit(font.render(f"Highscore: {highscore}", True, (255,255,255)), (10, 40))

        else:
            # GAME OVER SCOREBORD
            screen.blit(big_font.render("GAME OVER", True, (255,255,255)), (WIDTH//2 - 150, 80))
            screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (WIDTH//2 - 70, 160))
            screen.blit(font.render(f"Highscore: {highscore}", True, (255,255,255)), (WIDTH//2 - 90, 200))
            screen.blit(font.render("ENTER = opnieuw spelen", True, (255,255,255)), (WIDTH//2 - 150, 260))
            screen.blit(font.render("ESC = afsluiten", True, (255,255,255)), (WIDTH//2 - 120, 300))

        pygame.display.flip()
        clock.tick(60)