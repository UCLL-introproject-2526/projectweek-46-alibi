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
# parallax layers
bubbles = []
plants_far = []
plants_mid = []
plants_near = []
stones_far = []
stones_mid = []
stones_near = []
sand_grains = []


def _draw_seaweed(surface, x, base_y, height, wiggle, time, color=(40,120,90), max_thickness=5, segments=10):
    # draw a curved seaweed made of short segments, thicker at base
    points = []
    for i in range(segments + 1):
        t = i / segments
        y = base_y - int(t * height)
        # amplitude reduces toward the top
        amp = (1 - t) * 12
        dx = math.sin(time * wiggle + i * 0.5) * amp
        x_pos = int(x + dx)
        points.append((x_pos, y))

    # draw segments with tapering thickness
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        t = i / segments
        thick = max(1, int(max_thickness * (1 - t)))
        pygame.draw.line(surface, color, p1, p2, thick)


def _init_background_for_size(width, height):
    global _bg_initialized, _bg_width, _bg_height, scroll_x
    global bubbles, plants_far, plants_mid, plants_near
    global stones_far, stones_mid, stones_near, sand_grains
    _bg_width = width
    _bg_height = height
    scroll_x = 0

    # bubbles with depth (z in 0.3..1.0; lower z = further away)
    bubbles = []
    for _ in range(90):
        z = random.uniform(0.35, 1.0)
        bubbles.append({
            "x": random.randint(0, width),
            "y": random.randint(max(0, height - 200), height),
            "z": z,
            "speed": random.uniform(0.2, 1.8) * z,
            "size": max(1, int(1 + (1 - z) * 6))
        })

    # define sand band vertical positions and heights so stones can be anchored
    sand_y_far = height - 140
    sand_h_far = 40
    sand_y_mid = height - 100
    sand_h_mid = 40
    sand_y_near = height - 60
    sand_h_near = 60

    # stones and plants split into far/mid/near layers
    stones_far = []
    stones_mid = []
    stones_near = []
    for _ in range(14):
        w_st = random.randint(20, min(80, width // 6))
        h_st = random.randint(10, min(40, height // 6))
        # anchor stone bottom onto the far sand band so it never floats in water
        y_pos = sand_y_far + sand_h_far - h_st - random.randint(0, 4)
        stones_far.append({
            "x": random.randint(0, width),
            "y": y_pos,
            "w": w_st,
            "h": h_st,
            "color": (50, 70, 80)
        })
    for _ in range(12):
        w_st = random.randint(40, min(140, width // 3))
        h_st = random.randint(20, min(60, height // 3))
        y_pos = sand_y_near + sand_h_near - h_st - random.randint(0, 6)
        stones_near.append({
            "x": random.randint(0, width),
            "y": y_pos,
            "w": w_st,
            "h": h_st,
            "color": (
                random.randint(60, 90),
                random.randint(60, 80),
                random.randint(60, 80)
            )
        })

    for _ in range(10):
        w_st = random.randint(30, min(100, width // 4))
        h_st = random.randint(15, min(50, height // 4))
        y_pos = sand_y_mid + sand_h_mid - h_st - random.randint(0, 5)
        stones_mid.append({
            "x": random.randint(0, width),
            "y": y_pos,
            "w": w_st,
            "h": h_st,
            "color": (
                random.randint(55, 85),
                random.randint(65, 85),
                random.randint(65, 85)
            )
        })

    plants_far = []
    plants_mid = []
    plants_near = []
    for _ in range(30):
        x = random.randint(0, width)
        h = random.randint(30, int(height * 0.25))
        plants_far.append((x, h, random.uniform(0.005, 0.03)))
    for _ in range(36):
        x = random.randint(0, width)
        h = random.randint(40, int(height * 0.35))
        plants_mid.append((x, h, random.uniform(0.01, 0.05)))
    for _ in range(28):
        x = random.randint(0, width)
        h = random.randint(60, int(height * 0.5))
        plants_near.append((x, h, random.uniform(0.02, 0.06)))

    # sand grains for texture (z depth influences size & parallax)
    sand_grains = []
    for _ in range(300):
        z = random.uniform(0.6, 1.0)
        gx = random.randint(0, width)
        gy = random.randint(max(0, height - 140), height - 5)
        sand_grains.append({
            "x": gx,
            "y": gy,
            "z": z,
            "size": max(1, int((1 - z) * 3 + 1)),
            "col": (200 - int((1 - z) * 40), 180 - int((1 - z) * 30), 140 - int((1 - z) * 20))
        })

    _bg_initialized = True


def draw_background(screen, time):
    global scroll_x, _bg_initialized, _bg_width, _bg_height
    w, h = screen.get_size()

    # initialize or reinitialize background when resolution changes
    if not _bg_initialized or (w != _bg_width or h != _bg_height):
        _init_background_for_size(w, h)

    screen.fill((8, 30, 70))

    # scrolling update (keep increasing to avoid teleporting)
    scroll_x += SCROLL_SPEED
    base_offset = -scroll_x

    # Far layer (slow parallax)
    m = 0.35
    sand_y_far = h - 140
    # draw tiled sand band (draw three tiles to guarantee coverage)
    offset = int((base_offset * m) % w)
    for tile in (-1, 0, 1):
        layer_offset = offset + tile * w
        pygame.draw.rect(screen, (175, 150, 110), (layer_offset, sand_y_far, w, 40))
    for x, ph, wiggle in plants_far:
        px = int((x + base_offset * m) % w)
        # slightly reduce coral size for a subtler appearance
        draw_h = int((ph * 0.5 + 30) * 0.92)
        for tile in (-1, 0, 1):
            _draw_seaweed(screen, px + tile * w, sand_y_far + 30, draw_h, wiggle * 0.6, time * 0.02, color=(60,90,100), max_thickness=2, segments=8)
    for s in stones_far:
        px = int((s["x"] + base_offset * m) % w)
        for tile in (-1, 0, 1):
            bx = px + tile * w
            # shadow for depth
            shadow = (10, 10, 12)
            pygame.draw.ellipse(screen, shadow, (bx + 3, s["y"] + 3, s["w"], s["h"]))
            # main stone
            pygame.draw.ellipse(screen, s["color"], (bx, s["y"], s["w"], s["h"]))
            # small highlight to give form
            hl = (min(255, s["color"][0] + 30), min(255, s["color"][1] + 30), min(255, s["color"][2] + 30))
            pygame.draw.ellipse(screen, hl, (bx + s["w"] // 4, s["y"] + s["h"] // 8, max(2, s["w"] // 4), max(2, s["h"] // 4)))

    # Mid layer
    m = 0.65
    sand_y_mid = h - 100
    offset = int((base_offset * m) % w)
    for tile in (-1, 0, 1):
        layer_offset = offset + tile * w
        pygame.draw.rect(screen, (185, 160, 120), (layer_offset, sand_y_mid, w, 40))
    for x, ph, wiggle in plants_mid:
        px = int((x + base_offset * m) % w)
        draw_h = int((ph * 0.75 + 40) * 0.92)
        for tile in (-1, 0, 1):
            _draw_seaweed(screen, px + tile * w, sand_y_mid + 25, draw_h, wiggle * 0.9, time * 0.03, color=(45,100,80), max_thickness=3, segments=10)
    for s in stones_mid:
        px = int((s["x"] + base_offset * m) % w)
        for tile in (-1, 0, 1):
            bx = px + tile * w
            shadow = (12, 12, 14)
            pygame.draw.ellipse(screen, shadow, (bx + 3, s["y"] + 3, s["w"], s["h"]))
            pygame.draw.ellipse(screen, s["color"], (bx, s["y"], s["w"], s["h"]))
            hl = (min(255, s["color"][0] + 28), min(255, s["color"][1] + 28), min(255, s["color"][2] + 28))
            pygame.draw.ellipse(screen, hl, (bx + s["w"] // 4, s["y"] + s["h"] // 8, max(2, s["w"] // 4), max(2, s["h"] // 4)))

    # Near layer
    m = 1.0
    sand_y_near = h - 60
    offset = int((base_offset * m) % w)
    for tile in (-1, 0, 1):
        layer_offset = offset + tile * w
        pygame.draw.rect(screen, (195, 175, 135), (layer_offset, sand_y_near, w, 60))
    for s in stones_near:
        px = int((s["x"] + base_offset * m) % w)
        for tile in (-1, 0, 1):
            bx = px + tile * w
            shadow = (14, 14, 16)
            pygame.draw.ellipse(screen, shadow, (bx + 3, s["y"] + 3, s["w"], s["h"]))
            pygame.draw.ellipse(screen, s["color"], (bx, s["y"], s["w"], s["h"]))
            hl = (min(255, s["color"][0] + 26), min(255, s["color"][1] + 26), min(255, s["color"][2] + 26))
            pygame.draw.ellipse(screen, hl, (bx + s["w"] // 4, s["y"] + s["h"] // 8, max(2, s["w"] // 4), max(2, s["h"] // 4)))
    for x, ph, wiggle in plants_near:
        px = int((x + base_offset * m) % w)
        draw_h = int((ph + 50) * 0.94)
        for tile in (-1, 0, 1):
            _draw_seaweed(screen, px + tile * w, h - 10, draw_h, wiggle * 1.1, time * 0.04, color=(40,120,90), max_thickness=5, segments=12)

    # Bubbles (sorted by depth)
    sorted_bubs = sorted(bubbles, key=lambda b: b["z"])
    for b in sorted_bubs:
        b["y"] -= b["speed"]
        if b["y"] < 0:
            b["y"] = h - 20
            b["x"] = random.randint(0, w)
        mult = 0.2 + 0.8 * (1 - b["z"])  # parallax factor
        px = int((b["x"] + base_offset * mult) % w)
        for tile in (-1, 0, 1):
            pygame.draw.circle(screen, (200,220,255), (px + tile * w, int(b["y"])), b["size"]) 

    # sand grains (texture) - draw last so they appear on top of sand bands
    for g in sand_grains:
        mult = 0.2 + 0.8 * (1 - g["z"]) 
        px = int((g["x"] + base_offset * mult) % w)
        for tile in (-1, 0, 1):
            pygame.draw.rect(screen, g["col"], (px + tile * w, int(g["y"]), g["size"], g["size"]))

    # subtle fog overlay at top to push far layers back
    fog = pygame.Surface((w, h // 3), pygame.SRCALPHA)
    fog.fill((8, 30, 70, 80))
    screen.blit(fog, (0, 0))
