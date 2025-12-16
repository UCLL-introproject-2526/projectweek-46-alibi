import pygame
import random
import math
from window import draw_background
from highscores import load_scores
import os

# -------------------------------
#   CONSTANTEN
# -------------------------------
FISH_W = 50
FISH_H = 30
FPS = 60
LEVEL_SCORE = 250

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
    # support either a full path like "img/vis1.png" or a short name like "vis1"
    if fish.startswith("img/") or fish.startswith("img\\") or fish.endswith(".png"):
        path = fish
    else:
        path = os.path.join("img", fish + ".png")
    image = pygame.image.load(path).convert_alpha()
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
def run_game(screen, fish, pattern, coin_manager=None):
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

    chest_image = pygame.image.load("img/kist.png").convert_alpha()
    chest_image = pygame.transform.scale(chest_image, (50, 50))

    fluobeam_image = pygame.image.load("img/Fluobeam.png").convert_alpha()
    fluobeam_image = pygame.transform.scale(fluobeam_image, (20, 4))

    # game objecten
    sharks = []
    laser_bullets = []   # 👈 TOEVOEGEN

    laser_active = False
    laser_timer = 0
    fire_timer = 0
    chest_active = False
    chest_rect = None
    previous_chest_level = 0

    spawn_timer = 0
    spawn_delay = 90
    shark_speed = 4
    vertical_speed = 0.8

    # score & level
    score = 240
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

    # boss spawn elke 250 punten
    last_boss_score = 0

    font = pygame.font.SysFont(None, 32)
    big_font = pygame.font.SysFont(None, 56)



    # -------------------------------
    #   MAIN LOOP
    # -------------------------------
    while True:
        draw_background(screen, time)
        time += 1

        # events
        # -------------------------------
        #   EVENTS
        # -------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "home"

                if game_over and event.key == pygame.K_TAB:
                    return "locker"

                if game_over and event.key == pygame.K_RETURN:
                    player_y = HEIGHT // 2
                    sharks.clear()
                    laser_bullets.clear()
                    score = 0
                    score_timer = 0
                    level = 1
                    game_over = False
                    boss_active = False
                    boss_defeated_this_level = False
                    laser_active = False
                    laser_timer = 0
                    fire_timer = 0
                    chest_active = False
                    chest_rect = None
                    previous_chest_level = 0




        # -------------------------------
        #   GAME LOGICA
        # -------------------------------
        if not game_over:
            # score
            # score (pauze tijdens boss fight)
            if not boss_active:
                score_timer += 1
                if score_timer >= 30:
                    score += 1
                    score_timer = 0


            chest_level = score // 50
            if chest_level > previous_chest_level:
                previous_chest_level = chest_level
                chest_active = True
                chest_rect = chest_image.get_rect(x=WIDTH, y=random.randint(0, HEIGHT - 50))
                # spawn a coin alongside the chest if a coin manager was provided
                if coin_manager:
                    coin_manager.spawn_at(WIDTH, random.randint(0, HEIGHT - 50))

            if laser_active:
                laser_timer -= 1
                if laser_timer <= 0:
                    laser_active = False

            # level scaling
            new_level = score // LEVEL_SCORE + 1
            if new_level != level:
                level = new_level
                shark_speed = 4 + level
                spawn_delay = max(30, 90 - level * 5)
                boss_defeated_this_level = False


            # in de loop
            # boss spawn elke 250 punten
            if score >= last_boss_score + 250 and not boss_active:
                boss_active = True
                sharks.clear()
                boss_rect = boss_image.get_rect(
                    x=WIDTH + 40,
                    y=HEIGHT // 2 - boss_image.get_height() // 2
                )
                boss_max_hp = 30 + score // 10
                boss_hp = boss_max_hp
                last_boss_score = score  # update nu correct




            # speler beweging
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player_y -= fish_speed
            if keys[pygame.K_DOWN]:
                player_y += fish_speed
            player_y = max(0, min(HEIGHT - FISH_H, player_y))

            player_rect = pygame.Rect(player_x, player_y, FISH_W, FISH_H)

            if chest_active and chest_rect and chest_rect.colliderect(player_rect):
                laser_active = True
                laser_timer = 10 * FPS
                fire_timer = random.randint(30, 120)
                chest_active = False
                chest_rect = None

            # check coin collisions
            if coin_manager:
                if coin_manager.check_collision(player_rect):
                    # coin_manager increments its internal counter
                    pass

            # spawn haaien
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

            # chest gedrag
            if chest_active and chest_rect:
                chest_rect.x -= shark_speed
                if chest_rect.right < 0:
                    chest_active = False
                    chest_rect = None

            # update coins
            if coin_manager:
                coin_manager.update(WIDTH, HEIGHT)

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

            # laser bullets
            can_shoot = laser_active or boss_active

            if can_shoot:
                fire_timer -= 1
                if fire_timer <= 0:
                    laser_bullets.append(
                        pygame.Rect(player_x + FISH_W, player_y + FISH_H//2 - 2, 20, 4)
                    )
                    fire_timer = random.randint(4, 10)  # iets sneller schieten bij boss


                for bullet in laser_bullets[:]:
                    bullet.x += 10
                    if bullet.x > WIDTH:
                        laser_bullets.remove(bullet)

            for bullet in laser_bullets[:]:
                bullet.x += 10
                if bullet.x > WIDTH:
                    laser_bullets.remove(bullet)


            # collision bullets with sharks
            for bullet in laser_bullets[:]:
                for shark in sharks[:]:
                    if bullet.colliderect(shark):
                        sharks.remove(shark)
                        laser_bullets.remove(bullet)
                        break

            # collision with boss
            if boss_active and boss_rect:
                for bullet in laser_bullets[:]:
                    if bullet.colliderect(boss_rect):
                        boss_hp -= 1
                        laser_bullets.remove(bullet)
                        if boss_hp <= 0:
                            boss_active = False


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
                score += 1

            # -------------------------------
            #   TEKENEN
            # -------------------------------
            draw_player_fish(screen, fish, pattern, player_x, player_y)

            if chest_active and chest_rect:
                screen.blit(chest_image, chest_rect)

            if coin_manager:
                coin_manager.draw(screen)

            for bullet in laser_bullets:
                screen.blit(fluobeam_image, bullet)

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

            # HUD: render score, highscore, level, optional power-up, then coins below them
            hud_x = 10
            hud_y = 10
            line_h = 30
            idx = 0
            screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (hud_x, hud_y + idx * line_h))
            idx += 1
            screen.blit(font.render(f"Highscore: {highscore}", True, (255, 255, 255)), (hud_x, hud_y + idx * line_h))
            idx += 1
            screen.blit(font.render(f"Level: {level}", True, (255, 255, 255)), (hud_x, hud_y + idx * line_h))
            idx += 1

            if laser_active:
                seconds = laser_timer // FPS
                screen.blit(font.render(f"Power-up: {seconds}s", True, (255, 255, 255)), (hud_x, hud_y + idx * line_h))
                idx += 1

            if coin_manager:
                # draw coin icon then count to the right
                icon = coin_manager.image
                icon_w, icon_h = icon.get_size()
                y_pos = hud_y + idx * line_h
                screen.blit(icon, (hud_x, y_pos))
                screen.blit(font.render(str(coin_manager.get_count()), True, (255, 255, 255)), (hud_x + icon_w + 8, y_pos))

        else:
            screen.blit(big_font.render("GAME OVER", True, (255, 255, 255)),
                        (WIDTH // 2 - 150, 120))
            screen.blit(font.render("ENTER = opnieuw", True, (255, 255, 255)),
                        (WIDTH // 2 - 150, 200))
            screen.blit(font.render("ESC = Terug naar menu", True, (255, 255, 255)),
                        (WIDTH // 2 - 150, 320))
            screen.blit(font.render("Tab = Terug naar locker", True, (255, 255, 255)),
                        (WIDTH // 2 - 150, 440))

        pygame.display.flip()
        clock.tick(FPS)
        