import pygame
import random
import math
from window import draw_background
from highscores import load_scores

# -------------------------------
#   CONSTANTEN
# -------------------------------
FISH_W = 50
FISH_H = 30
FPS = 60
LEVEL_SCORE = 100

SHARK_SIZE = (80, 50)
BOSS_SIZE = (160, 100)   # 2x zo groot

# -------------------------------
#   SCORE OPSLAAN
# -------------------------------
def save_score(score):
    with open("scores.txt", "a") as f:
        f.write(str(score) + "\n")

# -------------------------------
#   VIS TEKENEN
# -------------------------------
def draw_player_fish(surface, fish, pattern, x, y):
    image = pygame.image.load(fish + ".png").convert_alpha()
    image = pygame.transform.scale(image, (FISH_W, FISH_H))
    surface.blit(image, (x, y))

    if pattern == "stripes":
        for i in range(3):
            pygame.draw.rect(surface, (255, 255, 255),
                             (x + 18 + i * 18, y + 4, 8, FISH_H - 8), 2)

    elif pattern == "dots":
        for i in range(4):
            pygame.draw.circle(surface, (255, 255, 255),
                               (x + 18 + i * 18, y + 16 + (i % 2) * 8), 5)

    elif pattern == "waves":
        for i in range(5):
            wx = x + 14 + i * 16
            wy = y + FISH_H // 2 + math.sin(i * 0.9) * 6
            pygame.draw.circle(surface, (255, 255, 255),
                               (wx, int(wy)), 3)

# -------------------------------
#   GAME
# -------------------------------
def run_game(screen, fish, pattern):
    clock = pygame.time.Clock()
    WIDTH, HEIGHT = screen.get_size()
    time = 0

    # speler
    player_x = 100
    player_y = HEIGHT // 2
    fish_speed = 5

    # afbeeldingen
    shark_image = pygame.image.load("img/shark.png").convert_alpha()
    shark_image = pygame.transform.scale(shark_image, SHARK_SIZE)

    boss_image = pygame.image.load("img/boss.png").convert_alpha()
    boss_image = pygame.transform.scale(boss_image, BOSS_SIZE)

    # objecten
    sharks = []

    # timers & snelheid
    spawn_timer = 0
    spawn_delay = 90
    shark_speed = 4
    vertical_speed = 0.8

    # score & level
    score = 0
    score_timer = 0

    scores = load_scores()
    highscore = max(scores) if scores else 0

    level = 1
    game_over = False

    # boss
    boss_active = False
    boss_defeated_this_level = False
    boss_rect = None
    boss_hp = 0
    boss_max_hp = 0

    font = pygame.font.SysFont(None, 32)
    big_font = pygame.font.SysFont(None, 56)

    # -------------------------------
    #   MAIN LOOP
    # -------------------------------
    while True:
        draw_background(screen, time)
        time += 1

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "home"

                if game_over and event.key == pygame.K_RETURN:
                    player_y = HEIGHT // 2
                    sharks.clear()
                    score = 0
                    score_timer = 0
                    level = 1
                    game_over = False
                    boss_active = False
                    boss_defeated_this_level = False

        # -------------------------------
        #   GAME LOGICA
        # -------------------------------
        if not game_over:
            # score
            score_timer += 1
            if score_timer >= 30:
                score += 1
                score_timer = 0

            # level bepalen
            new_level = score // LEVEL_SCORE + 1
            if new_level != level:
                level = new_level
                shark_speed = 4 + level
                spawn_delay = max(30, 90 - level * 5)
                boss_defeated_this_level = False

            # boss spawn aan begin van elk level >= 2
            if level >= 2 and not boss_active and not boss_defeated_this_level:
                boss_active = True
                sharks.clear()
                boss_rect = boss_image.get_rect(
                    x=WIDTH + 40,
                    y=HEIGHT // 2 - boss_image.get_height() // 2
                )
                boss_max_hp = 30 + level * 10
                boss_hp = boss_max_hp

            # speler beweging
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player_y -= fish_speed
            if keys[pygame.K_DOWN]:
                player_y += fish_speed
            player_y = max(0, min(HEIGHT - FISH_H, player_y))

            player_rect = pygame.Rect(player_x, player_y, FISH_W, FISH_H)

            # haaien spawnen (alleen zonder boss)
            if not boss_active:
                spawn_timer += 1
                if spawn_timer > spawn_delay:
                    spawn_timer = 0
                    for _ in range(min(1 + level // 2, 4)):
                        sharks.append(
                            shark_image.get_rect(
                                x=WIDTH,
                                y=random.randint(0, HEIGHT - SHARK_SIZE[1])
                            )
                        )

            # haaien gedrag
            for shark in sharks[:]:
                shark.x -= shark_speed
                if shark.centery < player_rect.centery:
                    shark.y += vertical_speed
                elif shark.centery > player_rect.centery:
                    shark.y -= vertical_speed

                if shark.right < 0:
                    sharks.remove(shark)

                elif shark.colliderect(player_rect):
                    game_over = True
                    save_score(score)
                    scores.append(score)
                    highscore = max(scores)

            # boss gedrag
            if boss_active and boss_rect:
                if boss_rect.x > WIDTH - 220:
                    boss_rect.x -= 2

                if boss_rect.centery < player_rect.centery:
                    boss_rect.y += 1.5
                elif boss_rect.centery > player_rect.centery:
                    boss_rect.y -= 1.5

                boss_rect.y = max(0, min(HEIGHT - boss_rect.height, boss_rect.y))

                if boss_rect.colliderect(player_rect):
                    game_over = True
                    save_score(score)
                    scores.append(score)
                    highscore = max(scores)

            # boss verslaan
            if boss_active and boss_hp <= 0:
                boss_active = False
                boss_defeated_this_level = True
                boss_rect = None
                score += 50

            # -------------------------------
            #   TEKENEN
            # -------------------------------
            draw_player_fish(screen, fish, pattern, player_x, player_y)

            for shark in sharks:
                screen.blit(shark_image, shark)

            if boss_active and boss_rect:
                screen.blit(boss_image, boss_rect)

                # HP balk
                bar_w = 200
                pygame.draw.rect(screen, (255, 0, 0),
                                 (WIDTH // 2 - bar_w // 2, 20, bar_w, 16))
                pygame.draw.rect(screen, (0, 255, 0),
                                 (WIDTH // 2 - bar_w // 2, 20,
                                  int(bar_w * boss_hp / boss_max_hp), 16))

            # HUD
            screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
            screen.blit(font.render(f"Highscore: {highscore}", True, (255, 255, 255)), (10, 40))
            screen.blit(font.render(f"Level: {level}", True, (255, 255, 255)), (10, 70))

        else:
            screen.blit(big_font.render("GAME OVER", True, (255, 255, 255)),
                        (WIDTH // 2 - 150, 120))
            screen.blit(font.render("ENTER = opnieuw", True, (255, 255, 255)),
                        (WIDTH // 2 - 100, 200))

        pygame.display.flip()
        clock.tick(FPS)