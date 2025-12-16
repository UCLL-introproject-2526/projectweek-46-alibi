import pygame
import random
import math
from window import draw_background

# -------------------------------
#   CONSTANTEN
# -------------------------------
FISH_W = 50
FISH_H = 30
FPS = 60
LEVEL_SCORE = 100
POWER_UP_DURATION = 10 * FPS

<<<<<<< HEAD
# -------------------------------
#   HIGHSCORE
# -------------------------------
def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# -------------------------------
#   SPELER VIS
# -------------------------------
def draw_player_fish(surface, color, pattern, x, y):
    pygame.draw.ellipse(surface, color, (x, y, FISH_W, FISH_H))
    pygame.draw.polygon(surface, color,
        [(x, y + FISH_H//2), (x - 32, y), (x - 32, y + FISH_H)]
    )
    pygame.draw.circle(surface, (0, 0, 0),
        (x + FISH_W - 16, y + FISH_H//2), 4
    )
=======
def draw_player_fish(surface, fish, pattern, x, y):
    image = pygame.image.load(fish + ".png").convert_alpha()
    image = pygame.transform.scale(image, (FISH_W, FISH_H))
    surface.blit(image, (x, y))
>>>>>>> dc50ced302fd6e8ad41d1885ae5865fc3a7e418e

    if pattern == "stripes":
        for i in range(3):
            pygame.draw.rect(surface, (255,255,255),
                (x + 18 + i*18, y + 4, 8, FISH_H - 8), 2)

    elif pattern == "dots":
        for i in range(4):
            pygame.draw.circle(surface, (255,255,255),
                (x + 18 + i*18, y + 16 + (i % 2) * 8), 5)

    elif pattern == "waves":
        for i in range(5):
            wx = x + 14 + i * 16
            wy = y + FISH_H//2 + math.sin(i * 0.9) * 6
            pygame.draw.circle(surface, (255,255,255), (wx, int(wy)), 3)

# -------------------------------
#   GAME
# -------------------------------
def run_game(screen, fish, pattern):
    clock = pygame.time.Clock()
    WIDTH, HEIGHT = screen.get_size()
    time = 0

    player_x = 100
    player_y = HEIGHT // 2
    fish_speed = 5

<<<<<<< HEAD
    shark_image = pygame.image.load("shark.png").convert_alpha()
=======
    # haaien
    shark_image = pygame.image.load("img/shark.png").convert_alpha()
>>>>>>> dc50ced302fd6e8ad41d1885ae5865fc3a7e418e
    shark_image = pygame.transform.scale(shark_image, (80, 50))

<<<<<<< HEAD
    boss_image = pygame.image.load("boss.png").convert_alpha()
    boss_image = pygame.transform.scale(boss_image, (180, 100))

    kist_image = pygame.image.load("kist.png").convert_alpha()
    kist_image = pygame.transform.scale(kist_image, (50, 50))

    fluobeam_image = pygame.image.load("Fluobeam.png").convert_alpha()
=======
    # kist image
    kist_image = pygame.image.load("img/kist.png").convert_alpha()
    kist_image = pygame.transform.scale(kist_image, (50, 50))

    # fluobeam image
    fluobeam_image = pygame.image.load("img/Fluobeam.png").convert_alpha()
>>>>>>> dc50ced302fd6e8ad41d1885ae5865fc3a7e418e
    fluobeam_image = pygame.transform.scale(fluobeam_image, (12, 12))

    sharks = []
    boxes = []
    laser_bullets = []

    spawn_timer = 0
    spawn_delay = 90
    shark_speed = 4
    vertical_speed = 0.8

    score = 0
    score_timer = 0
    highscore = load_highscore()
    level = 1
    game_over = False

    power_up_active = False
    power_up_timer = 0
    last_box_spawn_score = 0
    box_speed = 4

    boss_active = False
    boss_rect = None
    boss_hp = 0
    boss_max_hp = 0

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
                    player_y = HEIGHT // 2
                    sharks.clear()
                    boxes.clear()
                    laser_bullets.clear()
                    score = 0
                    score_timer = 0
                    level = 1
                    game_over = False
                    boss_active = False

        if not game_over:
            score_timer += 1
            if score_timer >= 30:
                score += 1
                score_timer = 0

            new_level = score // LEVEL_SCORE + 1
            if new_level != level:
                level = new_level
                shark_speed = 4 + level
                spawn_delay = max(30, 90 - level * 5)

                if level % 5 == 0:
                    boss_active = True
                    sharks.clear()
                    boss_rect = boss_image.get_rect(
                        x=WIDTH + 40,
                        y=HEIGHT//2 - boss_image.get_height()//2
                    )
                    boss_max_hp = 20 + level * 5
                    boss_hp = boss_max_hp

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player_y -= fish_speed
            if keys[pygame.K_DOWN]:
                player_y += fish_speed
            player_y = max(0, min(HEIGHT - FISH_H, player_y))

            player_rect = pygame.Rect(player_x - 32, player_y, FISH_W, FISH_H)

            if not boss_active:
                spawn_timer += 1
                if spawn_timer > spawn_delay:
                    spawn_timer = 0
                    for _ in range(min(1 + level//2, 4)):
                        sharks.append(shark_image.get_rect(
                            x=WIDTH,
                            y=random.randint(0, HEIGHT - 50)
                        ))

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
                    if score > highscore:
                        highscore = score
                        save_highscore(highscore)

            if boss_active and boss_rect:
                if boss_rect.x > WIDTH - 220:
                    boss_rect.x -= 2
                if boss_rect.centery < player_rect.centery:
                    boss_rect.y += 1.5
                elif boss_rect.centery > player_rect.centery:
                    boss_rect.y -= 1.5

                if boss_rect.colliderect(player_rect):
                    game_over = True

            if power_up_active:
                power_up_timer -= 1
                if power_up_timer <= 0:
                    power_up_active = False
                if random.random() < 0.05:
                    laser_bullets.append({
                        "x": player_x + FISH_W//2,
                        "y": player_y + FISH_H//2,
                        "dx": 15
                    })

            for bullet in laser_bullets[:]:
                bullet["x"] += bullet["dx"]
                bullet_rect = pygame.Rect(bullet["x"]-5, bullet["y"]-5, 10, 10)

                if boss_active and boss_rect and bullet_rect.colliderect(boss_rect):
                    boss_hp -= 1
                    laser_bullets.remove(bullet)
                elif bullet["x"] > WIDTH:
                    laser_bullets.remove(bullet)

<<<<<<< HEAD
            if boss_active and boss_hp <= 0:
                boss_active = False
                boss_rect = None
                score += 50

            draw_player_fish(screen, color, pattern, player_x, player_y)
=======
            # tekenen
            draw_player_fish(screen, fish, pattern, player_x, player_y)
>>>>>>> dc50ced302fd6e8ad41d1885ae5865fc3a7e418e

            for shark in sharks:
                screen.blit(shark_image, shark)

            if boss_active and boss_rect:
                screen.blit(boss_image, boss_rect)
                bar_w = 200
                pygame.draw.rect(screen, (255,0,0),
                    (WIDTH//2 - bar_w//2, 20, bar_w, 16))
                pygame.draw.rect(screen, (0,255,0),
                    (WIDTH//2 - bar_w//2, 20, int(bar_w * boss_hp / boss_max_hp), 16))

            screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))
            screen.blit(font.render(f"Highscore: {highscore}", True, (255,255,255)), (10,40))
            screen.blit(font.render(f"Level: {level}", True, (255,255,255)), (10,70))

        else:
            screen.blit(big_font.render("GAME OVER", True, (255,255,255)),
                        (WIDTH//2 - 150, 100))
            screen.blit(font.render("ENTER = opnieuw", True, (255,255,255)),
                        (WIDTH//2 - 100, 180))

        pygame.display.flip()
        clock.tick(FPS)