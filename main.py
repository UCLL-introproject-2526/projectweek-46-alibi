import pygame

from homescreen import show_home_screen
from locker import show_locker
from window import create_main_surface

WIDTH, HEIGHT = 1024, 768

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Deep Sea")

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

        elif state == "game":
            create_main_surface()
            state = "home"   # ⬅️ BELANGRIJK: terug naar homescreen

        elif state == "locker":
            show_locker(screen)
            state = "home"   # ⬅️ BELANGRIJK: terug naar homescreen

    pygame.quit()


if __name__ == "__main__":
    main()
