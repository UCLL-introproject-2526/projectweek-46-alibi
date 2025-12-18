import pygame
import os
import random
from coins import CoinManager
from unlocked_fishes import save_unlocked_fishes
from window import draw_background
from powerups import FISH_POWERUPS

def show_itemshop(screen, coin_manager, unlocked_fishes):
    pygame.init()
    clock = pygame.time.Clock()
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("muziek/baby_shark.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    font = pygame.font.SysFont(None, 26)
    big_font = pygame.font.SysFont(None, 36)
    power_font = pygame.font.SysFont(None, 18)

    coin_img = pygame.image.load("img/muntje.png").convert_alpha()
    coin_img = pygame.transform.scale(coin_img, (24, 24))
    kaching_sound = pygame.mixer.Sound("muziek/kaging.mp3")
    kaching_sound.set_volume(0.6)

    WIDTH, HEIGHT = screen.get_size()
    back_button = pygame.Rect(20, 20, 120, 45)

    fish_names = ["vis1","vis2","vis3","vis4","vis5","vis6","vis7","vis8","vis9","vis10"]
    start_price = 20
    step = 20
    fish_items = [{"name": name, "price": start_price + i*step} for i, name in enumerate(fish_names)]

    item_width, item_height = 120, 100
    spacing_x, spacing_y = 40, 30
    start_y = 120

    scroll_y = 0
    SCROLL_SPEED = 40
    time = 0

    # SHAKE VARS
    shake_timer = 0
    SHAKE_DURATION = 15
    SHAKE_INTENSITY = 6
    world_surface = pygame.Surface((WIDTH, HEIGHT))

    while True:
        time += 1

        # SHAKE OFFSET
        shake_x = shake_y = 0
        if shake_timer > 0:
            shake_x = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY)
            shake_y = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY)
            shake_timer -= 1

        # TEKENEN OP world_surface
        world_surface.fill((0,0,0))
        draw_background(world_surface, time, scroll=False)

        # HEADER
        title = big_font.render("ITEMSHOP", True, (255,255,255))
        world_surface.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        coin_text = font.render(f"Coins: {coin_manager.get_count()}", True, (255,215,0))
        world_surface.blit(coin_text, (WIDTH - coin_text.get_width() - 20, 20))

        pygame.draw.rect(world_surface, (200,60,60), back_button)
        pygame.draw.rect(world_surface, (0,0,0), back_button, 3)
        world_surface.blit(font.render("TERUG", True, (255,255,255)), (back_button.x + 30, back_button.y + 12))

        # GRID LAYOUT
        available_width = WIDTH - 40
        items_per_row = max(1, available_width // (item_width + spacing_x))
        grid_width = items_per_row*item_width + (items_per_row-1)*spacing_x
        start_x = (WIDTH - grid_width)//2

        for i, item in enumerate(fish_items):
            row = i // items_per_row
            col = i % items_per_row
            x = start_x + col*(item_width + spacing_x)
            y = start_y + row*(item_height + spacing_y) + scroll_y
            rect = pygame.Rect(x,y,item_width,item_height)

            if y > HEIGHT or y + item_height < 100:
                continue

            pygame.draw.rect(world_surface, (180,220,255), rect, border_radius=12)
            pygame.draw.rect(world_surface, (0,0,0), rect, 2, border_radius=12)

            img_path = os.path.join("img", item["name"]+".png")
            if os.path.exists(img_path):
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img,(90,45))
                world_surface.blit(img, (x+15, y+10))

            power = FISH_POWERUPS.get(item["name"])
            if power:
                power_text = power_font.render(power.replace("_"," ").upper(), True, (0,0,0))
                px = x + (item_width - power_text.get_width())//2
                py = y + 60
                world_surface.blit(power_text, (px, py))

            if item["name"] in unlocked_fishes:
                status = font.render("UNLOCKED", True, (0,150,0))
                world_surface.blit(status, (x+15, y+75))
            else:
                price_text = font.render(str(item["price"]), True, (0,0,0))
                world_surface.blit(price_text, (x+35, y+75))
                coin_x = x + 35 + price_text.get_width() + 4
                coin_y = y + 75 + (price_text.get_height() - coin_img.get_height())//2
                world_surface.blit(coin_img, (coin_x, coin_y))

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEWHEEL:
                scroll_y += event.y*SCROLL_SPEED
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if back_button.collidepoint(mx, my):
                    return "locker"
                clicked_any = False
                for i, item in enumerate(fish_items):
                    row = i // items_per_row
                    col = i % items_per_row
                    x = start_x + col*(item_width + spacing_x)
                    y = start_y + row*(item_height + spacing_y) + scroll_y
                    rect = pygame.Rect(x,y,item_width,item_height)
                    if rect.collidepoint(mx,my):
                        clicked_any = True
                        if item["name"] not in unlocked_fishes:
                            if coin_manager.get_count() >= item["price"]:
                                coin_manager.count -= item["price"]
                                coin_manager._save()
                                unlocked_fishes.append(item["name"])
                                save_unlocked_fishes(unlocked_fishes)
                                kaching_sound.play()
                            else:
                                shake_timer = SHAKE_DURATION

        # SCROLL LIMITS
        total_rows = (len(fish_items) + items_per_row - 1)//items_per_row
        content_height = total_rows*(item_height + spacing_y)
        max_scroll = 0
        min_scroll = min(0, HEIGHT - (start_y + content_height + 20))
        scroll_y = max(min_scroll, min(max_scroll, scroll_y))

        # BLIT WORLD MET SHAKE
        screen.fill((0,0,0))
        screen.blit(world_surface, (shake_x, shake_y))
        pygame.display.flip()
        clock.tick(60)
