import pygame
import os
from coins import CoinManager

def show_itemshop(screen, coin_manager, unlocked_fishes):
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 26)
    big_font = pygame.font.SysFont(None, 36)

    WIDTH, HEIGHT = screen.get_size()

    # -------------------------------
    # BUTTONS
    # -------------------------------
    back_button = pygame.Rect(20, 20, 120, 45)

    # -------------------------------
    # FISH ITEMS
    # -------------------------------
    fish_items = [
        {"name": "vis1", "price": 0},
        {"name": "vis2", "price": 10},
        {"name": "vis3", "price": 20},
        {"name": "vis4", "price": 30},
        {"name": "vis5", "price": 50},
    ]

    # -------------------------------
    # MAIN LOOP
    # -------------------------------
    while True:
        screen.fill((10, 30, 70))

        # Titel
        title = big_font.render("ITEMSHOP", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - 90, 20))

        # Coins
        coin_text = font.render(
            f"Coins: {coin_manager.get_count()}",
            True,
            (255, 215, 0)
        )
        screen.blit(
            coin_text,
            (WIDTH - coin_text.get_width() - 20, 20)
        )



        # TERUG KNOP
        pygame.draw.rect(screen, (200, 60, 60), back_button)
        pygame.draw.rect(screen, (0, 0, 0), back_button, 3)
        screen.blit(font.render("TERUG", True, (255, 255, 255)),
                    (back_button.x + 30, back_button.y + 12))

        # -------------------------------
        # FISH SHOP GRID
        # -------------------------------
        start_x = 120
        start_y = 120
        spacing_x = 160

        for i, item in enumerate(fish_items):
            x = start_x + i * spacing_x
            y = start_y

            rect = pygame.Rect(x, y, 120, 100)
            pygame.draw.rect(screen, (180, 220, 255), rect, border_radius=12)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=12)

            # Fish image
            img_path = os.path.join("img", item["name"] + ".png")
            if os.path.exists(img_path):
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (90, 45))
                screen.blit(img, (x + 15, y + 10))

            # STATUS / PRICE
            if item["name"] in unlocked_fishes:
                status = font.render("UNLOCKED", True, (0, 150, 0))
                screen.blit(status, (x + 15, y + 65))
            else:
                price = font.render(f"{item['price']}c", True, (0, 0, 0))
                screen.blit(price, (x + 40, y + 65))

        # -------------------------------
        # EVENTS
        # -------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # TERUG NAAR LOCKER
                if back_button.collidepoint(mx, my):
                    return "locker"

                if event.type == pygame.QUIT:
                    return "quit"


                # FISH BUY
                for i, item in enumerate(fish_items):
                    x = start_x + i * spacing_x
                    y = start_y
                    rect = pygame.Rect(x, y, 120, 100)

                    if rect.collidepoint(mx, my):
                        if item["name"] not in unlocked_fishes:
                            if coin_manager.get_count() >= item["price"]:
                                coin_manager.count -= item["price"]
                                coin_manager._save()
                                unlocked_fishes.append(item["name"])


        pygame.display.flip()
        clock.tick(60)
