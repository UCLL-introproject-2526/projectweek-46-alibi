import pygame
import random
import math
# ===== ACHTERGROND =====
from window import draw_background

# --------------------------------
#   OUTLINED TEKST
# --------------------------------
def draw_outlined_text(screen, text, font, color, outline_color, pos):
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
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

    # ---------- UI ----------
    title_font = pygame.font.SysFont("arialblack", 72)
    sub_font = pygame.font.SysFont("arial", 32)
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

        subtitle = sub_font.render(
            "Ontwijk de hongerige haaien en verzamel schatten!",
            True,
            (50, 100, 160)
        )
        screen.blit(subtitle,
                    (WIDTH//2 - subtitle.get_width()//2, 280))

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
