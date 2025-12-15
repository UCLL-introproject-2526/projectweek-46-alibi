import pygame
from homescreen import show_home_screen
from game import create_main_surface   # of waar je game-functie staat

pygame.init()

WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Deep Sea")

while True:
    action = show_home_screen(screen)

    if action == "start":
        create_main_surface()

    if action == "quit":
        break

pygame.quit()
