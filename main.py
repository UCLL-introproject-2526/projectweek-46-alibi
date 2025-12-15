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

    while running:

        if state == "home":
            action = show_home_screen(screen)

            if action == "start":
                state = "game"
            elif action == "locker":
                state = "locker"
            elif action == "quit":
                running = False

        elif state == "locker":
            show_locker(screen)
            state = "home"

        elif state == "game":
            result = run_game(screen)
            if result == "quit":
                running = False
            else:
                state = "home"

    pygame.quit()

if __name__ == "__main__":
    main()
