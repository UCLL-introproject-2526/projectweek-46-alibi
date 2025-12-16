import pygame
import math

from homescreen import show_home_screen
from locker import show_locker
from sharks import run_game
from window import draw_background
from itemshop import show_itemshop      

WIDTH, HEIGHT = 1024, 768

FISH_W = 50
FISH_H = 30

def draw_player_fish(surface, fish, pattern, x, y, w=FISH_W, h=FISH_H):
    image = pygame.image.load(fish + ".png").convert_alpha()
    image = pygame.transform.scale(image, (int(w), int(h)))
    surface.blit(image, (x, y))

    scale_x = w / FISH_W
    scale_y = h / FISH_H

    if pattern == "stripes":
        for i in range(3):
            pygame.draw.rect(surface, (255, 255, 255),
                (x + 18*scale_x + i*18*scale_x, y + 4*scale_y,
                 8*scale_x, h - 8*scale_y), 2)

    elif pattern == "dots":
        for i in range(4):
            pygame.draw.circle(surface, (255, 255, 255),
                (x + 18*scale_x + i*18*scale_x,
                 y + 16*scale_y + (i % 2)*8*scale_y),
                5*scale_x)

    elif pattern == "waves":
        for i in range(5):
            wx = x + 14*scale_x + i*16*scale_x
            wy = y + h//2 + math.sin(i*0.9) * 6 * scale_y
            pygame.draw.circle(surface, (255,255,255), (wx, int(wy)), 3)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shark Attack")
    clock = pygame.time.Clock()

    state = "home"
    running = True

    # ----------------------------
    #   COINS + UNLOCK INFORMATION
    # ----------------------------
    coins = 0
    unlocked_colors = []
    unlocked_patterns = []

    # standaard vis
    player_color = (255, 0, 0)
    player_pattern = "none"
    player_fish = "vis1"

    transition_start_pos = (WIDTH//2 - 60, HEIGHT // 2 - 30)
    transition_end_pos = (100, HEIGHT // 2)
    transition_start_size = (120, 60)
    transition_end_size = (50, 30)
    transition_duration = 120
    transition_frame = 0

    while running:

        # ========== HOME ==========
        if state == "home":
            action = show_home_screen(screen)

            if action == "start":
                state = "game"

            elif action == "locker":
                state = "locker"

            elif action == "quit":
                running = False

        # ========== LOCKER ==========
        elif state == "locker":
            action, color, pattern = show_locker(screen)

            if action == "start":
                player_fish = color
                player_pattern = pattern
                state = "transition"

            elif action == "itemshop":
                state = "itemshop"

            else:
                state = "home"

        # ========== ITEMSHOP ==========
        elif state == "itemshop":
            coins, unlocked_colors, unlocked_patterns = show_itemshop(
                screen,
                coins,
                unlocked_colors,
                unlocked_patterns
            )

            # TERUG NAAR LOCKER
            state = "locker"

        # ========== TRANSITION ==========
        elif state == "transition":
            t = transition_frame / transition_duration
            current_x = transition_start_pos[0] + (transition_end_pos[0] - transition_start_pos[0]) * t
            current_y = transition_start_pos[1] + (transition_end_pos[1] - transition_start_pos[1]) * t
            current_w = transition_start_size[0] + (transition_end_size[0] - transition_start_size[0]) * t
            current_h = transition_start_size[1] + (transition_end_size[1] - transition_start_size[1]) * t

            draw_background(screen, transition_frame)
            draw_player_fish(screen, player_fish, player_pattern, current_x, current_y, current_w, current_h)

            transition_frame += 1

            if transition_frame >= transition_duration:
                state = "game"
                transition_frame = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
            clock.tick(60)

        # ========== GAME ==========
        elif state == "game":
            result = run_game(screen, player_fish, player_pattern)

            if result == "quit":
                running = False
            else:
                state = "home"

    pygame.quit()


if __name__ == "__main__":
    main()
