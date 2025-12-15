import pygame

from homescreen import show_home_screen
from locker import show_locker
from sharks import run_game

WIDTH, HEIGHT = 1024, 768


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shark Attack")

    state = "home"
    running = True

    # standaard vis (voor het geval locker niet wordt geopend)
    player_color = (255, 0, 0)
    player_pattern = "none"

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
                state = "game"
            else:  # "back"
                state = "home"

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
