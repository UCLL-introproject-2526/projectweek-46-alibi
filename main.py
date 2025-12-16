import pygame

import coins
from homescreen import show_home_screen
from locker import show_locker
from sharks import run_game
from coins import CoinManager
from highscores import show_highscores
from itemshop import show_itemshop

# -------------------------------
#   INIT
# -------------------------------
pygame.init()
SCREEN_W, SCREEN_H = 1023, 768
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Shark Attack")

clock = pygame.time.Clock()

# -------------------------------
#   GAME STATE
# -------------------------------
state = "home"
unlocked_colors = []
unlocked_patterns = []
# gekozen vis (default)
selected_fish = "img/vis1.png"
selected_pattern = "none"

# -------------------------------
#   MAIN LOOP
# -------------------------------
running = True
coin_manager = CoinManager(spawn_chance=0.05, max_coins=8)

while running:

    if state == "home":
        state = show_home_screen(screen)

    elif state == "locker":
        result = show_locker(screen)
        # show_locker geeft terug:
        # ("start", fish, pattern)
        # ("back", None, None)
        # ("itemshop", fish, pattern)
        if result:
            action, fish, pattern = result

            if action == "start":
                selected_fish = fish
                selected_pattern = pattern
                state = "start"

            elif action == "back":
                state = "home"

            elif action == "itemshop":
                # doorverwijzen naar itemshop
                selected_fish = fish
                selected_pattern = pattern
                state = "itemshop"

            elif action == "start":
                selected_fish = fish
                selected_pattern = pattern
                state = "start"
    elif state == "itemshop":
        action = show_itemshop(screen, coins, unlocked_colors, unlocked_patterns)

        if action == "locker":
            state = "locker"
        elif action == "quit":
            running = False
        elif action == "start":
                selected_fish = fish
                selected_pattern = pattern
                state = "start"
    elif state == "start":
        state = run_game(screen, selected_fish, selected_pattern, coin_manager)

    elif state == "highscores":
        state = show_highscores(screen)

    elif state == "quit":
        running = False

    clock.tick(60)

pygame.quit()
