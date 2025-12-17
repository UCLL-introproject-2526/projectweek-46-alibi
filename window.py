import pygame
import random
import math

# Dynamic background that adapts to the current screen size (fullscreen)
scroll_x = 0
SCROLL_SPEED = 6

# background data (will be initialized for the current screen size)
_bg_initialized = False
_bg_width = 0
_bg_height = 0
bubbles = []
stones = []
plants = []


def _init_background_for_size(width, height):
    global _bg_initialized, _bg_width, _bg_height, bubbles, stones, plants, scroll_x
    _bg_width = width
    _bg_height = height
    scroll_x = 0

    bubbles = [{
        "x": random.randint(0, width),
        "y": random.randint(max(0, height - 200), height),
        "speed": random.uniform(0.6, 1.8),
        "size": random.randint(3, 8)
    } for _ in range(45)]

    stones = [{
        "x": random.randint(0, width),
        "y": random.randint(max(0, height - 120), max(0, height - 50)),
        "w": random.randint(40, min(120, width // 2)),
        "h": random.randint(20, min(60, height // 2)),
        "color": (
            random.randint(60, 90),
            random.randint(60, 80),
            random.randint(60, 80)
        )
    } for _ in range(18)]

    plants = []
    for _ in range(45):
        x = random.randint(0, width)
        h = random.randint(40, min(140, height - 100))
        wiggle = random.uniform(0.015, 0.05)
        plants.append((x, h, wiggle))

    _bg_initialized = True


def draw_background(screen, time):
    global scroll_x, _bg_initialized, _bg_width, _bg_height
    w, h = screen.get_size()

    # initialize or reinitialize background when resolution changes
    if not _bg_initialized or (w != _bg_width or h != _bg_height):
        _init_background_for_size(w, h)

    screen.fill((8, 30, 70))

    # Lichtdeeltjes (random per-frame but constrained to screen size)
    for i in range(180):
        px = random.randint(0, w)
        py = (random.randint(0, h) + time) % max(1, h)
        # safe guard: don't draw outside
        if 0 <= px < w and 0 <= py < h:
            screen.set_at((px, py), (70, 120, 170))

    # scrolling update
    scroll_x -= SCROLL_SPEED
    if scroll_x <= -w:
        scroll_x = 0

    # draw two tiled layers so it scrolls seamlessly
    for layer_offset in (scroll_x, scroll_x + w):

        # Bodem
        pygame.draw.rect(screen, (170, 150, 110), (layer_offset, h - 140, w, 140))

        # Stenen
        for s in stones:
            pygame.draw.ellipse(screen, s["color"], (s["x"] + layer_offset, s["y"], s["w"], s["h"]))

        # Planten
        for x, ph, wiggle in plants:
            top_x = x + math.sin(time * wiggle) * (5 + ph * 0.05)
            pygame.draw.line(
                screen,
                (40, 120, 90),
                (x + layer_offset, h - 10),
                (top_x + layer_offset, h - 140 + (140 - ph)),
                5 if ph > 90 else 3
            )

    # Bubbels (blijven op plaats, maar move up over time)
    for b in bubbles:
        b["y"] -= b["speed"]
        if b["y"] < 0:
            b["y"] = h - 20
            b["x"] = random.randint(0, w)
        if 0 <= int(b["x"]) < w and 0 <= int(b["y"]) < h:
            pygame.draw.circle(screen, (200, 220, 255), (int(b["x"]), int(b["y"])), b["size"])
