import pygame
import random
import math

def create_main_surface():
    pygame.init()

    width, height = 1024, 768
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Deep Sea")

    clock = pygame.time.Clock()
    running = True
    time = 0

    # -------------------------------------------------
    #                   VIS TEKEN FUNCTIES
    # -------------------------------------------------

    def draw_clownfish(surface, x, y, scale=1, flip=False):
        color = (255, 120, 0)
        white = (245, 245, 245)
        black = (0, 0, 0)

        body = pygame.Surface((120*scale, 70*scale), pygame.SRCALPHA)

        pygame.draw.ellipse(body, color, (10*scale, 15*scale, 90*scale, 40*scale))
        pygame.draw.rect(body, white, (30*scale, 18*scale, 12*scale, 35*scale))
        pygame.draw.rect(body, white, (65*scale, 18*scale, 12*scale, 35*scale))

        pygame.draw.polygon(body, color,
            [(10*scale, 35*scale), (0, 20*scale), (0, 50*scale)]
        )
        pygame.draw.polygon(body, color,
            [(50*scale, 15*scale), (60*scale, 0), (70*scale, 15*scale)]
        )

        pygame.draw.circle(body, black, (95*scale, 35*scale), 4*scale)

        if flip:
            body = pygame.transform.flip(body, True, False)
        surface.blit(body, (x, y))

    def draw_bluetang(surface, x, y, scale=1, flip=False):
        blue = (30, 80, 200)
        yellow = (250, 220, 0)
        black = (0, 0, 0)

        body = pygame.Surface((140*scale, 70*scale), pygame.SRCALPHA)

        pygame.draw.ellipse(body, blue, (10*scale, 15*scale, 110*scale, 40*scale))
        pygame.draw.polygon(body, yellow,
            [(10*scale, 35*scale), (0, 20*scale), (0, 50*scale)]
        )
        pygame.draw.polygon(body, blue,
            [(50*scale, 15*scale), (65*scale, 0), (80*scale, 15*scale)]
        )

        pygame.draw.circle(body, black, (95*scale, 35*scale), 4*scale)

        if flip:
            body = pygame.transform.flip(body, True, False)
        surface.blit(body, (x, y))

    def draw_yellowfish(surface, x, y, scale=1, flip=False):
        yellow = (250, 230, 40)
        black = (0,0,0)

        body = pygame.Surface((120*scale, 60*scale), pygame.SRCALPHA)

        pygame.draw.ellipse(body, yellow, (10*scale, 15*scale, 90*scale, 35*scale))
        pygame.draw.polygon(body, yellow,
            [(10*scale, 35*scale), (0, 20*scale), (0, 50*scale)]
        )
        pygame.draw.polygon(body, yellow,
            [(40*scale, 15*scale), (50*scale, 0), (60*scale, 15*scale)]
        )

        pygame.draw.circle(body, black, (85*scale, 30*scale), 4*scale)

        if flip:
            body = pygame.transform.flip(body, True, False)
        surface.blit(body, (x, y))

    fish_types = [draw_clownfish, draw_bluetang, draw_yellowfish]

    # -------------------------------------------------
    #                 REALISTISCHE KWAL (verder weg)
    # -------------------------------------------------

    def draw_jellyfish(surface, x, y, size=0.6):   # kleiner = verder weg
        purple = (140, 70, 200)
        dark = (90, 30, 130)

        body = pygame.Surface((140*size, 160*size), pygame.SRCALPHA)

        # Kop
        pygame.draw.ellipse(body, purple, (0, 0, 140*size, 80*size))
        pygame.draw.ellipse(body, dark, (10*size, 10*size, 120*size, 60*size), 2)

        # Tentakels (minder contrast)
        for i in range(8):
            start_x = 20*size + i * 15*size
            for t in range(20):
                tx = start_x + math.sin((t/3) + time*0.04 + i) * 3
                ty = 80*size + t*4*size
                pygame.draw.circle(body, purple, (int(tx), int(ty)), int(2*size))

        surface.blit(body, (x, y))

    # -------------------------------------------------
    #                    BUBBELS
    # -------------------------------------------------

    bubbles = []
    for _ in range(45):
        bubbles.append({
            "x": random.randint(0, width),
            "y": random.randint(height - 200, height),
            "speed": random.uniform(0.6, 1.8),
            "size": random.randint(3, 8)
        })

    # -------------------------------------------------
    #                    STENEN
    # -------------------------------------------------

    stones = []
    for _ in range(18):
        stones.append({
            "x": random.randint(0, width),
            "y": random.randint(height - 120, height - 50),
            "w": random.randint(40, 120),
            "h": random.randint(20, 60),
            "color": (
                random.randint(60, 90),
                random.randint(60, 80),
                random.randint(60, 80)
            )
        })

    # -------------------------------------------------
    #                    VISSEN (spawnen enkel aan randen)
    # -------------------------------------------------

    def create_fish():
        side = random.choice(["left", "right"])

        if side == "left":
            x = random.randint(-350, -120)
            dir = 1
        else:
            x = random.randint(width + 120, width + 350)
            dir = -1

        return {
            "x": x,
            "y": random.choice([
                random.randint(120, 260),
                random.randint(350, 480)
            ]),
            "speed": random.uniform(0.8, 2.2),
            "dir": dir,
            "type": random.choice(fish_types),
            "scale": random.uniform(0.6, 1.0)
        }

    fishes = [create_fish() for _ in range(20)]

    # -------------------------------------------------
    #                    KWAL DATA
    # -------------------------------------------------

    jelly_x = 420
    jelly_y = 260     # verder naar achter → hoger in beeld
    jelly_dir = 1

    # -------------------------------------------------
    #                    PLANTEN
    # -------------------------------------------------

    plants = []
    for _ in range(45):
        x = random.randint(0, width)
        h = random.randint(40, 140)
        wiggle = random.uniform(0.015, 0.05)
        plants.append((x, h, wiggle))

    # -------------------------------------------------
    #                   MAIN LOOP
    # -------------------------------------------------

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((8, 30, 70))

        # Lichtdeeltjes
        for i in range(180):
            px = random.randint(0, width)
            py = (random.randint(0, height) + time) % 650
            screen.set_at((px, py), (70, 120, 170))

        # Bodem
        pygame.draw.rect(screen, (170, 150, 110), (0, height - 140, width, 140))

        # Stenen
        for s in stones:
            pygame.draw.ellipse(screen, s["color"],
                                (s["x"], s["y"], s["w"], s["h"]))

        # Planten
        for x, h, wiggle in plants:
            top_x = x + math.sin(time * wiggle) * (5 + h * 0.05)
            pygame.draw.line(
                screen,
                (40, 120, 90),
                (x, height - 10),
                (top_x, height - 140 + (140 - h)),
                5 if h > 90 else 3
            )

        # Bubbels
        for b in bubbles:
            b["y"] -= b["speed"]
            if b["y"] < 0:
                b["y"] = height - 20
                b["x"] = random.randint(0, width)
            pygame.draw.circle(screen, (200, 220, 255),
                               (int(b["x"]), int(b["y"])), b["size"])

        # Vissen (respawn enkel aan rand)
        for fish in fishes:
            fish["x"] += fish["speed"] * fish["dir"]

            if fish["dir"] == 1 and fish["x"] > width + 300:
                fish.update(create_fish())
            elif fish["dir"] == -1 and fish["x"] < -300:
                fish.update(create_fish())

            flip = (fish["dir"] == -1)
            fish["type"](screen, fish["x"], fish["y"], fish["scale"], flip)

        # KWAL verder weg, lichte beweging
        jelly_y += jelly_dir * 0.3
        if jelly_y < 220 or jelly_y > 300:
            jelly_dir *= -1

        draw_jellyfish(screen, jelly_x, jelly_y, 0.6)

        time += 1
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

create_main_surface()
