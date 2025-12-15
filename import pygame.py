import pygame

def create_main_surface():
    pygame.init()

    screen_size = (1024, 768)
    screen = pygame.display.set_mode(screen_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # optional: clear screen
        screen.fill((0, 0, 0))
        pygame.display.flip()

    pygame.quit()

create_main_surface()