
import pygame
import random
import math
from window import draw_background
from highscores import load_scores
from powerups import FISH_POWERUPS
import os
import random
random.seed()  


# -------------------------------
#   CONSTANTEN
# -------------------------------
FISH_W = 50
FISH_H = 30
FPS = 60
LEVEL_SCORE = 50

SCROLL_SPEED = 6

SHARK_SIZE = (80, 50)
BOSS_SIZE = (160, 100)   # 2x zo groot

# -------------------------------
#   BOSS TYPES
# -------------------------------

BOSS_TYPES = [
    {
        "name": "spread",
        "fire_delay": 90,
        "bullets": 5,
        "pattern": "spread",
        "base_speed": 4
    },
    {
        "name": "aimed",
        "fire_delay": 75,
        "bullets": 1,
        "pattern": "aimed",
        "base_speed": 6
    },
    {
        "name": "wave",
        "fire_delay": 60,
        "bullets": 3,
        "pattern": "wave",
        "base_speed": 5
    },
    {
        "name": "rain",
        "fire_delay": 100,
        "bullets": 6,
        "pattern": "rain",
        "base_speed": 3
    },
    {
        "name": "spiral",
        "fire_delay": 5,
        "bullets": 1,
        "pattern": "spiral",
        "base_speed": 4
    },
    {
        "name": "burst",
        "fire_delay": 120,
        "bullets": 8,
        "pattern": "burst",
        "base_speed": 5
    },
    {
        "name": "sniper",
        "fire_delay": 150,
        "bullets": 1,
        "pattern": "sniper",
        "base_speed": 8
    },
]


# -------------------------------
#   MUSIC
# -------------------------------
try:
    pygame.mixer.init()
except Exception:
    # ignore if audio cannot be initialized in this environment
    pass

NORMAL_MUSIC = "muziek/normal_theme.mp3"
BOSS_MUSIC = "muziek/boss_theme.mp3"
try:
    death_sound = pygame.mixer.Sound("muziek/death.mp3")
except Exception:
    death_sound = None

try:
    laser_sound = pygame.mixer.Sound("muziek/laser.mp3")
    laser_sound.set_volume(0.1)
except Exception:
    laser_sound = None
# -------------------------------
#   SCORE OPSLAAN
# -------------------------------
def save_score(score):
    with open("textbestanden/scores.txt", "a") as f:
        f.write(str(score) + "\n")

# -------------------------------
#   death effect
# -------------------------------

def death_effect(screen, death_sound):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((200, 0, 0))

    death_sound.play()
    pygame.time.delay(150)

    for alpha in range(0, 160, 12):
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    overlay.fill((0, 0, 0))
    for alpha in range(0, 255, 10):
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(60)



# -------------------------------
#   VIS TEKENEN
# -------------------------------
def draw_player_fish(surface, fish, x, y, time):
    # support either a full path like "img/vis1.png" or a short name like "vis1"
    if fish.startswith("img/") or fish.startswith("img\\") or fish.endswith(".png"):
        path = fish
    else:
        path = os.path.join("img", fish + ".png")
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (FISH_W, FISH_H))
    surface.blit(image, (x, y))
    # kleine rotatie voor staart-zwiep
    angle = math.sin(time * 0.2) * 5   # 5 graden heen en weer

    rotated_image = pygame.transform.rotate(image, angle)
    rect = rotated_image.get_rect(center=(x + FISH_W//2, y + FISH_H//2))

    surface.blit(rotated_image, rect.topleft)


# -------------------------------
#   POWERUP INITIALIZER
# -------------------------------
def init_powers(active_power):
    godmode = active_power == "godmode"

    # shields
    if godmode:
        shield_hits = 2
    elif active_power == "shield":
        shield_hits = 1
    else:
        shield_hits = 0

    # laser start
    laser_active = godmode or active_power == "laser"
    laser_timer = 60 * FPS if godmode else (30 * FPS if active_power == "laser" else 0)

    # movement speed
    fish_speed = 5
    if active_power == "speed":
        fish_speed = 8
    if godmode:
        fish_speed = 10

    return godmode, shield_hits, laser_active, laser_timer, fish_speed


# -------------------------------
#   GAME ENTRY
# -------------------------------
def run_game(screen, fish, pattern, coin_manager):
    active_power = FISH_POWERUPS.get(fish, None)
    godmode, shield_hits, laser_active, laser_timer, fish_speed = init_powers(active_power)


    


   






    clock = pygame.time.Clock()
    # -------------------------------
    #   AUDIO (DEATH SOUND)
    # -------------------------------

    death_sound.set_volume(80)
    # start normale muziek bij game begin
    pygame.mixer.music.load(NORMAL_MUSIC)
    pygame.mixer.music.set_volume(80)
    pygame.mixer.music.play(-1)  # -1 = oneindig herhalen

    WIDTH, HEIGHT = screen.get_size()
    time = 0
    boss_direction = 1  # 1 = naar beneden, -1 = naar boven
    boss_speed_y = 1.5
    boss_bullets = []  # lijst voor de boss kogels
    BOSS_BULLET_SPEED = 5
    boss_fire_timer = 0  # frames tot volgende schot



    # speler
    player_x = 100
    player_y = HEIGHT // 2
    

    fish_speed = 5
    if active_power == "speed":
        fish_speed = 8
    if godmode:
        fish_speed = 10


    # afbeeldingen
    shark_image = pygame.image.load("img/shark.png").convert_alpha()
    shark_image = pygame.transform.scale(shark_image, SHARK_SIZE)

    chest_image = pygame.image.load("img/kist.png").convert_alpha()
    chest_image = pygame.transform.scale(chest_image, (50, 50))

    fluobeam_image = pygame.image.load("img/Fluobeam.png").convert_alpha()
    fluobeam_image = pygame.transform.scale(fluobeam_image, (20, 4))

    boss_bullet_image = pygame.image.load("img/boss_kogels.png").convert_alpha()
    boss_bullet_image = pygame.transform.scale(boss_bullet_image, (40,40))  # pas grootte aan indien nodig

    explosion_image = pygame.image.load("img/explosion.png").convert_alpha()
    explosion_image = pygame.transform.scale(explosion_image, (250, 250))

    boss_images = [
    pygame.image.load("img/blastoise.png").convert_alpha(),
    pygame.image.load("img/boss.png").convert_alpha(),
    pygame.image.load("img/gyarados.png").convert_alpha(),
    pygame.image.load("img/kraken.png").convert_alpha(),
    pygame.image.load("img/lapras.png").convert_alpha(),
    pygame.image.load("img/lochness.png").convert_alpha(),
    pygame.image.load("img/megalodon.png").convert_alpha()
]

    # schaal alle afbeeldingen naar dezelfde grootte
    boss_images = [pygame.transform.scale(img, BOSS_SIZE) for img in boss_images]



    # game objecten
    sharks = []
    laser_bullets = []   # 👈 TOEVOEGEN

    # Titanic event
    titanic_image = pygame.image.load("img/titanic.png").convert_alpha()
    titanic_rect = None
    titanic_active = False
    titanic_sunk = False

    titanic_spawn_score = 150

    # zinken
    titanic_sink_velocity = 0.0
    titanic_sink_accel = 0.1
    titanic_sink_max = 4

    # kantelen
    titanic_angle = 0.08
    titanic_tilt_speed = 0.015
    titanic_max_angle = 18   # graden



    
    fire_timer = 0
    chest_active = False
    chest_rect = None
    previous_chest_level = 0

    spawn_timer = 0
    spawn_delay = 90
    shark_speed = 4
    vertical_speed = 0.8

    # score & level
    score = 140
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
    boss_dying = False
    boss_explode_timer = 0
    boss_explosions = []
    dying_boss_rect = None
    current_boss = None
    boss_bullet_speed = 0




    # boss spawn elke 150 punten
    last_boss_score = 0

    font = pygame.font.SysFont(None, 32)
    big_font = pygame.font.SysFont(None, 56)



    # -------------------------------
    #   MAIN LOOP
    # -------------------------------
    while True:
        draw_background(screen, time, scroll=True)


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
                    if game_over and event.key == pygame.K_RETURN:
                        # 🔁 powers opnieuw initialiseren
                        godmode, shield_hits, laser_active, laser_timer, fish_speed = init_powers(active_power)

                        player_y = HEIGHT // 2
                        sharks.clear()
                        laser_bullets.clear()
                        boss_bullets.clear()

                        score = 0
                        score_timer = 0
                        level = 1
                        game_over = False

                        # 🔥 BELANGRIJK: boss reset
                        boss_active = False
                        boss_dying = False
                        boss_rect = None
                        dying_boss_rect = None
                        boss_explosions.clear()
                        boss_fire_timer = 0
                        boss_hp = 0
                        boss_max_hp = 0

                        # 🔥 DEZE WAS DE BUG
                        last_boss_score = 0

                        titanic_active = False
                        titanic_sunk = False
                        titanic_rect = None
                        titanic_angle = 0
                        titanic_sink_velocity = 0



                       

                        chest_active = False
                        chest_rect = None
                        previous_chest_level = 0

                        # 🎵 muziek reset
                        pygame.mixer.music.load(NORMAL_MUSIC)
                        pygame.mixer.music.play(-1)




        # -------------------------------
        #   GAME LOGICA
        # -------------------------------
        if not game_over:
            # score
            # score (pauze tijdens boss fight)
            if not boss_active:
                score_timer += 1
                if score >= titanic_spawn_score and not titanic_active:
                    titanic_active = True
                    titanic_rect = titanic_image.get_rect(
                        x=WIDTH + 40,
                        y=40
                    )
                    titanic_sink_velocity = 0.0
                    titanic_angle = 0.0
                    titanic_sunk = False


                if score_timer >= 30:
                    score_timer = 0                  
                    if godmode:
                        score += 3
                    elif active_power == "double_score":
                        score += 2
                    else:
                        score += 1




            chest_level = score // 20
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
                if active_power == "slow_enemies":
                    shark_speed *= 0.6
                spawn_delay = max(30, 90 - level * 5)
                boss_defeated_this_level = False


            # in de loop
            # boss spawn elke 50 punten
            if score >= last_boss_score + 50 and not boss_active:
                last_boss_score = score  # eerst bijwerken

                boss_active = True
                sharks.clear()

                pygame.mixer.music.fadeout(500)
                pygame.mixer.music.load(BOSS_MUSIC)
                pygame.mixer.music.play(-1)

                current_boss = random.choice(BOSS_TYPES)
                boss_image = random.choice(boss_images)

                boss_rect = boss_image.get_rect(
                    x=WIDTH + 40,
                    y=HEIGHT // 2 - boss_image.get_height() // 2
                )

                boss_max_hp = 6 + level * 2
                boss_hp = boss_max_hp

                boss_bullet_speed = current_boss["base_speed"] + level * 0.4
                boss_fire_timer = max(30, current_boss["fire_delay"] - level * 3)

            if titanic_active and titanic_rect:
                # meescrollen met achtergrond (zelfde snelheid)
                titanic_rect.x -= SCROLL_SPEED

                sand_y_mid = HEIGHT - 100

                if not titanic_sunk:
                    # versnellen tijdens zinken
                    titanic_sink_velocity += titanic_sink_accel
                    titanic_sink_velocity = min(titanic_sink_velocity, titanic_sink_max)

                    titanic_rect.y += titanic_sink_velocity

                    # kantelen tijdens zinken
                    if titanic_angle < titanic_max_angle:
                        titanic_angle -= titanic_tilt_speed

                    # bodem geraakt → afremmen
                    if titanic_rect.bottom >= sand_y_mid:
                        titanic_rect.bottom = sand_y_mid
                        titanic_sink_velocity *= 0.25   # demping
                        titanic_tilt_speed *= 0.6

                        # bijna stil → gestrand
                        if titanic_sink_velocity < 0.05:
                            titanic_sink_velocity = 0
                            titanic_sunk = True








            # speler beweging
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player_y -= fish_speed
            if keys[pygame.K_DOWN]:
                player_y += fish_speed
            player_y = max(0, min(HEIGHT - FISH_H, player_y))

            player_rect = pygame.Rect(player_x, player_y, FISH_W, FISH_H)

            if chest_active and chest_rect and chest_rect.colliderect(player_rect):
                # Grant temporary laser for 10s when opening a chest, but only
                # if a laser isn't already active and the previous power has finished.
                # This prevents overriding an existing power or godmode.
                if not laser_active:
                    laser_active = True
                    laser_timer = max(laser_timer, 10 * FPS)


                fire_timer = 0
                chest_active = False
                chest_rect = None

            # check coin collisions
            if coin_manager:
                if coin_manager.check_collision(player_rect):
                
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
                    if not game_over:
                        if shield_hits > 0:
                            shield_hits -= 1
                            sharks.remove(shark)
                        else:                        
                            game_over = True                 # Zet direct game_over
                            death_effect(screen, death_sound)
                            save_score(score)
                            scores.append(score)
                            highscore = max(scores)
                            pygame.mixer.music.fadeout(1000)



            # laser bullets
            can_shoot = laser_active or boss_active

            if can_shoot:
                fire_timer -= 1
                if fire_timer <= 0:
                    laser_bullets.append({
                        "rect": pygame.Rect(player_x + FISH_W, player_y + FISH_H//2 - 2, 20, 4),
                        "dx": 10,
                        "chain": 2 if active_power == "chain_shot" else 1
                    })
                    laser_sound.play()
                    fire_timer = int(0.1 * FPS) if godmode else (
                        int(0.25 * FPS) if active_power == "rapid_fire" else int(0.5 * FPS)
                    )

            # move bullets (handle legacy Rect bullets and dict bullets)
            for b in laser_bullets[:]:
                # convert legacy Rect entries to dict for backwards compatibility
                if isinstance(b, pygame.Rect):
                    idx = laser_bullets.index(b)
                    b = {"rect": b, "dx": 10, "chain": 1}
                    laser_bullets[idx] = b

                b["rect"].x += b.get("dx", 10)
                if b["rect"].left > WIDTH:
                    try:
                        laser_bullets.remove(b)
                    except ValueError:
                        pass
            
            # boss bullets

            for bullet in boss_bullets[:]:
                bullet["rect"].x += bullet["dx"]
                bullet["rect"].y += bullet["dy"]

                # verwijder als buiten scherm
                if bullet["rect"].right < 0 or bullet["rect"].left > WIDTH or bullet["rect"].top > HEIGHT or bullet["rect"].bottom < 0:
                    boss_bullets.remove(bullet)
                # check collision met speler
                elif bullet["rect"].colliderect(player_rect):
                    if not game_over:
                        game_over = True
                        # clear boss bullets when player dies from them
                        boss_bullets.clear()
                        death_effect(screen, death_sound)
                        save_score(score)
                        scores.append(score)
                        highscore = max(scores)
                        pygame.mixer.music.fadeout(1000)





            # collision bullets with sharks (chain-shot: kill first hit, then nearest, then stop)
            for b in laser_bullets[:]:
                br = b["rect"] if isinstance(b, dict) else (b if isinstance(b, pygame.Rect) else None)
                if br is None:
                    continue
                hit_any = False
                for shark in sharks[:]:
                    if br.colliderect(shark):
                        # kill the first shark hit
                        try:
                            sharks.remove(shark)
                        except ValueError:
                            pass
                        hit_any = True
                        # if chain remains, find nearest remaining shark and kill it as well
                        if b.get("chain", 1) > 1 and sharks:
                            sx, sy = br.centerx, br.centery
                            nearest = min(sharks, key=lambda s: (s.centerx - sx) ** 2 + (s.centery - sy) ** 2)
                            try:
                                sharks.remove(nearest)
                            except ValueError:
                                pass
                        # bullet stops after applying its chain hits
                        try:
                            laser_bullets.remove(b)
                        except ValueError:
                            pass
                        break

            # collision with boss
            if boss_active and boss_rect:
                for bullet in laser_bullets[:]:
                    # support dict bullets and legacy Rect bullets
                    if isinstance(bullet, dict):
                        brect = bullet.get("rect")
                        bullet_obj = bullet
                    elif isinstance(bullet, pygame.Rect):
                        brect = bullet
                        bullet_obj = bullet
                    else:
                        brect = None
                        bullet_obj = bullet

                    if brect and brect.colliderect(boss_rect):
                        damage = 5 if godmode else (2 if active_power == "boss_damage" else 1)
                        boss_hp -= damage

                        try:
                            laser_bullets.remove(bullet_obj)
                        except ValueError:
                            pass

                        if boss_hp <= 0 and not boss_dying:
                            boss_dying = True
                            boss_explode_timer = FPS
                            boss_bullets.clear()
                            dying_boss_rect = boss_rect.copy()  # 📍 positie vastzetten
                            # SOUND
                            explosion_sound = pygame.mixer.Sound("muziek/explosion.mp3")
                            pygame.mixer.music.set_volume(0.2)   # muziek dimmen
                            explosion_sound.set_volume(1.0)
                            explosion_sound.play()

                            


            if boss_active and boss_rect and current_boss:
                boss_fire_timer -= 1
                if boss_fire_timer <= 0:
                    pattern = current_boss["pattern"]

                    if pattern == "spread":
                        for i in range(5):
                            angle = -45 + i * (90 / 4)
                            rad = math.radians(angle)
                            boss_bullets.append({
                                "rect": pygame.Rect(boss_rect.center, (20,20)),
                                "dx": -boss_bullet_speed * math.cos(rad),
                                "dy": boss_bullet_speed * math.sin(rad)
                            })

                    elif pattern == "aimed":
                        dx = player_rect.centerx - boss_rect.centerx
                        dy = player_rect.centery - boss_rect.centery
                        dist = max(1, math.hypot(dx, dy))
                        boss_bullets.append({
                            "rect": pygame.Rect(boss_rect.center, (20,20)),
                            "dx": boss_bullet_speed * dx / dist,
                            "dy": boss_bullet_speed * dy / dist
                        })

                    elif pattern == "wave":
                        for i in range(3):
                            boss_bullets.append({
                                "rect": pygame.Rect(boss_rect.center, (20,20)),
                                "dx": -boss_bullet_speed,
                                "dy": math.sin(time * 0.1 + i) * 3
                            })

                    elif pattern == "rain":
                        for _ in range(6):
                            boss_bullets.append({
                                "rect": pygame.Rect(
                                    boss_rect.left,
                                    random.randint(0, HEIGHT),
                                    20, 20),
                                "dx": -boss_bullet_speed,
                                "dy": 0
                            })

                    elif pattern == "spiral":
                        angle = time * 0.15
                        boss_bullets.append({
                            "rect": pygame.Rect(boss_rect.center, (20,20)),
                            "dx": -boss_bullet_speed * math.cos(angle),
                            "dy": boss_bullet_speed * math.sin(angle)
                        })

                    elif pattern == "burst":
                        for _ in range(8):
                            ang = random.uniform(-60, 60)
                            rad = math.radians(ang)
                            boss_bullets.append({
                                "rect": pygame.Rect(boss_rect.center, (20,20)),
                                "dx": -boss_bullet_speed * math.cos(rad),
                                "dy": boss_bullet_speed * math.sin(rad)
                            })

                    elif pattern == "sniper":
                        dx = player_rect.centerx - boss_rect.centerx
                        dy = player_rect.centery - boss_rect.centery
                        dist = max(1, math.hypot(dx, dy))
                        boss_bullets.append({
                            "rect": pygame.Rect(boss_rect.center, (30,30)),
                            "dx": boss_bullet_speed * 1.5 * dx / dist,
                            "dy": boss_bullet_speed * 1.5 * dy / dist
                        })

                    boss_fire_timer = max(30, current_boss["fire_delay"] - level * 3)





            # boss gedrag
            if boss_active and boss_rect:
                if boss_rect.x > WIDTH - 220:
                    boss_rect.x -= 2

                # boss beweegt onafhankelijk op en neer
                boss_rect.y += boss_speed_y * boss_direction

                # keer om bij boven- of ondergrens
                if boss_rect.top <= 0:
                    boss_direction = 1
                elif boss_rect.bottom >= HEIGHT:
                    boss_direction = -1



                boss_rect.y = max(0, min(HEIGHT - boss_rect.height, boss_rect.y))

                if boss_rect.colliderect(player_rect):
                    if not game_over:
                        game_over = True
                        # clear boss bullets when player collides with boss
                        boss_bullets.clear()
                        death_effect(screen, death_sound)
                        save_score(score)
                        scores.append(score)
                        highscore = max(scores)
                        pygame.mixer.music.fadeout(1000)
            
            if boss_dying and dying_boss_rect:
                boss_explode_timer -= 1

                if boss_explode_timer % 6 == 0:
                    # spawn explosions centered on the boss area (not beside it)
                    cx = dying_boss_rect.centerx
                    cy = dying_boss_rect.centery
                    ex_w, ex_h = explosion_image.get_size()
                    max_off_x = max(0, dying_boss_rect.width // 2)
                    max_off_y = max(0, dying_boss_rect.height // 2)
                    off_x = random.randint(-max_off_x, max_off_x)
                    off_y = random.randint(-max_off_y, max_off_y)
                    ex = int(cx + off_x - ex_w // 2)
                    ey = int(cy + off_y - ex_h // 2)
                    boss_explosions.append([ex, ey, 15])


                if boss_explode_timer <= 0:
                    boss_dying = False
                    boss_active = False
                    boss_rect = None
                    dying_boss_rect = None
                    boss_explosions.clear()

                    pygame.mixer.music.fadeout(500)
                    pygame.mixer.music.load(NORMAL_MUSIC)
                    pygame.mixer.music.play(-1)



            # -------------------------------
            #   TEKENEN
            # -------------------------------
            # Titanic tekenen (achter voorgrond, vóór player)
            if titanic_active and titanic_rect:
                rotated = pygame.transform.rotate(titanic_image, -titanic_angle)
                r_rect = rotated.get_rect(center=titanic_rect.center)
                screen.blit(rotated, r_rect.topleft)


            draw_player_fish(screen, fish, player_x, player_y, time)
            def draw_shark(surface, image, rect, time):
                # haaien wiebelen agressiever
                angle = math.sin(time * 0.3 + rect.y * 0.1) * 6

                rotated = pygame.transform.rotate(image, angle)
                new_rect = rotated.get_rect(center=rect.center)

                surface.blit(rotated, new_rect.topleft)


            if chest_active and chest_rect:
                screen.blit(chest_image, chest_rect)

            if coin_manager:
                coin_manager.draw(screen)

            for bullet in laser_bullets:
                # bullets may be legacy Rects or dicts with a 'rect' key
                if isinstance(bullet, dict):
                    rect = bullet.get("rect")
                elif isinstance(bullet, pygame.Rect):
                    rect = bullet
                else:
                    rect = None
                if rect:
                    screen.blit(fluobeam_image, rect)

            for shark in sharks:
                draw_shark(screen, shark_image, shark, time)


            if boss_active and boss_rect and not boss_dying:
                screen.blit(boss_image, boss_rect)


            for bullet in boss_bullets:
                screen.blit(boss_bullet_image, bullet["rect"])


                # HP balk
                bar_w = 200
                pygame.draw.rect(screen, (255, 0, 0),
                                 (WIDTH // 2 - bar_w // 2, 20, bar_w, 16))
                pygame.draw.rect(screen, (0, 255, 0),
                                 (WIDTH // 2 - bar_w // 2, 20,
                                  int(bar_w * boss_hp / boss_max_hp), 16))
            for explosion in boss_explosions[:]:
                x, y, life = explosion
                screen.blit(explosion_image, (x, y))
                explosion[2] -= 1
                if explosion[2] <= 0:
                    boss_explosions.remove(explosion)


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
            if active_power:
                screen.blit(
                    font.render(f"Skin power: {active_power}", True, (255, 255, 0)),
                    (hud_x, hud_y + idx * line_h)
                )
                idx += 1
            if godmode:
                screen.blit(
                    font.render("GODMODE ACTIVE", True, (255, 0, 0)),
                    (hud_x, hud_y + idx * line_h)
                )
                idx += 1
            if shield_hits > 0:
                screen.blit(
                    font.render(f"Shields: {shield_hits}", True, (0, 200, 255)),
                    (hud_x, hud_y + idx * line_h)
                )
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
            screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)),
                        (WIDTH // 2 - 70, 180))
            screen.blit(font.render(f"Highscore: {highscore}", True, (255, 255, 255)),
                        (WIDTH // 2 - 70, 200))
            # draw three key images (enter, esc, tab) centered with labels under each
            key_size = (88, 52)
            spacing = 28
            # safe loader: returns surface or None
            def _load_key(name):
                path = os.path.join("img", name)
                if os.path.exists(path):
                    try:
                        im = pygame.image.load(path).convert_alpha()
                        return pygame.transform.scale(im, key_size)
                    except Exception:
                        return None
                return None

            enter_img = _load_key("enter.png")
            esc_img = _load_key("esc.png")
            tab_img = _load_key("tab.png")

            labels = ["= opnieuw", "= Terug naar menu", "= Terug naar locker"]
            symbols = ["⏎", "⎋", "⇥"]

            # stack the three keys vertically and put labels to the right of each
            # adjust offsets to move icons a bit left and down
            left_offset = 40
            down_offset = 40
            col_x = WIDTH // 2 - key_size[0] // 2 - left_offset
            top_y = 220 + down_offset
            vert_spacing = key_size[1] + 24

            for i, (img, sym, label) in enumerate(zip((enter_img, esc_img, tab_img), symbols, labels)):
                y = top_y + i * vert_spacing
                x = col_x
                if img:
                    rect = img.get_rect(topleft=(x, y))
                    screen.blit(img, rect.topleft)
                else:
                    rect = pygame.Rect(x, y, key_size[0], key_size[1])
                    pygame.draw.rect(screen, (240, 240, 240), rect, border_radius=6)
                    pygame.draw.rect(screen, (50, 50, 50), rect, 2, border_radius=6)
                    sym_surf = big_font.render(sym, True, (20, 20, 20))
                    screen.blit(sym_surf, sym_surf.get_rect(center=rect.center).topleft)

                # draw label to the right of the key, vertically centered
                label_surf = font.render(label, True, (255, 255, 255))
                label_x = rect.right + 12
                label_y = rect.centery - label_surf.get_height() // 2
                screen.blit(label_surf, (label_x, label_y))
            

        pygame.display.flip()
        clock.tick(FPS)