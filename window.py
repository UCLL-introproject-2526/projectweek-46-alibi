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

    # --- VISTEKENINGEN ---

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

    def create_fish():
        y_position = random.choice([
            random.randint(80, 250),
            random.randint(450, 600)
        ])

        return {
            "x": random.randint(-300, 1300),
            "y": y_position,
            "speed": random.uniform(1.2, 3.0),
            "dir": random.choice([1, -1]),
            "type": random.choice(fish_types),
            "scale": random.uniform(0.8, 1.3)
        }

    fishes = [create_fish() for _ in range(12)]

    # Planten
    plants = []
    for _ in range(45):
        x = random.randint(0, width)
        h = random.randint(40, 140)
        wiggle = random.uniform(0.015, 0.05)
        plants.append((x, h, wiggle))

    # --- MAIN LOOP ---
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((10, 40, 80))

        # Lichtdeeltjes
        for i in range(180):
            px = random.randint(0, width)
            py = (random.randint(0, height) + time) % 650
            screen.set_at((px, py), (80, 130, 180))

        # Bodem
        pygame.draw.rect(screen, (180, 165, 120), (0, height - 140, width, 140))

        # Planten
        for x, h, wiggle in plants:
            top_x = x + math.sin(time * wiggle) * (5 + h * 0.05)
            pygame.draw.line(
                screen,
                (40, 130, 90),
                (x, height - 20),
                (top_x, height - 140 + (140 - h)),
                5 if h > 90 else 3
            )

        # Vissen bewegen + tekenen
        for fish in fishes:
            fish["x"] += fish["speed"] * fish["dir"]

            if fish["dir"] == 1 and fish["x"] > 1300:
                fish.update(create_fish())
            elif fish["dir"] == -1 and fish["x"] < -300:
                fish.update(create_fish())

            flip = (fish["dir"] == -1)
            fish["type"](screen, fish["x"], fish["y"], fish["scale"], flip)

        time += 1
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

create_main_surface()