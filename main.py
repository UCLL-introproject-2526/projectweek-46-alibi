import pygame
import window
from homescreen import show_home_screen
from window import create_main_surface

pygame.init()

screen = pygame.display.set_mode((window.WIDTH, window.HEIGHT))

# 1️⃣ eerst window.py
window.setup_window()

# 2️⃣ homescreen
while True:
    action = show_home_screen(screen)

    if action == "start":
        create_main_surface()

    elif action == "locker":
        show_locker(screen)

    elif action == "quit":
        break

pygame.quit()

