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

    # (optioneel) spelerdata
    player_color = None

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
            result = show_locker(screen)

            # locker geeft nu (actie, kleur) terug
            if result is not None:
                action, player_color = result

                if action == "start":
                    state = "game"
                else:  # "back"
                    state = "home"
            else:
                state = "home"

        # ================= GAME =================
        elif state == "game":
            result = run_game(screen)

            # game klaar → terug naar menu
            if result == "quit":
                running = False
            else:
                state = "home"

    pygame.quit()


if __name__ == "__main__":
    main()
