import pygame
import random
import math

WIDTH, HEIGHT = 1024, 768
scroll_x = 0   # globale variabele
SCROLL_SPEED = 6  # hoe snel je "vooruit" gaat


# -----------------------------
#   ACHTERGROND DATA (1x)
# -----------------------------

bubbles = [{
    "x": random.randint(0, WIDTH),
    "y": random.randint(HEIGHT - 200, HEIGHT),
    "speed": random.uniform(0.6, 1.8),
    "size": random.randint(3, 8)
} for _ in range(45)]

stones = [{
    "x": random.randint(0, WIDTH),
    "y": random.randint(HEIGHT - 120, HEIGHT - 50),
    "w": random.randint(40, 120),
    "h": random.randint(20, 60),
    "color": (
        random.randint(60, 90),
        random.randint(60, 80),
        random.randint(60, 80)
    )
} for _ in range(18)]

plants = []
for _ in range(45):
    x = random.randint(0, WIDTH)
    h = random.randint(40, 140)
    wiggle = random.uniform(0.015, 0.05)
    plants.append((x, h, wiggle))


# -----------------------------
#   ACHTERGROND TEKEN FUNCTIE
# -----------------------------

def draw_background(screen, time):
    global scroll_x
    screen.fill((8, 30, 70))

    # Lichtdeeltjes
    for i in range(180):
        px = random.randint(0, WIDTH)
        py = (random.randint(0, HEIGHT) + time) % 650
        screen.set_at((px, py), (70, 120, 170))

    # --- SCROLLING UPDATE ---
    scroll_x -= SCROLL_SPEED
    if scroll_x <= -WIDTH:
        scroll_x = 0

    # --- BODEM + STENEN + PLANTEN TWEE KEER TEKENEN ---
    for layer_offset in (scroll_x, scroll_x + WIDTH):

        # Bodem
        pygame.draw.rect(screen, (170, 150, 110),
                         (layer_offset, HEIGHT - 140, WIDTH, 140))

        # Stenen
        for s in stones:
            pygame.draw.ellipse(screen,
                                s["color"],
                                (s["x"] + layer_offset,
                                 s["y"],
                                 s["w"],
                                 s["h"]))

        # Planten
        for x, h, wiggle in plants:
            top_x = x + math.sin(time * wiggle) * (5 + h * 0.05)
            pygame.draw.line(
                screen,
                (40, 120, 90),
                (x + layer_offset, HEIGHT - 10),
                (top_x + layer_offset, HEIGHT - 140 + (140 - h)),
                5 if h > 90 else 3
            )

    # Bubbels (blijven op plaats)
    for b in bubbles:
        b["y"] -= b["speed"]
        if b["y"] < 0:
            b["y"] = HEIGHT - 20
            b["x"] = random.randint(0, WIDTH)
        pygame.draw.circle(screen,
                           (200, 220, 255),
                           (int(b["x"]), int(b["y"])),
                           b["size"])
