def show_itemshop(screen, coins, unlocked_colors, unlocked_patterns):
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    WIDTH, HEIGHT = screen.get_size()

    shop_height = 0
    shop_target_height = 260
    shop_open = False

    shop_button = pygame.Rect(WIDTH - 90, 20, 70, 70)

    # TERUG KNOP
    back_button = pygame.Rect(20, 20, 100, 40)   # links bovenaan in shop

    color_items = [
        {"color": (255, 100, 0), "price": 10},
        {"color": (0, 255, 200), "price": 15},
        {"color": (200, 0, 255), "price": 20}
    ]

    pattern_items = [
        {"name": "stripes", "price": 15},
        {"name": "dots", "price": 20},
        {"name": "waves", "price": 25}
    ]

    def draw_shop():
        pygame.draw.rect(screen, (20, 40, 80), (0, 0, WIDTH, shop_height))

        title = font.render("ITEMSHOP", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - 60, 10))
        
        # TERUG-KNOP TEKENEN (ALLEEN ALS SHOP OPEN STAAT)
        if shop_open:
            pygame.draw.rect(screen, (200, 50, 50), back_button)
            pygame.draw.rect(screen, (0,0,0), back_button, 3)
            back_text = font.render("TERUG", True, (255,255,255))
            screen.blit(back_text, (back_button.x + 10, back_button.y + 10))

        y_offset = 60

        screen.blit(font.render("Kleuren:", True, (255,255,255)), (40, y_offset))
        y_offset += 40

        for i, item in enumerate(color_items):
            x = 40 + i * 120
            rect = pygame.Rect(x, y_offset, 60, 40)

            pygame.draw.rect(screen, item["color"], rect)
            pygame.draw.rect(screen, (0,0,0), rect, 2)

            price_text = font.render(f"{item['price']}c", True, (255,255,255))
            screen.blit(price_text, (x, y_offset + 50))

        y_offset += 110

        screen.blit(font.render("Patronen:", True, (255,255,255)), (40, y_offset))
        y_offset += 40

        for i, item in enumerate(pattern_items):
            x = 40 + i * 140
            rect = pygame.Rect(x, y_offset, 110, 40)

            pygame.draw.rect(screen, (200,200,200), rect)
            pygame.draw.rect(screen, (0,0,0), rect, 2)

            text = font.render(item["name"], True, (0,0,0))
            screen.blit(text, (x + 10, y_offset + 10))

            price_text = font.render(f"{item['price']}c", True, (255,255,255))
            screen.blit(price_text, (x, y_offset + 50))

    # -------------------------------
    # MAIN LOOP
    # -------------------------------
    while True:
        screen.fill((5, 20, 60))

        if shop_open and shop_height < shop_target_height:
            shop_height += 10
        if not shop_open and shop_height > 0:
            shop_height -= 10

        draw_shop()

        pygame.draw.rect(screen, (255, 200, 0), shop_button)
        pygame.draw.rect(screen, (0, 0, 0), shop_button, 3)
        screen.blit(font.render("SHOP", True, (0,0,0)),
                    (shop_button.x + 10, shop_button.y + 20))

        coin_text = font.render(f"Coins: {coins}", True, (255,255,0))
        screen.blit(coin_text, (20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return coins, unlocked_colors, unlocked_patterns, "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # SHOP OPENEN / SLUITEN
                if shop_button.collidepoint(mx, my):
                    shop_open = not shop_open

                # TERUG NAAR LOCKER
                if shop_open and back_button.collidepoint(mx, my):
                    return coins, unlocked_colors, unlocked_patterns, "locker"

                if shop_open:
                    # KLEUREN KOPEN
                    for i, item in enumerate(color_items):
                        x = 40 + i * 120
                        rect = pygame.Rect(x, 100, 60, 40)

                        if rect.collidepoint(mx, my) and coins >= item["price"]:
                            coins -= item["price"]
                            unlocked_colors.append(item["color"])

                    # PATRONEN KOPEN
                    for i, item in enumerate(pattern_items):
                        x = 40 + i * 140
                        rect = pygame.Rect(x, 210, 110, 40)

                        if rect.collidepoint(mx, my) and coins >= item["price"]:
                            coins -= item["price"]
                            unlocked_patterns.append(item["name"])

        pygame.display.flip()
        clock.tick(60)
