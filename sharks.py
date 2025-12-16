import pygame
import random
import math
from window import draw_background   # zelfde achtergrond


# -------------------------------
#   SPELER VIS (kleiner formaat)
# -------------------------------
FISH_W = 50
FISH_H = 30

def draw_player_fish(surface, color, pattern, x, y):
    # body
    pygame.draw.ellipse(surface, color, (x, y, FISH_W, FISH_H))

    # staart
    pygame.draw.polygon(
        surface, color,
        [(x, y + FISH_H//2), (x - 32, y), (x - 32, y + FISH_H)]
    )

    # oog
    pygame.draw.circle(
        surface, (0, 0, 0),
        (x + FISH_W - 16, y + FISH_H//2),
        4
    )

    # patronen
    if pattern == "stripes":
        for i in range(3):
            pygame.draw.rect(
                surface, (255, 255, 255),
                (x + 18 + i*18, y + 4, 8, FISH_H - 8),
                2
            )

    elif pattern == "dots":
        for i in range(4):
            pygame.draw.circle(
                surface, (255, 255, 255),
                (x + 18 + i*18, y + 16 + (i % 2) * 8),
                5
            )

    elif pattern == "waves":
        for i in range(5):
            wx = x + 14 + i * 16
            wy = y + FISH_H//2 + math.sin(i * 0.9) * 6
            pygame.draw.circle(surface, (255, 255, 255), (wx, int(wy)), 3)


# -------------------------------
#   GAME
# -------------------------------
def run_game(screen, color, pattern):
    clock = pygame.time.Clock()
    WIDTH, HEIGHT = screen.get_size()
    time = 0

    # speler
    player_x = 100
    player_y = HEIGHT // 2
    fish_speed = 5

    # haaien
    shark_image = pygame.image.load("img/shark.png").convert_alpha()
    shark_image = pygame.transform.scale(shark_image, (80, 50))
    sharks = []

    # kist image
    kist_image = pygame.image.load("img/kist.png").convert_alpha()
    kist_image = pygame.transform.scale(kist_image, (50, 50))

    # fluobeam image
    fluobeam_image = pygame.image.load("img/Fluobeam.png").convert_alpha()
    fluobeam_image = pygame.transform.scale(fluobeam_image, (12, 12))

    spawn_timer = 0
    spawn_delay = 90
    shark_speed = 4
    vertical_speed = 0.8

    # score
    score = 0
    highscore = 0
    score_timer = 0
    game_over = False

    # power-up
    power_up_active = False
    power_up_timer = 0
    boxes = []
    last_box_spawn_score = 0
    box_speed = 4
    laser_bullets = []

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
                    # reset
                    player_y = HEIGHT // 2
                    sharks.clear()
                    spawn_timer = 0
                    score = 0
                    score_timer = 0
                    game_over = False
                    power_up_active = False
                    power_up_timer = 0
                    boxes.clear()
                    last_box_spawn_score = 0
                    laser_bullets.clear()

        if not game_over:
            # score omhoog
            score_timer += 1
            if score_timer >= 30:
                score += 1
                score_timer = 0

            # spawn power-up box elke 50 punten
            if score >= last_box_spawn_score + 50 and not boxes:
                box_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT - 50), 50, 50)
                boxes.append(box_rect)
                last_box_spawn_score = score

            # speler bewegen
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player_y -= fish_speed
            if keys[pygame.K_DOWN]:
                player_y += fish_speed

            player_y = max(0, min(HEIGHT - FISH_H, player_y))

            # haaien spawnen
            spawn_timer += 1
            if spawn_timer > spawn_delay:
                spawn_timer = 0
                for _ in range(random.randint(1, 2)):
                    rect = shark_image.get_rect(
                        x=WIDTH,
                        y=random.randint(0, HEIGHT - shark_image.get_height())
                    )
                    sharks.append(rect)

            # box beweging en botsing
            for box in boxes[:]:
                box.x -= box_speed
                if box.right < 0:
                    boxes.remove(box)
                elif box.colliderect(player_rect):
                    power_up_active = True
                    power_up_timer = 10 * 60  # 10 seconden bij 60 FPS
                    boxes.remove(box)

            # botsing + beweging
            player_rect = pygame.Rect(player_x - 32, player_y, FISH_W, FISH_H)

            for shark in sharks[:]:
                shark.x -= shark_speed

                if shark.centery < player_rect.centery:
                    shark.y += vertical_speed
                elif shark.centery > player_rect.centery:
                    shark.y -= vertical_speed

                if shark.right < 0:
                    sharks.remove(shark)
                    continue

                if shark.colliderect(player_rect):
                    game_over = True
                    highscore = max(highscore, score)

            # power-up timer
            if power_up_active:
                power_up_timer -= 1
                if power_up_timer <= 0:
                    power_up_active = False

                # vuur laser rechtdoor (naar rechts)
                if random.random() < 0.05:  # 5% kans per frame om te vuren
                    bullet_speed = 15
                    bullet = {
                        'x': player_x + FISH_W // 2,
                        'y': player_y + FISH_H // 2,
                        'dx': bullet_speed,
                        'dy': 0
                    }
                    laser_bullets.append(bullet)

            # laser bullets beweging en botsing
            for bullet in laser_bullets[:]:
                bullet['x'] += bullet['dx']
                bullet['y'] += bullet['dy']
                bullet_rect = pygame.Rect(bullet['x'] - 5, bullet['y'] - 5, 10, 10)
                hit = False
                for shark in sharks[:]:
                    if bullet_rect.colliderect(shark):
                        sharks.remove(shark)
                        hit = True
                        break
                if hit or bullet['x'] > WIDTH or bullet['x'] < 0 or bullet['y'] > HEIGHT or bullet['y'] < 0:
                    laser_bullets.remove(bullet)

            # tekenen
            draw_player_fish(screen, color, pattern, player_x, player_y)

            for shark in sharks:
                screen.blit(shark_image, shark)

            # teken boxes
            for box in boxes:
                screen.blit(kist_image, box)

            # teken laser bullets
            for bullet in laser_bullets:
                screen.blit(fluobeam_image, (int(bullet['x']) - 6, int(bullet['y']) - 6))

            screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10, 10))
            screen.blit(font.render(f"Highscore: {highscore}", True, (255,255,255)), (10, 40))

            if power_up_active:
                screen.blit(font.render(f"Power-up: {power_up_timer // 60}s", True, (255,255,255)), (10, 70))

        else:
            screen.blit(big_font.render("GAME OVER", True, (255,255,255)),
                        (WIDTH//2 - 150, 80))
            screen.blit(font.render(f"Score: {score}", True, (255,255,255)),
                        (WIDTH//2 - 70, 160))
            screen.blit(font.render(f"Highscore: {highscore}", True, (255,255,255)),
                        (WIDTH//2 - 90, 200))
            screen.blit(font.render("ENTER = opnieuw spelen", True, (255,255,255)),
                        (WIDTH//2 - 150, 260))
            screen.blit(font.render("ESC = terug", True, (255,255,255)),
                        (WIDTH//2 - 120, 300))

        pygame.display.flip()
        clock.tick(60)
