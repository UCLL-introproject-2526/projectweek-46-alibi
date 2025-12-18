import pygame
import random
import math
from pygame.locals import *

# ===============================
# CONFIG
# ===============================
ENRAGE_THRESHOLD = 0.30
ENRAGE_HP_MULT = 2.0

SNIPER_CD = 85
BURST_CD = 90
WAVE_CD = 70
SPIRAL_CD = 6
SUMMON_CD = 240

MINE_FUSE = 60
MINE_FALL_SPEED = 4

# ===============================
# SPAWN HELPERS
# ===============================

def spawn_sniper(boss_rect, boss_bullets, player_rect, speed):
    sx, sy = boss_rect.center
    px, py = player_rect.center
    dx, dy = px - sx, py - sy
    length = max(1, math.hypot(dx, dy))
    boss_bullets.append({
        "rect": pygame.Rect(sx, sy, 20, 20),
        "dx": (dx / length) * speed,
        "dy": (dy / length) * speed
    })


def spawn_burst(boss_rect, boss_bullets, speed):
    for off in (-30, 0, 30):
        boss_bullets.append({
            "rect": pygame.Rect(boss_rect.centerx, boss_rect.centery + off, 20, 20),
            "dx": -speed,
            "dy": 0
        })


def spawn_wave(boss_rect, boss_bullets, speed):
    boss_bullets.append({
        "rect": pygame.Rect(boss_rect.centerx, boss_rect.centery, 20, 20),
        "dx": -speed,
        "dy": 0,
        "wave": True,
        "t": 0,
        "base_y": boss_rect.centery
    })


def spawn_spiral(boss_rect, boss_bullets, speed, angle):
    rad = math.radians(angle)
    boss_bullets.append({
        "rect": pygame.Rect(boss_rect.centerx, boss_rect.centery, 18, 18),
        "dx": -speed * math.cos(rad),
        "dy": speed * math.sin(rad)
    })


def spawn_mine(boss_rect, mines):
    mines.append({
        "rect": pygame.Rect(boss_rect.left - 10, boss_rect.centery, 22, 22),
        "timer": MINE_FUSE
    })

# ===============================
# INIT BOSS STATE
# ===============================

def create_boss_state(attack_a, attack_b, fps):
    """
    Maak boss-state aan bij spawn
    """
    return {
        "attack_a": attack_a,
        "attack_b": attack_b,
        "current": attack_a,
        "switch_time": 4 * fps,
        "switch_timer": 4 * fps,
        "fire_timer": 30,
        "burst_count": 0,
        "spiral_angle": 0,
        "enraged": False,
        "speed_mult": 1.0,
        "mines": []
    }

# ===============================
# UPDATE BOSS FIGHT (CALL EACH FRAME)
# ===============================

def update_boss_fight(
    boss_rect,
    boss_hp,
    boss_max_hp,
    boss_bullets,
    player_rect,
    sharks,
    shark_image,
    bullet_speed,
    state
):
    """
    Update boss attacks & enrage
    Returns: boss_hp, boss_max_hp
    """

    # ---------- ENRAGE ----------
    if not state["enraged"] and boss_hp <= boss_max_hp * ENRAGE_THRESHOLD:
        state["enraged"] = True
        boss_hp = int(boss_hp * ENRAGE_HP_MULT)
        boss_max_hp = int(boss_max_hp * ENRAGE_HP_MULT)
        state["speed_mult"] = 1.3

    speed = state["speed_mult"]

    # ---------- SWITCH ATTACK ----------
    state["switch_timer"] -= 1
    if state["switch_timer"] <= 0:
        state["current"] = (
            state["attack_b"]
            if state["current"] == state["attack_a"]
            else state["attack_a"]
        )
        state["switch_timer"] = state["switch_time"]
        state["fire_timer"] = 10
        state["burst_count"] = 0

    state["fire_timer"] -= 1
    atk = state["current"]

    # ---------- ATTACK LOGIC ----------
    if atk == "sniper" and state["fire_timer"] <= 0:
        spawn_sniper(boss_rect, boss_bullets, player_rect, bullet_speed * 1.4)
        state["fire_timer"] = int(SNIPER_CD / speed)

    elif atk == "burst":
        if state["burst_count"] < 3:
            spawn_burst(boss_rect, boss_bullets, bullet_speed * 1.1)
            state["burst_count"] += 1
            state["fire_timer"] = 10
        else:
            state["burst_count"] = 0
            state["fire_timer"] = int(BURST_CD / speed)

    elif atk == "wave" and state["fire_timer"] <= 0:
        spawn_wave(boss_rect, boss_bullets, bullet_speed)
        state["fire_timer"] = int(WAVE_CD / speed)

    elif atk == "spiral" and state["fire_timer"] <= 0:
        spawn_spiral(boss_rect, boss_bullets, bullet_speed, state["spiral_angle"])
        state["spiral_angle"] = (state["spiral_angle"] + 20) % 360
        state["fire_timer"] = int(SPIRAL_CD / speed)

    elif atk == "mine" and state["fire_timer"] <= 0:
        spawn_mine(boss_rect, state["mines"])
        state["fire_timer"] = 95

    elif atk == "summon" and state["fire_timer"] <= 0:
        for _ in range(2 if not state["enraged"] else 3):
            sharks.append(
                shark_image.get_rect(
                    x=800,
                    y=random.randint(0, 600 - shark_image.get_height())
                )
            )
        state["fire_timer"] = int(SUMMON_CD / speed)

    return boss_hp, boss_max_hp
