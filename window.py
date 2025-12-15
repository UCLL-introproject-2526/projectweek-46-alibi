import pygame
import math
import random

def create_main_surface():
    pygame.init()

    width, height = 1024, 768
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Deep Sea - Real Fish")

    clock = pygame.time.Clock()
    running = True
    time = 0

    # --- Laad echte vis afbeeldingen ---
    fish_images = [
        pygame.image.load("clownfish.png").convert_alpha(),
        pygame.image.load("bluetang.png").convert_alpha(),
        pygame.image.load("yellowfish.png").convert_alpha()
    ]

    # Schaal alles netjes
    fish_images = [
        pygame.transform.scale(img, (img.get_width() // 2, img.get_height() // 2))
        for img in fish_images
    ]

    # --- Planten ---
    plants = []
    for _ in range(45):
        x = random.randint(0, width)
        h = random.randint(40, 140)
        wiggle = random.uniform(0.015, 0.05)
        plants.append((x, h, wiggle))

    # --- Vissen (gebruik echte sprites) ---
    fish_list = []
    for _ in range(10):
        img = random.choice(fish_images)
        x = random.randint(0, width)
        y = random.randint(100, height - 250)
        speed = random.uniform(1.0, 3.0)
        direction = random.choice([1, -1])
        fish_list.append([x, y, speed, direction, img])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((10, 40, 80))

        # Lichtdeeltjes
        for i in range(200):
            px = random.randint(0, width)
            py = (random.randint(0, height) + time) % (height - 140)
            screen.set_at((px, py), (80, 130, 180))

        # Bodem
        pygame.draw.rect(screen, (180, 165, 120), (0, height - 140, width, 140))

        # Planten
        for x, h, wiggle in plants:
            top_x = x + math.sin(time * wiggle) * (5 + h * 0.05)
            pygame.draw.line(
                screen,
                (40, 130, 90),
                (x, height - 20),
                (top_x, height - 140 + (140 - h)),
                5 if h > 90 else 3
            )

        # --- Echte vissen tekenen ---
        for fish in fish_list:
            x, y, speed, direction, img = fish

            fish[0] += speed * direction

            # Reset wanneer buiten beeld
            if direction == 1 and x > width + 100:
                fish[0] = -100
                fish[1] = random.randint(100, height - 250)
            elif direction == -1 and x < -100:
                fish[0] = width + 100
                fish[1] = random.randint(100, height - 250)

            # Als de vis links zwemt: flip horizontaal
            draw_img = pygame.transform.flip(img, True, False) if direction == -1 else img

            screen.blit(draw_img, (fish[0], fish[1]))

        time += 1
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()







create_main_surface()