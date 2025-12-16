import pygame
import random
import math
import os
from window import draw_background
from highscores import load_scores

# -------------------------------
# CONSTANTEN
# -------------------------------
FISH_W = 50
FISH_H = 30
FPS = 60
LEVEL_SCORE = 250

SHARK_SIZE = (80, 50)

# -------------------------------
# SCORE OPSLAAN
# -------------------------------
def save_score(score):
    with open("scores.txt", "a") as f:
        f.write(str(score) + "\n")

# -------------------------------
# PLAYER FISH
# -------------------------------
def draw_player_fish(surface, fish, pattern, x, y):
    if fish.startswith("img/") or fish.endswith(".png"):
        path = fish
    else:
        path = os.path.join("img", fish + ".png")

    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (FISH_W, FISH_H))
    surface.blit(image, (x, y))

# -------------------------------
# BOSS CLASS
# -------------------------------
class Boss:
    def __init__(self, image_path, size, base_hp, speed, fire_delay, bullet_speed):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.base_hp = base_hp
        self.speed = speed
        self.fire_delay = fire_delay
        self.bullet_speed = bullet_speed

# -------------------------------
# BOSS TYPES
# -------------------------------
BOSS_TYPES = [
    ("img/boss.png", (160, 100), 30, 1.0, 90, 6),
    ("img/bombini.png", (140, 80), 20, 1.5, 60, 8),
    ("img/tung.png", (200, 120), 60, 0.8, 120, 4),
]

# -------------------------------
# GAME
# -------------------------------
def run_game(screen, fish, pattern, coin_manager=None):
    clock = pygame.time.Clock()
    WIDTH, HEIGHT = screen.get_size()
    time = 0

    # speler
    player_x = 100
    player_y = HEIGHT // 2
    fish_speed = 5

    # images
    shark_image = pygame.image.load("img/shark.png").convert_alpha()
    shark_image = pygame.transform.scale(shark_image, SHARK_SIZE)

    chest_image = pygame.image.load("img/kist.png").convert_alpha()
    chest_image = pygame.transform.scale(chest_image, (50, 50))

    fluobeam_image = pygame.image.load("img/Fluobeam.png").convert_alpha()
    fluobeam_image = pygame.transform.scale(fluobeam_image, (20, 4))

    boss_bullet_image = pygame.image.load("img/Fluobeam.png").convert_alpha()
    boss_bullet_image = pygame.transform.scale(boss_bullet_image, (14, 6))

    # game objecten
    sharks = []
    laser_bullets = []
    boss_bullets = []

    # boss
    boss_active = False
    current_boss = None
    boss_rect = None
    boss_hp = 0
    boss_max_hp = 0
    boss_fire_timer = 0

    # boss beweging (op/af, beperkt)
    boss_dir = 1
    boss_start_y = 0
    BOSS_MOVE_RANGE = 80

    # timers
    laser_active = False
    laser_timer = 0
    fire_timer = 0

    spawn_timer = 0
    spawn_delay = 90
    shark_speed = 4

    score = 240
    score_timer = 0
    last_boss_score = 0

    scores = load_scores()
    highscore = max(scores) if scores else 0

    level = 1
    game_over = False

    font = pygame.font.SysFont(None, 32)
    big_font = pygame.font.SysFont(None, 56)

    # -------------------------------
    # MAIN LOOP
    # -------------------------------
    while True:
        draw_background(screen, time)
        time += 1

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "home"

                if game_over and event.key == pygame.K_RETURN:
                    sharks.clear()
                    laser_bullets.clear()
                    boss_bullets.clear()
                    boss_active = False
                    current_boss = None
                    score = 0
                    game_over = False

        # -------------------------------
        # GAME LOGICA
        # -------------------------------
        if not game_over:

            if not boss_active:
                score_timer += 1
                if score_timer >= 30:
                    score += 1
                    score_timer = 0

            # level scaling
            level = score // LEVEL_SCORE + 1
            shark_speed = 4 + level
            spawn_delay = max(30, 90 - level * 5)

            # boss spawn
            if score >= last_boss_score + 250 and not boss_active:
                boss_active = True
                sharks.clear()
                params = random.choice(BOSS_TYPES)
                current_boss = Boss(*params)


                boss_rect = current_boss.image.get_rect(
                    x=WIDTH + 40,
                    y=HEIGHT // 2 - current_boss.image.get_height() // 2
                )

                boss_start_y = boss_rect.y
                boss_dir = 1

                boss_max_hp = current_boss.base_hp + score // 10
                boss_hp = boss_max_hp
                last_boss_score = score
                boss_fire_timer = 0

            # speler beweging
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player_y -= fish_speed
            if keys[pygame.K_DOWN]:
                player_y += fish_speed
            player_y = max(0, min(HEIGHT - FISH_H, player_y))

            player_rect = pygame.Rect(player_x, player_y, FISH_W, FISH_H)

            # haaien spawn
            if not boss_active:
                spawn_timer += 1
                if spawn_timer > spawn_delay:
                    spawn_timer = 0
                    sharks.append(
                        shark_image.get_rect(
                            x=WIDTH,
                            y=random.randint(0, HEIGHT - SHARK_SIZE[1])
                        )
                    )

            # haaien gedrag
            for shark in sharks[:]:
                shark.x -= shark_speed
                if shark.right < 0:
                    sharks.remove(shark)
                elif shark.colliderect(player_rect):
                    game_over = True
                    save_score(score)

            # laser bullets
            fire_timer -= 1
            if fire_timer <= 0:
                laser_bullets.append(
                    pygame.Rect(player_x + FISH_W, player_y + FISH_H // 2 - 2, 20, 4)
                )
                fire_timer = random.randint(8, 14)

            for bullet in laser_bullets[:]:
                bullet.x += 10
                if bullet.x > WIDTH:
                    laser_bullets.remove(bullet)

            # bullets vs sharks
            for bullet in laser_bullets[:]:
                for shark in sharks[:]:
                    if bullet.colliderect(shark):
                        sharks.remove(shark)
                        laser_bullets.remove(bullet)
                        break

            # -------------------------------
            # BOSS GEDRAG
            # -------------------------------
            if boss_active and boss_rect:
                # naar binnen schuiven
                if boss_rect.x > WIDTH - 220:
                    boss_rect.x -= 2

                # rustige op/af beweging
                boss_rect.y += boss_dir * current_boss.speed
                if boss_rect.y > boss_start_y + BOSS_MOVE_RANGE:
                    boss_dir = -1
                elif boss_rect.y < boss_start_y - BOSS_MOVE_RANGE:
                    boss_dir = 1

                # boss schieten
                boss_fire_timer += 1
                if boss_fire_timer >= current_boss.fire_delay:
                    boss_fire_timer = 0
                    boss_bullets.append(
                        pygame.Rect(
                            boss_rect.x,
                            boss_rect.centery - 3,
                            14,
                            6
                        )
                    )

            # boss bullets
            for bullet in boss_bullets[:]:
                bullet.x -= current_boss.bullet_speed
                if bullet.right < 0:
                    boss_bullets.remove(bullet)
                elif bullet.colliderect(player_rect):
                    game_over = True
                    save_score(score)

            # player bullets vs boss
            if boss_active:
                for bullet in laser_bullets[:]:
                    if bullet.colliderect(boss_rect):
                        boss_hp -= 1
                        laser_bullets.remove(bullet)
                        if boss_hp <= 0:
                            boss_active = False
                            current_boss = None
                            boss_rect = None
                            boss_bullets.clear()
                            score += 50

            # -------------------------------
            # TEKENEN
            # -------------------------------
            draw_player_fish(screen, fish, pattern, player_x, player_y)

            for bullet in laser_bullets:
                screen.blit(fluobeam_image, bullet)

            for bullet in boss_bullets:
                screen.blit(boss_bullet_image, bullet)

            for shark in sharks:
                screen.blit(shark_image, shark)

            if boss_active and boss_rect:
                screen.blit(current_boss.image, boss_rect)

                bar_w = 200
                pygame.draw.rect(screen, (255, 0, 0),
                                 (WIDTH // 2 - bar_w // 2, 20, bar_w, 16))
                pygame.draw.rect(screen, (0, 255, 0),
                                 (WIDTH // 2 - bar_w // 2, 20,
                                  int(bar_w * boss_hp / boss_max_hp), 16))

            screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))

        else:
            screen.blit(big_font.render("GAME OVER", True, (255, 255, 255)),
                        (WIDTH // 2 - 150, 150))

        pygame.display.flip()
        clock.tick(FPS)

        