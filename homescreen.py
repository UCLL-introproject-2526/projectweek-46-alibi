import pygame
import random
import math
# ===== ACHTERGROND =====
from window import draw_background

# --------------------------------
#   OUTLINED TEKST
# --------------------------------
def draw_outlined_text(screen, text, font, color, outline_color, pos):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                outline = font.render(text, True, outline_color)
                screen.blit(outline, (pos[0] + dx, pos[1] + dy))


    screen.blit(font.render(text, True, color), pos)


# --------------------------------
#   HOME SCREEN
# --------------------------------
def show_home_screen(screen):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # ---------- AUDIO ----------
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    pygame.mixer.music.load("muziek/jaws.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    click_sound = pygame.mixer.Sound("muziek/shark_bite.mp3")
    click_sound.set_volume(0.6)

    # ---------- AFBEELDING ----------
    shark_img = pygame.image.load("img/shark_mouth.png").convert_alpha()
    shark_img = pygame.transform.scale(shark_img, (420, 620))

    arrow_up_img = pygame.image.load("img/pijltjeomhoog1.png").convert_alpha()
    arrow_up_img = pygame.transform.scale(arrow_up_img, (24, 24))

    arrow_down_img = pygame.image.load("img/pijltjeomlaag1.png").convert_alpha()
    arrow_down_img = pygame.transform.scale(arrow_down_img, (24, 24))

    # ---------- UI ----------
    title_font = pygame.font.SysFont("arialblack", 72)
    sub_font = pygame.font.SysFont("arial", 25)
    button_font = pygame.font.SysFont("arial", 34)

    start_button  = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 + 120, 320, 70)
    locker_button = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 + 210, 320, 70)
    close_button  = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 + 300, 320, 70)

    pygame.event.clear()
    time = 0

    # ---------- LOOP ----------
    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit"

            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.collidepoint(event.pos):
                    click_sound.play()
                    pygame.mixer.music.stop()
                    return "start"

                if locker_button.collidepoint(event.pos):
                    click_sound.play()
                    pygame.mixer.music.stop()
                    return "locker"

                if close_button.collidepoint(event.pos):
                    click_sound.play()
                    pygame.mixer.music.stop()
                    return "quit"

        # ===== ACHTERGROND =====
        draw_background(screen, time, scroll=False)
          # ===== CONTROLS (RECHTS) =====
        controls_x = 15
        controls_y = -5

    

        controls = [
            (None, "CONTROLS:"),
            ("up", " → VIS OMHOOG"),
            ("down", " → VIS OMLAAG")
            ]
        
        for i, (img_key, text) in enumerate(controls):
            x_pos = controls_x
            if img_key == "up":
                screen.blit(arrow_up_img, (x_pos, controls_y + 20 + i * 28))
                x_pos += arrow_up_img.get_width() + 5
            elif img_key == "down":
                screen.blit(arrow_down_img, (x_pos, controls_y + 20 + i * 28))
                x_pos += arrow_down_img.get_width() + 5
            draw_outlined_text(
                screen,
                text,
                sub_font,
                (210, 230, 255),
                (0, 0, 0),
                (x_pos, controls_y + 20 + i * 28)
            )




        # ===== HAAI (STIL) =====
        screen.blit(
            shark_img,
            (WIDTH//2 - shark_img.get_width()//2, 120)
        )

        # ===== TITEL =====
        title_text = "SHARK ATTACK"
        title_surface = title_font.render(title_text, True, (30, 70, 120))
        title_x = WIDTH//2 - title_surface.get_width()//2

        draw_outlined_text(
            screen,
            title_text,
            title_font,
            (30, 70, 120),
            (255, 255, 255),
            (title_x, 200)
        )

        subtitle_text = "ONTWIJK DE HONGERIGE HAAIEN EN VERZAMEL SCHATTEN!"
        

        draw_outlined_text(
            screen,
            subtitle_text,
            sub_font,
            (50, 100, 160),   # tekstkleur
            (255, 255, 255),  # witte rand (zelfde als titel)
            (WIDTH//2 - sub_font.size(subtitle_text)[0]//2, 280)
        )




        # ===== KNOPPEN =====
        for rect, text in [
            (start_button, "START GAME"),
            (locker_button, "LOCKER"),
            (close_button, "SLUITEN")
        ]:
            hover = rect.collidepoint(mouse_pos)

            if rect == close_button:
                color = (200, 60, 60) if hover else (160, 40, 40)
            else:
                color = (70, 140, 200) if hover else (50, 120, 180)

            pygame.draw.rect(screen, color, rect, border_radius=14)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=14)

            label = button_font.render(text, True, (255, 255, 255))
            screen.blit(
                label,
                (rect.centerx - label.get_width()//2,
                 rect.centery - label.get_height()//2)
            )

        time += 1
        pygame.display.flip()
        clock.tick(60)
