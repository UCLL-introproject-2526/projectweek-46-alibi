import pygame
import math

from homescreen import show_home_screen
from locker import show_locker
from sharks import run_game
from window import draw_background

WIDTH, HEIGHT = 1024, 768


# -------------------------------
#   SPELER VIS (kleiner formaat)
# -------------------------------
FISH_W = 50
FISH_H = 30

def draw_player_fish(surface, color, pattern, x, y, w=FISH_W, h=FISH_H):
    scale_x = w / FISH_W
    scale_y = h / FISH_H

    # body
    pygame.draw.ellipse(surface, color, (x, y, w, h))

    # staart
    tail_length = 32 * scale_x
    pygame.draw.polygon(
        surface, color,
        [(x, y + h//2), (x - tail_length, y), (x - tail_length, y + h)]
    )

    # oog
    eye_x = x + w - 16 * scale_x
    eye_y = y + h//2
    eye_radius = 4 * scale_x
    pygame.draw.circle(
        surface, (0, 0, 0),
        (eye_x, eye_y),
        eye_radius
    )

    # patronen
    if pattern == "stripes":
        for i in range(3):
            rect_x = x + 18 * scale_x + i * 18 * scale_x
            rect_y = y + 4 * scale_y
            rect_w = 8 * scale_x
            rect_h = (h - 8 * scale_y)
            pygame.draw.rect(
                surface, (255, 255, 255),
                (rect_x, rect_y, rect_w, rect_h),
                2
            )

    elif pattern == "dots":
        for i in range(4):
            dot_x = x + 18 * scale_x + i * 18 * scale_x
            dot_y = y + 16 * scale_y + (i % 2) * 8 * scale_y
            dot_radius = 5 * scale_x
            pygame.draw.circle(
                surface, (255, 255, 255),
                (dot_x, dot_y),
                dot_radius
            )

    elif pattern == "waves":
        for i in range(5):
            wx = x + 14 * scale_x + i * 16 * scale_x
            wy = y + h//2 + math.sin(i * 0.9) * 6 * scale_y
            wave_radius = 3 * scale_x
            pygame.draw.circle(surface, (255, 255, 255), (wx, int(wy)), wave_radius)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shark Attack")
    clock = pygame.time.Clock()

    state = "home"
    running = True

    # standaard vis (voor het geval locker niet wordt geopend)
    player_color = (255, 0, 0)
    player_pattern = "none"

    # transition variables
    transition_start_pos = (WIDTH//2 - 60, HEIGHT // 2 - 30)
    transition_end_pos = (100, HEIGHT // 2)
    transition_start_size = (120, 60)
    transition_end_size = (50, 30)
    transition_duration = 120  # frames (2 seconds at 60 FPS)
    transition_frame = 0

    while running:

        # ================= HOMESCREEN =================
        if state == "home":
            action = show_home_screen(screen)

            if action == "start":
                state = "game"

            elif action == "locker":
                state = "locker"

            elif action == "quit":
                running = False

        # ================= LOCKER =================
        elif state == "locker":
            action, color, pattern = show_locker(screen)

            if action == "start":
                player_color = color
                player_pattern = pattern
                state = "transition"
                transition_frame = 0
            else:  # "back"
                state = "home"

        # ================= TRANSITION =================
        elif state == "transition":
            # animate fish from locker to game start position
            t = transition_frame / transition_duration
            current_x = transition_start_pos[0] + (transition_end_pos[0] - transition_start_pos[0]) * t
            current_y = transition_start_pos[1] + (transition_end_pos[1] - transition_start_pos[1]) * t
            current_w = transition_start_size[0] + (transition_end_size[0] - transition_start_size[0]) * t
            current_h = transition_start_size[1] + (transition_end_size[1] - transition_start_size[1]) * t

            draw_background(screen, transition_frame)

            draw_player_fish(screen, player_color, player_pattern, current_x, current_y, current_w, current_h)

            transition_frame += 1

            if transition_frame >= transition_duration:
                state = "game"
                transition_frame = 0

            # handle events during transition
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
            clock.tick(60)

        # ================= GAME =================
        elif state == "game":
            result = run_game(screen, player_color, player_pattern)

            if result == "quit":
                running = False
            else:
                state = "home"

    pygame.quit()


if __name__ == "__main__":
    main()
